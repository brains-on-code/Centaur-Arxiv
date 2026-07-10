public float arrayAverage(int[] numbers) {
	int counter = 0;
	int sum = 0;

	while (counter < numbers.length) {
		sum = sum + numbers[counter];
		counter = counter + 1;
	}

	float average = sum / (float) counter;
	return average;
}