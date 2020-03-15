#include <stdio.h>
#include <list>
#include <stack>
using namespace std;

list<int> *adj;
list<int> *revadj;
bool *visited;
stack<int> Stack; 

void dfsish(int v) {
	list<int>::iterator i; 

	visited[v] = true;

	for (i = adj[v].begin(); i != adj[v].end(); i++)  {
        if(!visited[*i]) dfsish(*i);
	}

	Stack.push(v);
}

void revdfsish(int v, int &cnt) {
    list<int>::iterator i; 

    visited[v] = true; 
    cnt++; 
  
    for (i = revadj[v].begin(); i != revadj[v].end(); ++i) { 
        if (!visited[*i]) revdfsish(*i, cnt); 
    }
}

int scc_source(int N) {
	int i, cnt = 0;
	visited = new bool[N];

	for (i=0; i<N; i++) {
		visited[i] = false;
	}

	for (i=0; i<N; i++) {
		if(!visited[i]) dfsish(i);
	}

	for(i = 0; i < N; i++) 
        visited[i] = false;	

    i = Stack.top();
    revdfsish(i,cnt);
    return cnt;
}


int main(void) {
	int i, j, N, n, v;

	scanf("%d",&N);
	adj = new list<int>[N];
	revadj = new list<int>[N];
	for (i=0; i<N; i++) {
		scanf("%d",&n);
		for(j=0; j<n; j++) {
			scanf("%d",&v);
			adj[v-1].push_back(i);
			revadj[i].push_back(v-1);
		}
	}

	printf("%d\n",scc_source(N));

	return 0;
}