public int buycp(int hawc, int cfbuncd) {
	int product = hawc;
	if (cfbuncd == 0)
		return 1;

	for (int i = 1; i < cfbuncd; i++) {
		product = product * hawc;
	}

	return product;
}