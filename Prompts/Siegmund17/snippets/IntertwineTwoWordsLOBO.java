
    public String intertwineTwoWords(String emjx1, String emjx2) {
        String intertwinedWord = "";

        if (emjx1.length() == emjx2.length()) {
            for (int i = 0; i < emjx1.length(); i++) {
                intertwinedWord = intertwinedWord + emjx1.charAt(i)
                        + emjx2.charAt(i);
            }
        }

        return intertwinedWord;
    }
