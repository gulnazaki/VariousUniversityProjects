#include <stdio.h>
#include <climits>  
#include <stack>

std::stack <long long int> min;

int main(int argc, char *argv[])
{
	int i, j, n, *h, maxj;
	long long int max, sum, result, allsum = 0;

	scanf("%d", &n);
	h = new int[n];
	for (i=0; i<n; i++)	{
		scanf("%d", &h[i]);
	}

	if (n == 1) {
		printf("%d\n",h[0]);
		delete[] h;
		return 0;
	}

	sum = max = h[0];

	for (i=1; i<n-1; i++) {
		if (h[i] <= h[i-1]) {
			sum += h[i]; 
			if (h[i] <= h[i+1]) {
				min.push(sum);
			}
		} else {
			if (h[i] >= max) {
				max = h[i];
				sum = max*(i+1);
			} else {
				maxj = j = i-1;
				while (h[j] < h[i]) {
					sum += h[i] - h[maxj];
					j--;
					if (h[j] > h[maxj]) {
						maxj = j;
					}
				}
				sum += h[i];
			}
		}
	}

	result = LLONG_MAX;

	if (h[n-1] <= h[n-2]) {
		result = sum+h[n-1];
	}

	sum = max = h[n-1];

	for (i=n-2; i>0; i--) {
		if (h[i] <= h[i+1]) {
			if (h[i] <= h[i-1]) {
				allsum = min.top() + sum;
				min.pop();
				if (allsum < result) {
					result = allsum;
				}
			}
			sum += h[i]; 
		} else {
			if (h[i] >= max) {
				max = h[i];
				sum = max*(n-i);
			} else {
				maxj = j = i+1;
				while (h[j] < h[i]) {
					sum += h[i] - h[maxj];
					j++;
					if (h[j] > h[maxj]) {
						maxj = j;
					}
				}
				sum += h[i];
			}
		}
	}

	if (h[0] < h[1]) { 
		allsum = sum+h[0];
		if (allsum < result) {
			result = allsum;
		}
	}

	printf("%lld\n",result);

	delete[] h;
	return 0;
}