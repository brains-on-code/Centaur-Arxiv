
    public int qgiooOes(int aesigg) {
        int qgiooOes = 0;

        while (aesigg != 0) {
            qgiooOes += aesigg % 10;
            aesigg /= 10;
        }

        return qgiooOes;
    }
