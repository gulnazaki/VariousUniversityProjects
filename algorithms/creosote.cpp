#include <stdio.h>  
#include <vector>

std::vector <long long int> gr, co;

int s, curr = 0;

long long int query(long long int x) {
    if (curr >= gr.size())
        curr = gr.size() - 1;

    while (curr < gr.size() - 1 && (gr[curr] * x + co[curr] < gr[curr + 1] * x + co[curr + 1]))
        curr++;
    return gr[curr] * x + co[curr];
}

void update(long long int gnew, long long int cnew) {
    while (gr.size() >= 2) {
        int s = gr.size() - 1;
        if ((gr[s-1] - gr[s]) * (co[s-1] - cnew) > (co[s] - co[s-1]) * (gnew - gr[s-1])) {
            gr.pop_back();
            co.pop_back();
        }
        else break;
    }
    gr.push_back(gnew);
    co.push_back(cnew);
}

int main(void) {
    int n, a, b, c, i;
    long long int *sum, *dp, asq, j;
    scanf("%d", &n);
    sum = new long long int[n];
    dp = new long long int[n];
    scanf("%d %d %d", &a, &b, &c);
    scanf("%lld",sum);
    for (i = 1; i < n; i++) {
       scanf("%lld", &j);
       sum[i] = sum[i-1] + j;
    }
    asq = a * sum[0] * sum[0];
    dp[0] = asq + (b * sum[0]) + c;
    gr.push_back(-2 * a * sum[0]);
    co.push_back(dp[0] + asq - b * sum[0]);
    
    for (i = 1; i < n; i++) {
        asq = a * sum[i] * sum[i];
        dp[i] = asq + b * sum[i] + c;
        j = query(sum[i]);
        if (j >= 0) {
            dp[i] += j;
        }

        update(-2 * a * sum[i], dp[i] + asq - (b * sum[i]));
    }
    
    printf("%lld\n", dp[n-1]);

    gr.clear();
    co.clear();
    delete[] sum;
    delete[] dp;
    return 0;
}
