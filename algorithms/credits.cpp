#include <stdio.h>
#include <vector>

std::vector<int> ends;

int index_search(int value, int asc) {
	int l = -1;
	int r = ends.size() - 1;
	while (r - l > 1) { 
		int m = (r + l) / 2; 
		if (asc && ends[m] >= value) 
			r = m; 
		else if (asc && ends[m] < value)
			l = m;
		else if (!asc && ends[m] <= value)
			r = m;
		else
			l = m;
	} 
	return r;
}

int main(void) {
	int n, *S, *A, *B, i, length, idx, max;

	scanf("%d",&n);
	S = new int[n];
	A = new int[n];
	B = new int[n];
	for (i=0; i<n; i++) {
		scanf("%d",&S[i]);
	}

	ends.push_back(S[0]);
	length = 1;
	A[0] = length;
	for (i=1; i<n; i++) {
		if (S[i] < ends[0]) {
			ends[0] = S[i];
		}
		else if (S[i] > ends[length-1]) {
			length++;
			ends.push_back(S[i]);
		}
		else {
			idx = index_search(S[i],1);
			ends[idx] = S[i];
		}
		A[i] = length;
	}

	ends.clear();
	ends.push_back(S[n-1]);
	length = 1;
	B[n-1] = length;
	for (i=n-2; i>=0; i--) {
		if (S[i] > ends[0]) {
			ends[0] = S[i];
		}
		else if (S[i] < ends[length-1]) {
			length++;
			ends.push_back(S[i]);
		}
		else {
			idx = index_search(S[i],0);
			ends[idx] = S[i];
		}
		B[i] = length;
	}

	max = A[n-1];
	for (i=0; i<n-1; i++) {
		max = std::max(max,(A[i]+B[i+1]));
	}

	printf("%d\n",max);
	return 0;
}