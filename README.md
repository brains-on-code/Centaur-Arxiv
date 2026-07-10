# Predicting Program Comprehension with Foundation Models of Human Cognition

This repository contains the replication package, analysis scripts, and additional information for the paper "Predicting Program Comprehension with Foundation Models of Human Cognition"

## Prompts

The folder 'Prompts' contains the prompts used for each study and the scripts used to generate the ablations from the complete prompts.
Each study has its own subfolder of the form 'AuthorXX'.
Each study folder contains the following:

* A subfolder called 'snippets', containing all code snippets used in the original study. Some studies have additional subfolders containing other study materials.
* A subfolder called  'Supplemental\_files', containing a file 'notes.txt' documenting notable decisions made for this study and some .csv files containing statistical information used in creating the prompts or analysing the data.
* A subfolder called 'csv\_files' containing csv-files with the prompts used in our evaluation. This subfolder contains the following:

  * A subfolder called 'whole\_runs' containing the prompts used in RQ1.
  * A subfolder called 'ablations' containing one folder for each of the seven ablations for this study, which each contain the prompts used for this ablation.
  * A subfolder called 'zero\_shot' containing templates for ablations without sequence information with placeholders for responses.
  * A file 'AuthorXX\_whole\_runs.csv' containing all .csv files from the folder 'whole\_runs' in one file. Some studies have a similar file for 'zero\_shot'
* A file 'paper\_information.txt' containing the name of the paper and a link to its replication package.
* A file 'task\_description.txt' containing the task description used in the prompts of this study.

Additionally, the folder 'Prompts' also contains the Jupyter-Notebooks used to create the ablation prompts, the generic task template we used and a file 'keywords.txt' containing the keywords used to search for replication packages.

## Evaluation

The folder Evaluation contains the results of our analysis.
It contains the following:

* A subfolder 'analysis' containing the analysis scripts used to obtain our results from the probabilities output by Centaur and Llama.
* A subfolder 'answer\_amounts' containing a .csv file for each study, counting how often each response was given for each task.
* A subfolder 'full\_results' containing the probabilities output by Llama and Centaur in the next-token prediction for each ablation. We omit all tokens that are not the target token and have an assigned probability below 0.01.
* A subfolder 'illustrations' containing scripts used to create figures in our paper.
* A subfolder 'results' containing the results of our analysis.
* The file 'run\_Centaur.py' used to obtain the probabilities of Centaur and Llama for each study and ablation. Note that executing this file requires at least 140 GB of VRAM.

