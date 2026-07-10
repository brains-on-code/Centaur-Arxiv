from transformers import TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from datasets import load_dataset, Dataset
import pandas as pd
import scipy
import math
import torch
from accelerate.utils import release_memory
import gc
from sys import float_info
import os
from time import sleep

load_existing = True
modelnames = ["Centaur", "Llama"]
modeladdresses = {"Centaur": "marcelbinz/Llama-3.1-Centaur-70B", "Llama": "meta-llama/Llama-3.1-70B-Instruct"}
task_names = ["Ajami18", "Bauer19", "Börstler16", "Buse10", "Gopstein17a", "Gopstein17b", "Medeiros19", "Siegmund17", "Peitek18"]
versions = ["", "_no_order", "_no_snippets", "_no_order_no_snippets", "_no_desc", "_no_order_no_desc", "_no_snippets_no_desc", "_no_order_no_snippets_no_desc"]
data_location = "GenericPipeline/Prompts/"
prob_thresh = 0.01
data_files = {task_name: [f"{data_location}{task_name}/{file}"  for file in os.listdir(f"{data_location}{task_name}")] for task_name in task_names}
data_files_all_versions = {}
for version in versions:
      for task in data_files: 
            data_files_all_versions[f"{task}{version}"] =  [f"{data_location}{task}{version}/{file}"  for file in os.listdir(f"{data_location}{task}{version}")]

def lk_to_dict(lk): 
      lk_arr = lk.strip("[]").split("], [")
      dict = {}
      for l in lk_arr: 
            key, val = l.split(", ")
            dict[int(key)] = float(val)
      return(dict)
def loss_from_df(df): 
      correct_labels = df["correct"]
      answer = df["answer"]
      likelihoods = df["likelihoods"]
      eval_loss = 0
      count = 0
      curr_iter = -1
      prob = 1
      for label, iter, lk in zip(correct_labels, answer, likelihoods):  
            lbl, atkn = label.strip("[]").split(",")
            lk_dict = lk_to_dict(lk)
            if curr_iter == -1: 
                  curr_iter = iter
            if curr_iter == iter : 
                  p = lk_dict[int(lbl)] if atkn == " None" else lk_dict[int(lbl)]+lk_dict[int(atkn)] 
                  prob *= p
            else: 
                  eval_loss += -math.log(prob)
                  count += 1
                  p = lk_dict[int(lbl)] if atkn == " None" else lk_dict[int(lbl)]+lk_dict[int(atkn)] 
                  prob = p
                  curr_iter = iter
      eval_loss += -math.log(prob)
      count += 1
      return(eval_loss, count)


