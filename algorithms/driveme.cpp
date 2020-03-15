#include <stdio.h>
#include <queue>
#include <vector>
#include <climits>
#include <tuple>
#include <list>
#include <stdlib.h>
using namespace std;

list<tuple<int,int>> adj[100][2];

int dist[100][100][11];

int min_of(int s,int t,int p) {
	int d, min;

	min = INT_MAX;
	for (d=0; d<=p; d++) {
		if (min > dist[s][t][d]) min = dist[s][t][d];
	}
	return min;
}

void dijkstra(int N, int K) {
	int i, j, k_, w_, d, newd, distance, sign;
	list<tuple<int,int>>::iterator k; 


	for (i=0; i<N; i++) {
		for (j=0; j<N; j++) {
			for (d=0; d<=K; d++) {
				if (i==j) dist[i][j][d] = 0;
				else dist[i][j][d] = INT_MAX;
			}
		}
	}

	for (i=0; i<N; i++) {
		priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<tuple<int,int,int>>> Q;
		Q.push(make_tuple(0,i,0)); 
		while (!Q.empty()) {
			distance = get<0>(Q.top());
			j = get<1>(Q.top());
			d = get<2>(Q.top());
			Q.pop();
		
			for (sign = 0; sign<=1; sign++) {
				for (k = adj[j][sign].begin(); k != adj[j][sign].end(); k++)  {
				    k_ = get<0>(*k);
				    w_ = get<1>(*k);
				    newd = d + sign;
				    if (newd <= K) {
				      	if (dist[i][k_][newd] > distance + w_) {
	    					dist[i][k_][newd] = distance + w_;
	    					Q.push(make_tuple(dist[i][k_][newd],k_,newd));
	    				}
				    }
				}
			}
		}
	}
}


int main(void) {
	int N, M, K, Q;
	int i, s, t, w, p;
	std::queue<int> results;

	scanf("%d %d %d %d",&N, &M, &K, &Q);
	for (i=0; i<M; i++) {
		scanf("%d %d %d",&s, &t, &w);
		adj[s-1][0].push_back(make_tuple(t-1,w));
		adj[t-1][1].push_back(make_tuple(s-1,w));
	}

	dijkstra(N,K);

	for (i=0; i<Q; i++) {
		scanf("%d %d %d",&s, &t, &p);
		results.push(min_of(s-1,t-1,p));
	}

	for (i=0; i<Q; i++) {
		w = results.front();
		results.pop();
		if (w==INT_MAX) {
			printf("IMPOSSIBLE\n");
		}
		else {
			printf("%d\n",w);
		}
	}
	return 0;
}