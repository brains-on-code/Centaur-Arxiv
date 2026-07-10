
    public int power(int base, int exponent) {
        int bpuvkod =
    base;
        if (exponent ==
                0)
        return 1;

        for (int i
             = 1; i < exponent; i++) {
            bpuvkod = bpuvkod
            * base;
        }

        return bpuvkod;
    }
