
    public Integer firstAboveTreshold(int[] ngozwjAjjac, int threshold) {
        for (int i = 0; i < ngozwjAjjac.length; ++i) {
            int numberToTest = ngozwjAjjac[i];

            if (numberToTest > threshold)
                return numberToTest;
        }
        return null;
    }
