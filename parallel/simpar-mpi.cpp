//--------------------------------------------------------------------------------------//
//-------------------------------------- INCLUDES --------------------------------------//
//--------------------------------------------------------------------------------------//
#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <unordered_map> 
#include <set> 
#include <vector>
#include <iterator>
#include <math.h>
#include <mpi.h>
//#include <omp.h>
    
//--------------------------------------------------------------------------------------//
//------------------------------------- NAMESPACES -------------------------------------//
//--------------------------------------------------------------------------------------//
using namespace std;

//--------------------------------------------------------------------------------------//
//--------------------------------------- MARCOS ---------------------------------------//
//--------------------------------------------------------------------------------------//
#define RND0_1 ((double) random() / ((long long)1<<31))
#define G 6.67408e-11
#define EPSLON 0.0005
#define N_NEIGHBORS 9

/*
#define ROW_START(i,n,r,c) (((i)/(c)) * ((n) / double((r))))
#define ROW_END(i,n,r,c) (ROW_START((i)+(c),(n),(r),(c)) -1)
#define ROW_SIZE(i,n,r,c) ((ROW_END((i),(n),(r),(c))+1) - ROW_START((i),(n),(r),(c)))
#define COL_START(i,n,r,c) (int((i) * ((n) / double((c)))) % (n))
#define COL_END(i,n,r,c) (int(((i)+1) * ((n) / double((c))) - 1) % (n))
#define COL_SIZE(i,n,r,c) ((COL_END((i),(n),(r),(c))+1) - COL_START((i),(n),(r),(c)))
*/

//--------------------------------------------------------------------------------------//
//-------------------------------------- STRUCTS ---------------------------------------//
//--------------------------------------------------------------------------------------//
struct particle_t {
    double x, y;    //Position
    double vx, vy;  //Velocity
    double m;       //Mass
    double c;    //Cell
    double id;
    double present;
};

struct cell_t {
    double x, y;    //Position
    double mx, my;  //Auxiliary (mass times position)
    double m;       //Total mass
};

//--------------------------------------------------------------------------------------//
//------------------------------------- FUNCTIONS --------------------------------------//
//--------------------------------------------------------------------------------------//
long cell_index(double x, double y, long n){
    long cell_x = (x == 1)?0:x*n;
    long cell_y = (y == 1)?0:y*n;
    return cell_x + cell_y * n;
}

int row_start(int p, int n, int r, int c) {
    return (p / c) * (n / double(r));
}

int row_end(int p, int n, int r, int c) {
    return row_start(p+c, n, r, c)-1;
}

int col_start(int p, int n, int r, int c) {
    return int(p * (n / double(c))) % n;
}

int col_end(int p, int n, int r, int c) {
    return int((p+1) * (n / double(c))-1) % n;
}

vector<int> get_frontier_cells(int r, int c, int cell_height, int cell_width, vector<int> process_cells) {
    vector<int> frontier = vector<int>();
    //Left superior diagonal
    if (r==-1 && c==-1) frontier.push_back(process_cells[0]);
    //Right superior diagonal
    else if (r==-1 && c==1) frontier.push_back(process_cells[cell_width-1]);
    //Left inferior diagonal
    else if (r==1 && c==-1) frontier.push_back(process_cells[cell_width*(cell_height-1)]);
    //Right inferior diagonal
    else if (r==1 && c==1) frontier.push_back(process_cells[cell_width*(cell_height-1)+cell_width-1]);
    //Up
    else if (r==-1 && c==0) {
        for (int i = 0; i < cell_width; i++) {
            frontier.push_back(process_cells[i]);
        }
    }
    //Down
    else if (r==1 && c==0) {
        for (int i = cell_width*(cell_height-1); i < cell_width*cell_height; i++) {
            frontier.push_back(process_cells[i]);
        }
    }
    //Left
    else if (r==0 && c==-1) {
        for (int i = 0; i < cell_width*cell_height; i+=cell_width) {
            frontier.push_back(process_cells[i]);
        }
    }
    //Right
    else if (r==0 && c==1) {
        for (int i = cell_width-1; i < cell_width*cell_height+(cell_width-1); i+=cell_width) {
            frontier.push_back(process_cells[i]);
        }
    }
    return frontier;
}

