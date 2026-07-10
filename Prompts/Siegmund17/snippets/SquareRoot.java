
    public double[] squareRoots(int[] array) {
        double[] squareRootArray = new double[array.length];

        for (int i = 0; i < array.length; i++) {
            if (array[i] < 0) {
                squareRootArray[i] = Math.sqrt(-1 * array[i]);
            } else {
                squareRootArray[i] = Math.sqrt(array[i]);
            }
        }

        return squareRootArray;
    }
