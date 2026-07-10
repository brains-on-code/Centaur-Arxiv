
    public String reverseWord(String qwko) {
        String reversedWord
        = "";

        for (
                int i = qwko.length()
                - 1;
                i >= 0;
                i--) {
            reversedWord
            +=
                    qwko.charAt(i);
        }

        return
        reversedWord;
    }