with torch.no_grad():
      for modelname in modelnames:
            gc.collect()
            torch.cuda.empty_cache()
            model = AutoModelForCausalLM.from_pretrained(modeladdresses[modelname], torch_dtype=torch.bfloat16, device_map="auto")
            print(model.hf_device_map)
            tokenizer = AutoTokenizer.from_pretrained(modeladdresses[modelname])
            l_id = tokenizer(" <<").input_ids[1:]
            r_id = tokenizer(" >>").input_ids[1:]
            print(l_id, r_id)
            collator = DataCollatorForCompletionOnlyLM(response_template=l_id, instruction_template=r_id, tokenizer=tokenizer)
            is_quantized =False
            if modelname == "Llama": tokenizer.pad_token = tokenizer.eos_token 
            def metrics_test(predictions): 
                  relevant_pred = []
                  relevant_label = []
                  relevant_iter = []
                  sum_log_like = 0
                  count = 0
                  space_id = tokenizer(" ").input_ids[1:]
                  preds, labels = predictions
                  for part in range(len(preds)): 
                        relevant_part = []
                        iter_label = []
                        part_label_rev = []
                        part_pred = preds[part]
                        label_part = labels[part]
                        curr_pred = 1
                        pred_count = 1
                        ongoing_pred = False
                        buffer_count = 1
                        for i in range(len(label_part)):
                              label = label_part[i]
                              if not label == -100: #
                                    add_token = None
                                    if buffer_count != 0: 
                                          ongoing_pred = True
                                          buffer_count = 0
                                          if label == space_id: continue
                                          txt = tokenizer.decode(label)
                                          if txt[0] == " ": 
                                                tokens = tokenizer.encode(txt[1:])[1:]
                                                if len(tokens) == 1:
                                                      add_token = tokens[0]
                                    pred = part_pred[i-1] 
                                    softmax_pred = scipy.special.softmax(pred)
                                    if curr_pred*softmax_pred[label]==0: 
                                          print(curr_pred, softmax_pred[label])
                                    p = softmax_pred[label]
                                    if add_token != None: 
                                          p += softmax_pred[add_token]
                                    curr_pred *= p 
                                    #sum_log_like += -math.log(softmax_pred[label])
                                    #count += 1
                                    probs = []
                                    for j, prob in enumerate(softmax_pred): 
                                          if prob >= prob_thresh or j == label or j == add_token:
                                                probs.append([j, prob])
                                    relevant_part.append(probs)
                                    iter_label.append(pred_count)
                                    part_label_rev.append([label, add_token])
                              else: 
                                    if ongoing_pred: 
                                          buffer_count += 1
                                          if buffer_count >= 3:
                                                if curr_pred == 0: 
                                                      sum_log_like += -math.log(float_info.min)
                                                else:
                                                      sum_log_like += -math.log(curr_pred)
                                                count += 1
                                                ongoing_pred = False
                                                curr_pred = 1
                                                pred_count += 1
                        if ongoing_pred: 
                              if curr_pred == 0: 
                                    sum_log_like += -math.log(float_info.min)
                              else:
                                    sum_log_like += -math.log(curr_pred)
                              count += 1
                              ongoing_pred = False
                              curr_pred = 1
                        relevant_pred.append(relevant_part)
                        relevant_label.append(part_label_rev)
                        relevant_iter.append(iter_label)
                  return({"metrics": relevant_pred, "labels": relevant_label, "log-like": sum_log_like, "count": count, "iter": relevant_iter})

            for version in versions: 
                  data = []
                  for task_name in task_names:
                        eval_loss = 0
                        count = 0
                        df_count = 0
                        for file in data_files_all_versions[f"{task_name}{version}"]:
                              file_name = file.split("/")[-1]
                              print(file_name)
                              if load_existing and os.path.exists(f"GenericPipeline/results/aux/{modelname}/{task_name}{version}/{file_name}"):
                                    df = pd.read_csv(f"GenericPipeline/results/aux/{modelname}/{task_name}{version}/{file_name}")
                                    e_l, c =  loss_from_df(df)
                                    count += c
                                    eval_loss += e_l
                                    continue
                              data_df = pd.read_csv(file)
                              dataset = Dataset.from_pandas(data_df, split = "train")
                              eval_dataset = dataset.filter(lambda example: example['experiment'].startswith(task_name))
                              model.is_quantized = False
                              training_args = TrainingArguments(
                                    output_dir="eval",
                                    per_device_eval_batch_size=1
                              )
                              trainer = SFTTrainer(
                                    model=model,
                                    tokenizer=tokenizer,
                                    args=training_args,
                                    train_dataset=eval_dataset,
                                    eval_dataset=eval_dataset,
                                    dataset_text_field="text",
                                    max_seq_length=32768,
                                    compute_metrics=metrics_test,
                                    data_collator=collator,
                              )
                              model.is_quantized = False
                              print("starting evaluation")
                              result = trainer.evaluate()
                              labels = result['eval_labels']
                              likelihoods = result['eval_metrics']
                              iters = result['eval_iter']
                              token_data = []
                              for i in range(len(labels)):
                                    j = 0
                                    for l, lk, it in zip(labels[i], likelihoods[i], iters[i]): 
                                          token_data.append([f"{file_name}_{j}", it, l, lk])
                                          j += 1
                              count += result["eval_count"]
                              eval_loss += result["eval_log-like"]
                              print(eval_loss,count)
                              df = pd.DataFrame(token_data, columns=['participant', 'answer', 'correct', 'likelihoods'])
                              df_count +=1
                              os.makedirs(f"GenericPipeline/results/aux/{modelname}/{task_name}{version}/", exist_ok=True)
                              df.to_csv(f"GenericPipeline/results/aux/{modelname}/{task_name}{version}/{file_name}", index = False)
                        df_list = []
                        sleep(10)
                        for file in os.listdir(f"GenericPipeline/results/aux/{modelname}/{task_name}{version}/"):
                              df_list.append(pd.read_csv(f"GenericPipeline/results/aux/{modelname}/{task_name}{version}/{file}"))
                        df = pd.concat(df_list)
                        df.to_csv(f"GenericPipeline/results/{modelname}/{task_name}{version}_{modelname}.csv", index=False)
                        data.append([task_name, eval_loss/count])
                  df = pd.DataFrame(data, columns=['task', str(modelname)])
                  df.to_csv(f'GenericPipeline/results/{modelname}' + version +  '.csv')
            #trainer = release_memory(trainer)
            #tokenizer = release_memory(tokenizer)
            #model = release_memory(model)
            #del df
            #del df_list
            #gc.collect()
