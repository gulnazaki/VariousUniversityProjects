#include <stdio.h>
#define MOD 1000000103

int N,M,K,X;
int path[180][180][101], start[180][180], end[180][180], cnt[180][180];

int max(int a, int b) {
	if (a>b) return a;
	else return b;
}

void num_to_xy(int n,int &x,int &y) {
	x = n/M;
	y = n%M;
}

void zero(int* A, int cnt) {
	for (int i=0; i<=cnt; i++) {
		A[i] = 0;
	}
}

void add_cnt(int* A, int* B, int cnt1, int cnt2) {
	for (int i=0; i<=cnt2; i++) {
		A[i] += B[i];
		A[i] %= MOD;
	}
	for (int i=cnt2+1; i<=cnt1; i++) {
		A[i] += B[cnt2];
		A[i] %= MOD;
	}
}

int update_end(int* e, int* s, int ecnt, int scnt) {
	int newcnt;
	if (ecnt >= scnt) {
		newcnt = ecnt;
		for (int i=1; i<=scnt; i++) {
			e[i] += s[i-1];
			e[i] %= MOD;
		}
		for (int i=scnt+1; i<=ecnt; i++) {
			e[i] += s[scnt-1];
			e[i] %= MOD;
		}	
	}
	else {
		newcnt = scnt;
		int last = e[ecnt];
		for (int i=1; i<=ecnt; i++) {
			e[i] += s[i-1];
			e[i] %= MOD;
		}
		for (int i=ecnt+1; i<=scnt; i++) {
			e[i] = last + s[i-1];
			e[i] %= MOD;
		}
	}	
	return newcnt;
}

void fill(int x,int y) {
	if (x == N-1 and y == M-1) return;

	int counter = 0;
	if (x != N-1 and !start[x+1][y]) counter = max(counter,cnt[x+1][y]);
	if (y != M-1 and !start[x][y+1]) counter = max(counter,cnt[x][y+1]);
	cnt[x][y] = counter;
 	zero(path[x][y],counter);
	if (x != N-1 and !start[x+1][y]) add_cnt(path[x][y],path[x+1][y],counter,cnt[x+1][y]);
	if (y != M-1 and !start[x][y+1]) add_cnt(path[x][y],path[x][y+1],counter,cnt[x][y+1]);

	if (end[x][y]) {
		int a, b;
		num_to_xy(end[x][y],a,b);
		if(!path[a][b][cnt[a][b]]) return;
		cnt[x][y] = update_end(path[x][y],path[a][b],cnt[x][y],cnt[a][b]+1);
	}
}

int main(int argc, char *argv[])
{
	int i,j,k,l,s,e,x,y;

	scanf("%d %d %d %d",&N,&M,&K,&X);
	for(i=0; i<N; i++) {
		for(j=0; j<M; j++) {
			start[i][j] = end[i][j] = 0;
		}
	}
	for (i=0; i<K; i++) {
		scanf("%d %d",&s,&e);
		num_to_xy(s,x,y);
		start[x][y] = e;
		num_to_xy(e,x,y);
		end[x][y] = s;
	}

	path[N-1][M-1][0] = 1;
	cnt[N-1][M-1] = 0;

	k = N-1;
	l = M-1;
	for(i=N-1; i>=0; i--) {
		for(j=l; j>=0; j--) {
			fill(i,j);
		}
		for(j=k-1; j>=0; j--) {
			if(l>=0) fill(j,l);
		}
		l--;
		k--;
	}

	x = X > cnt[0][0] ? cnt[0][0] : X;
	printf("%d\n",path[0][0][x]);
}