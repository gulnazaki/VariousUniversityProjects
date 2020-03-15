#include <stdio.h>
#include <float.h>

float time_to(int t, int u, int L) {
	float time = (float) t;
	time += (float) L / (float) u;
	return time;
}

int main(int argc, char *argv[])
{
	long i, N, L, K, k, *ta, *ua, *tb, *ub, *ka, *kb, left_par[3], right_par[3], max_u;
	float m, min_ta[3], min_tb[3], time_a, time_b, lmr[3];

	scanf("%ld %ld %ld",&N,&L,&K);
	ta = new long[N];
	ua = new long[N];
	tb = new long[N];
	ub = new long[N];
	ka = new long[K];
	kb = new long[K];
	for (i=0; i<N; i++) {
		scanf("%ld %ld",&ta[i],&ua[i]);
	}
	for (i=0; i<N; i++) {
		scanf("%ld %ld",&tb[i],&ub[i]);
	}

	for (k=0; k<K; k++) {
		lmr[0] = 0.0;
		lmr[2] = (float) L;
		min_ta[0] = (float) ta[0];
		left_par[0] = 0;
		min_tb[2] = (float) tb[2];
		right_par[2] = 0;
		min_ta[2] = min_tb[0] = FLT_MAX;
		max_u = 0;
		for (i=0; i<N; i++) {
			if (ua[i] > max_u) max_u = ua[i];
			else continue;
			if (ta[i] > min_ta[2]) break;
			time_a = time_to(ta[i],ua[i],lmr[2]);
			if (time_a < min_ta[2]) {
				min_ta[2] = time_a;
				left_par[2] = i;
			}
		}
		max_u = 0;
		for (i=0; i<N; i++) {
			if (ub[i] > max_u) max_u = ub[i];
			else continue;
			if (tb[i] > min_tb[0]) break;
			time_b = time_to(tb[i],ub[i],lmr[2]);
			if (time_b < min_tb[0]) {
				min_tb[0] = time_b;
				right_par[0] = i;
			}
		}

		if (left_par[0] == left_par[2] and right_par[0] == right_par[2]) {
			ua[left_par[0]] = ub[right_par[0]] = 0;
			ka[k] = left_par[0];
			kb[k] = right_par[0];
			continue;
		}

		while(1) {
			lmr[1] = (lmr[0]+lmr[2]) / 2;
			min_ta[1] = FLT_MAX;
			max_u = 0;
			for (i=0; i<N; i++) {
				if (ua[i] > max_u) max_u = ua[i];
				else continue;
				if (ta[i] > min_ta[1]) break;
				time_a = time_to(ta[i],ua[i],lmr[1]);
				if (time_a < min_ta[1]) {
					min_ta[1] = time_a;
					left_par[1] = i;
				}
			}
			min_tb[1] = FLT_MAX;
			max_u = 0;
			for (i=0; i<N; i++) {
				if (ub[i] > max_u) max_u = ub[i];
				else continue;
				if (tb[i] > min_tb[1]) break;
				time_b = time_to(tb[i],ub[i],L - lmr[1]);
				if (time_b < min_tb[1]) {
					min_tb[1] = time_b;
					right_par[1] = i;
				}
			}

			if (left_par[0] == left_par[2] and right_par[0] == right_par[2]) {
				ua[left_par[0]] = ub[right_par[0]] = 0;
				ka[k] = left_par[0];
				kb[k] = right_par[0];
				break;
			}
			else if (min_ta[1] < min_tb[1]) {
				lmr[0] = lmr[1];
				min_ta[0] = min_ta[1];
				left_par[0] = left_par[1];
				min_tb[0] = min_tb[1];
				right_par[0] = right_par[1];
			}
			else {
				lmr[2] = lmr[1];
				min_ta[2] = min_ta[1];
				left_par[2] = left_par[1];
				min_tb[2] = min_tb[1];
				right_par[2] = right_par[1];
			}
		}
	}


	for (i=0; i<K; i++) {
		printf("%ld %ld\n",ka[i]+1,kb[i]+1);
	}

	delete[] ta;
	delete[] ua;
	delete[] tb;
	delete[] ub;
	delete[] ka;
	delete[] kb;
	return 0;
}