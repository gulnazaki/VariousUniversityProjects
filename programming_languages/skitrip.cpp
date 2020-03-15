#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace std;


/* Skitrip */
/* Melistas Thomas */
/* Patris Nikolas */


int *create_height_table(char *file, int &entries) {
  FILE *fp;
  int *table;

  // open file; error if text file doesn't exist or has a different name
  if ((fp = fopen(file,"r")) == NULL) {
    printf("File doesn't exist or has different name.\nEnter filename as command line argument\n");
    exit(1);
  }
  // reading first line; error if there is no entries number
  if (fscanf(fp, "%d\n", &entries) != 1) {
    printf("Wrong file format (check first line)\n");
    exit(2);
  }
  // creating table
  table = new int[entries];
  // reads first (given in the first line) entries from second line and puts heights in table
  for (int i=0; i<entries; i++) {
    if (fscanf(fp, "%d", &table[i]) != 1) {
      printf("Wrong file format (fewer entries than promised)\n");
      exit(3);
    }
  }
  // return pointer to the height table
  return table;
}

vector<int> create_vector(int *table, int entries, char order) {
  vector<int> vec;
  int previous;

  // creating the L vector
  if (order == '>') {
    previous = 1000000001; // initializing higher than highest
    // starts from first element and stores all ascending elements
    for (int i=0; i<entries; i++) {
      if (table[i] < previous) {
        vec.push_back(i);
        previous = table[i];
      }
    }
  }
  // creating the R vector
  else {
    previous = 0;        // initialize lower than lowest
    // starts from lsst element and stores all descending elements
    for (int i=entries-1; i>=0; i--) {
      if (table[i] > previous) {
        vec.push_back(i);
        previous = table[i];
      }
    }
  }
  // returning created vector
  return vec;
}

int maximum_distance(vector<int> L, vector<int> R, int *table) {
  int distance = 0, max_distance = 0;

  // we use a reverse iterator for R
  vector<int>::reverse_iterator it2 = R.rbegin();
  // we find the max_distance for every element on L
  for (vector<int>::iterator it1 = L.begin() ; it1 != L.end() ; ++it1) {
    // while height of R element is bigger or equal to that of L
    while (table[*it2] >= table[*it1] && it2 != R.rend()) {
      distance = *it2 - *it1;
      ++it2;
    }
    // keeps the maximum of all distances
    if (distance > max_distance) max_distance = distance;
  }
  return max_distance;
}

int main (int argc, char* argv[]) {
  int *table, entries;
  vector<int> L, R;

  table = create_height_table(argv[1],entries);
  L = create_vector(table,entries,'>');
  R = create_vector(table,entries,'<');
  printf("%d\n", maximum_distance(L,R,table));
  delete table;
  return 0;
}