void init_particles(int process, long seed, long ncside, long long n_part, vector<particle_t> &par, unordered_map<int, int> process_map) {
    srandom(seed);

    for (long long i = 0; i < n_part; i++) {
        particle_t p = {
            RND0_1, RND0_1,
            RND0_1 / ncside / 10.0,
            RND0_1 / ncside / 10.0,
            RND0_1 * ncside / (G * 1e6 * n_part),
            0,
            double(i),
            1
        };
        p.c = cell_index(p.x, p.y, ncside);
        if (process == process_map[p.c]) par.push_back(p);
    }
}

void init_process_cells(int process, int n_processes, long ncside, long &max_cell_buffer, int rows, int cols, vector<int> process_cells[], unordered_map<int, int> &process_map) {
    for (int i = 0; i < n_processes; i++) {
        int r_start = row_start(i,ncside,rows,cols);             //Start of the cell rows
        int r_end   = row_end(i,ncside,rows,cols);               //End of the cell rows
        int c_start = col_start(i,ncside,rows,cols);             //Start of the cell columns
        int c_end   = col_end(i,ncside,rows,cols);               //End of the cell rows

        process_cells[i] = vector<int>();

        for (int r = r_start; r <= r_end; r++) {                            //Go through the rows of cells this process will handle
            for (int c = c_start; c <= c_end; c++) {                        //Go through the columns of cells this process will handle
                long cell_index = c+r*ncside;
                process_cells[i].push_back(cell_index);                     //Add the cell to the process' cells
                process_map[cell_index] = i;
            }       
        }
        if (process_cells[i].size() > max_cell_buffer) max_cell_buffer = process_cells[i].size();
    }
}

void update_particles(long *neighbors, cell_t *grid, vector<particle_t> &par, int ncside){
    for(long long p = 0; p < par.size(); p++){
        if(par[p].present < 0) continue;
        double ax = 0, ay = 0;

        for(int n = 0; n < N_NEIGHBORS; n++){
            long c = neighbors[int(par[p].c * N_NEIGHBORS) + n]; //Cell index of current neighbor

            double dx = grid[c].x - par[p].x;
            double dy = grid[c].y - par[p].y;

            double d  = sqrt(dx*dx + dy*dy);
            
            if(d >= EPSLON){
                double f = (G * grid[c].m) / (d*d*d); //Optimized calculations by simplification of the formula
                ax += f * dx;
                ay += f * dy;
            }
        }
        par[p].x  += par[p].vx + 0.5*ax;     //Calculate X Position
        par[p].y  += par[p].vy + 0.5*ay;     //Calculate Y Position

        if     (par[p].x > 1) par[p].x -= 1; //Wrap Around X > 1
        else if(par[p].x < 0) par[p].x += 1; //Wrap Around X < 0
        if     (par[p].y > 1) par[p].y -= 1; //Wrap Around Y > 1
        else if(par[p].y < 0) par[p].y += 1; //Wrap Around Y < 0

        par[p].vx += ax;                     //Calculate X Velocity
        par[p].vy += ay;                     //Calculate Y Velocity

        par[p].c = cell_index(par[p].x, par[p].y, ncside);
    }
    MPI_Barrier(MPI_COMM_WORLD);
}


