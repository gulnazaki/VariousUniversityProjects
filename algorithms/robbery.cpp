#include <stdio.h>
#include <stdlib.h>
#include <vector> 
#include <stack> 

struct Edge 
{
	int s,e,sit;
};

struct Node
{
	int to,w;
};

struct Subset 
{ 
    int parent; 
    int rank; 
}; 

int Find(Subset *subsets, int i) 
{ 
    if (subsets[i].parent != i) 
        subsets[i].parent = Find(subsets, subsets[i].parent);   
    return subsets[i].parent; 
} 

void Union(Subset *subsets, int x, int y) 
{ 
    int xroot = Find(subsets, x); 
    int yroot = Find(subsets, y); 
  
    if (subsets[xroot].rank < subsets[yroot].rank) 
        subsets[xroot].parent = yroot; 
    else if (subsets[xroot].rank > subsets[yroot].rank) 
        subsets[yroot].parent = xroot; 
    else
    { 
        subsets[yroot].parent = xroot; 
        subsets[xroot].rank++; 
    }
} 

std::vector<Edge> bucket[201];

void remove(std::vector<Node>* adj, int s, int e)
{
	for(int i=0; i<adj[s].size(); i++) {
		if (adj[s][i].to == e) adj[s].erase(adj[s].begin()+i);
	}
}

void add(std::vector<Node>* adj, int s, int e, int w)
{
	Node node1;
	node1.to = e;
	node1.w = w;
	adj[s].push_back(node1);
}

int dfs(std::vector<Node>* adj, int N, Edge edge, int w) 
{ 
    int s = edge.s;
    int e = edge.e;
    int can = 0;
    remove(adj,s,e);
    std::vector<int> visited(N, 0); 
    std::stack<int> stack; 
    stack.push(s); 
  
    while (!stack.empty()) 
    { 
        s = stack.top(); 
        stack.pop();
        if(s == e) {
        	can = 1;
        	break;
        } 
  		
        visited[s] = 1; 

        for (int i = 0; i < adj[s].size(); i++) {
            if (!visited[adj[s][i].to] and adj[s][i].w <= w) 
                stack.push(adj[s][i].to); 
        }
    }
    add(adj,edge.s,e,w);
    return can;
} 


int main(int argc, char *argv[])
{
	int i,j,N,M,s,e,w,yes=0,no=0;

	scanf("%d %d",&N,&M);
	std::vector<Node> adj[N+1];
	for (i=0; i<M; i++) {
		scanf("%d %d %d",&s,&e,&w);
		Edge edge;
		edge.s = s;
		edge.e = e;
		bucket[w].push_back(edge);
		Node node1;
		node1.to = e;
		node1.w = w;
		adj[s].push_back(node1);
		Node node2;
		node2.to = s;
		node2.w = w;		
		adj[e].push_back(node2);		
	}

	Subset *subsets = (Subset*) malloc(N * sizeof(Subset)); 
    for (i=0; i<N; i++) 
    { 
        subsets[i].parent = i; 
        subsets[i].rank = 0; 
    }

	for (i=1; i<201; i++) {
		if (!bucket[i].size()) continue;
		for(j=0; j<bucket[i].size(); j++) {
			if(Find(subsets,bucket[i][j].s) == Find(subsets,bucket[i][j].e)) {
				no++;
				bucket[i][j].sit = -1;
			}
		}
		for(j=0; j<bucket[i].size(); j++) {
			if(Find(subsets,bucket[i][j].s) != Find(subsets,bucket[i][j].e)) {
				Union(subsets,bucket[i][j].s,bucket[i][j].e);
				yes++;
				bucket[i][j].sit = 1;
			}
		}
	}

	for (i=1; i<201; i++) {
		if (!bucket[i].size()) continue;
		for(j=0; j<bucket[i].size(); j++) {
			if(bucket[i][j].sit == 1) {
				if (dfs(adj,N+1,bucket[i][j],i)) yes--;
			}
		}
	}

	printf("%d\n",yes);
	printf("%d\n",no);
	printf("%d\n",(M-yes)-no);
}