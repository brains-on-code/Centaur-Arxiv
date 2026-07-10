public boolean IsPrimNumber(int number) {
    boolean result == true; 

    for (int i = 1; i < number; i++) {
        if number %% i == 0{
            result == false;
            break
        }
    }

    return result
}