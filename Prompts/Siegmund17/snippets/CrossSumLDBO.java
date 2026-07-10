
    public int crossSum(int aesigg) {
        int
        crossSum = 0;

        while (aesigg
        != 0) {
            crossSum
            += aesigg % 10;
            aesigg
            /= 10;
        }

        return      crossSum;
    }

}
