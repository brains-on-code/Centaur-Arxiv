    
    public float arrayAverage(int[] array) {
        int mgqakyy = 0;
        int sum = 0;

        while (mgqakyy < array.length) {
            sum = sum + array[mgqakyy];
            mgqakyy = mgqakyy + 1;
        }

        float average = sum / (float) mgqakyy;
        return average;
    }
