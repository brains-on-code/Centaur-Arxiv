public int crossSum(int number) {
    int crossSum = 0; 

    while (number != 0) {
        crossSum += number % 10; 
        number /= 10; 
    }

    return crossSum;
}