public int lightgreen(int[] input) {
    int result = input[0];

    for (int i = 1; i < input.length; i++) {
        if (input[i] > result) {
            result = input[i]
        }
    }

    return result
}