void update_cmass(cell_t* grid, vector<particle_t> &par, vector<int> &cells, long ncside){
    for (auto c = cells.begin(); c != cells.end(); c++) {
        grid[(*c)].mx = 0;                      //Reset mx
        grid[(*c)].my = 0;                      //Reset my
        grid[(*c)].m  = 0;                      //Reset total mass
    }
    for (long long p = 0; p < par.size(); p++) {
        if (par[p].present < 0) continue;
        long c = par[p].c;

        grid[c].mx += par[p].m * par[p].x;   //Sum of mass times x
        grid[c].my += par[p].m * par[p].y;   //Sum of mass times y
        grid[c].m  += par[p].m;              //M, sum of all particles' masses in the cell
    }
    for(auto c = cells.begin(); c != cells.end(); c++) {
        if (grid[(*c)].m != 0) {
            grid[(*c)].x = grid[(*c)].mx / grid[(*c)].m; //Divide by total mass to obtain x
            grid[(*c)].y = grid[(*c)].my / grid[(*c)].m; //Divide by total mass to obtain y
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
}

void init_comm_map(int process, int rows, int cols, int ncside, unordered_map<int, set<int>> &comm_map, vector<int> process_cells[]) {
    int cell_height = row_end(process,ncside,rows,cols)+1 - row_start(process,ncside,rows,cols);
    int cell_width  = col_end(process,ncside,rows,cols)+1 - col_start(process,ncside,rows,cols);

    int r_start = -1+(rows==1);                                  
    int r_end   = 1-(rows==1);                                                        //Get the maximum neighbor row
    int c_start = -1+(cols==1);
    int c_end   = 1-(cols==1);                                                        //Get the maximum neighbor column
    
    for (int r = r_start; r <= r_end; r++) {
        for (int c = c_start; c <= c_end; c++) {
            if (r != 0 || c != 0) {
                int x = (cols + ((process + c)%cols)) % cols;                           //Get the neighbor x position in the process grid [0,cols]
                int y = (rows + ((int(process/cols) + r)%rows)) %rows;                  //Get the neighbor y position in the process grid [0,rows]

                vector<int> frontier = get_frontier_cells(r, c, cell_height, cell_width, process_cells[process]); //
                comm_map[x+y*cols].insert(frontier.begin(), frontier.end());
            }
        }
    }
}

void init_neighbors(long *neighbors, long ncside){
    for(long c = 0; c < ncside*ncside; c++) {
        int idx = 0;
        for(int h = -1; h <= 1; h++) {
            for(int w = -1; w <= 1; w++) {
                long x = (ncside + ((c + w)%ncside)) % ncside;
                long y = (ncside + ((long(c/ncside) + h)%ncside)) % ncside;
                neighbors[c*N_NEIGHBORS+(idx++)] = x+y*ncside;
            }
        }
    }
}

void get_cmasses(int process, int ncside, long max_cell_buffer, unordered_map<int, set<int>> comm_map, cell_t* grid, MPI_Datatype cell_type) {
    MPI_Request requests[comm_map.size()];
    MPI_Request requests2[comm_map.size()];
    MPI_Status  statuses[comm_map.size()];
    MPI_Status  statuses2[comm_map.size()];

    vector<vector<cell_t>> recv = vector<vector<cell_t>>(comm_map.size());

    int req = 0;
    for (auto comm : comm_map) {
        vector<cell_t> send = vector<cell_t>(comm.second.size());
        recv[req] = vector<cell_t>(max_cell_buffer);

        int i = 0;
        for (auto c = comm.second.begin(); c != comm.second.end(); c++) {
            send[i++] = grid[(*c)];
        }

        MPI_Irecv(&recv[req].front(), max_cell_buffer, cell_type, comm.first, 0, MPI_COMM_WORLD, &requests[req]);
        MPI_Isend(&send.front(), send.size(), cell_type, comm.first, 0, MPI_COMM_WORLD, &requests2[req]);
        req++;
    }
    MPI_Waitall(comm_map.size(), requests, statuses);
    MPI_Waitall(comm_map.size(), requests2, statuses2);

    int i = 0;
    for (auto comm : comm_map) {
        int count;
        MPI_Get_count(&statuses[i], cell_type, &count);

        int j = 0;
        for (auto c = comm.second.begin(); c != comm.second.end(); c++) {
            grid[(*c)] = recv[i][j++];
            if (j == count) break;
        }
        i++;
    }
    MPI_Barrier(MPI_COMM_WORLD);
}

void get_particles(int process, long max_par_buffer, unordered_map<int, int> process_map, unordered_map<int, set<int>> comm_map, vector<particle_t> &par, MPI_Datatype par_type) {

    unordered_map<int, vector<particle_t>> par_send;

    for (auto comm : comm_map) {
        par_send[comm.first] = vector<particle_t>();
    }

    for (int i = par.size()-1; i >= 0; i--) {
        if (par[i].present < 0) continue;
        int destination = process_map[par[i].c];
        if (destination != process) {
            par_send[destination].push_back(par[i]);
            par[i].present = -1;
        }
    }

    MPI_Request requests[par_send.size()];
    MPI_Request requests2[par_send.size()];
    MPI_Status  statuses[par_send.size()];
    MPI_Status  statuses2[par_send.size()];

    vector<vector<particle_t>> recv = vector<vector<particle_t>>(par_send.size());

    int req = 0;
    for (auto p : par_send) {
        int i = p.first;

        recv[req] = vector<particle_t>(max_par_buffer);

        MPI_Irecv(&recv[req].front(), max_par_buffer, par_type, i, 1, MPI_COMM_WORLD, &requests[req]);
        MPI_Isend(&par_send[i].front(), par_send[i].size(), par_type, i, 1, MPI_COMM_WORLD, &requests2[req]);
        req++;
    }
    MPI_Waitall(par_send.size(), requests, statuses);
    MPI_Waitall(par_send.size(), requests2, statuses2);

    for (int i = 0; i < req; i++) {
        int count;
        MPI_Get_count(&statuses[i], par_type, &count);
        par.insert(par.end(), recv[i].begin(), recv[i].begin()+count);
    }

    MPI_Barrier(MPI_COMM_WORLD);
}

void print_first(vector<particle_t> par) {
    for (int i = 0; i < par.size(); i++) {
        if (par[i].id == 0 and par[i].present > 0) {
            printf("%.2f %.2f\n", par[i].x, par[i].y);
            break;
        }
    }
    MPI_Barrier(MPI_COMM_WORLD);
}

void print_overall(int process, vector<particle_t> par) {
    double process_cmass[3] = {0, 0, 0};
    double overall_cmass[3] = {0, 0, 0};

    for (int i = 0; i < par.size(); i++) {
        if (par[i].present < 0) continue;
        process_cmass[0] += par[i].m * par[i].x;
        process_cmass[1] += par[i].m * par[i].y;
        process_cmass[2] += par[i].m;
    }

    MPI_Reduce(process_cmass, overall_cmass, 3, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);

    if (process == 0) {
        printf("%.2f %.2f\n", overall_cmass[0]/overall_cmass[2], overall_cmass[1]/overall_cmass[2]);
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);                                                     //Initialize MPI

    MPI_Datatype par_type, cell_type;                                           //MPI Datatype for particles 
    int process, n_processes;                                                   //Process ID, Number of Processes

    MPI_Type_contiguous(8, MPI_DOUBLE, &par_type);                              //Create contiguous datatype
    MPI_Type_commit(&par_type);                                                 //Commit contiguous datatype

    MPI_Type_contiguous(5, MPI_DOUBLE, &cell_type);                             //Create contiguous datatype
    MPI_Type_commit(&cell_type);                                                //Commit contiguous datatype

    MPI_Comm_rank(MPI_COMM_WORLD, &process);                                    //Set MPI Process ID
    MPI_Comm_size(MPI_COMM_WORLD, &n_processes);                                //Set MPI Process Size

    unsigned long seed        = stol(argv[1]);                                  //Random seed
    unsigned long ncside      = stol(argv[2]);                                  //Grid size
    unsigned long long n_part = stoll(argv[3]);                                 //Number of particles
    unsigned long timesteps   = stol(argv[4]);                                  //Number of timesteps

    long max_cell_buffer = 0, max_par_buffer = n_part / (log10(n_part)*log10(n_part)*log10(n_part)+1);

    int dims[] = {0, 0};

    MPI_Dims_create(n_processes, 2, dims);

    vector<int> process_cells[n_processes];
    unordered_map<int, set<int>> comm_map;
    unordered_map<int, int> process_map;
    cell_t* grid    = new cell_t[ncside*ncside];
    long* neighbors = new long[ncside*ncside*N_NEIGHBORS];

    vector<particle_t> par;

    init_neighbors(neighbors, ncside);

    init_process_cells(process, n_processes, ncside, max_cell_buffer, dims[0], dims[1], process_cells, process_map);

    init_comm_map(process, dims[0], dims[1], ncside, comm_map, process_cells);

    init_particles(process, seed, ncside, n_part, par, process_map);

    for(int t = 0; t < timesteps; t++){
        update_cmass(grid, par, process_cells[process], ncside);
    
        get_cmasses(process, ncside, max_cell_buffer, comm_map, grid, cell_type);

        update_particles(neighbors, grid, par, ncside);

        get_particles(process, max_par_buffer, process_map, comm_map, par, par_type);
    }
    print_first(par);
    
    print_overall(process, par);

    delete[] grid;
    delete[] neighbors;

    MPI_Finalize();                                 //Finalize MPI

    return 0;
}
