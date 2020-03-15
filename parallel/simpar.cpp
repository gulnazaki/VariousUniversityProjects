//--------------------------------------------------------------------------------------//
//-------------------------------------- INCLUDES --------------------------------------//
//--------------------------------------------------------------------------------------//
#include <stdlib.h>
#include <iostream>
#include <math.h>
#include <omp.h>
#include <ctime>

//--------------------------------------------------------------------------------------//
//------------------------------------- NAMESPACES -------------------------------------//
//--------------------------------------------------------------------------------------//
using namespace std;

//--------------------------------------------------------------------------------------//
//------------------------------------- CONSTANTS --------------------------------------//
//--------------------------------------------------------------------------------------//
#define RND0_1 ((double) random() / ((long long)1<<31))
#define G 6.67408e-11
#define EPSLON 0.0005
#define N_NEIGHBORS 9

//--------------------------------------------------------------------------------------//
//-------------------------------------- CLASSES ---------------------------------------//
//--------------------------------------------------------------------------------------//
class particle_t{
    public:
        double x, y;    //Position
        double vx, vy;  //Velocity
        double m;       //Mass
        long long c;    //Cell
};

class cell{
    public:
        double x, y;    //Position
        double mx, my;  //Mass x Position
        double m;       //Total mass
};

//--------------------------------------------------------------------------------------//
//------------------------------------- FUNCTIONS --------------------------------------//
//--------------------------------------------------------------------------------------//
void init_particles(long seed, long ncside, long long n_part, particle_t *par){
    srandom(seed);

    for(long long i = 0; i < n_part; i++){
        par[i].x  = RND0_1;
        par[i].y  = RND0_1;
        par[i].vx = RND0_1 / ncside / 10.0;
        par[i].vy = RND0_1 / ncside / 10.0;
        par[i].m  = RND0_1 * ncside / (G * 1e6 * n_part);
    }
}

long cell_index(long long p, long ncside, particle_t *par){
    long cell_x = (par[p].x == 1)?0:long(floor(par[p].x/(1./ncside)));
    long cell_y = (par[p].y == 1)?0:long(floor(par[p].y/(1./ncside)));
    return cell_x + cell_y * ncside;
}

long* cell_neighbors(long ncside){
    long* neighbors = new long[ncside*ncside*N_NEIGHBORS]();

    #pragma omp parallel for
    for(long c = 0; c < ncside*ncside; c++) {
        int idx = 0;
        long x = c%ncside;
        long y = floor(c/ncside);
        for(int h = -1; h <= 1; h++) {
            for(int w = -1; w <= 1; w++) {
                long nx = (ncside + x + w)%ncside;
                long ny = (ncside + y + h)%ncside;
                neighbors[c*N_NEIGHBORS+(idx++)] = nx+ny*ncside;
            }
        }
    }
    return neighbors;
}

void update_particles(long *neighbors, cell *grid, particle_t *par, long long n_part){
    #pragma omp parallel for
    for(long long p = 0; p < n_part; p++){
        double fx = 0, fy = 0;

        for(int n = 0; n < N_NEIGHBORS; n++){
            long long c = neighbors[par[p].c * N_NEIGHBORS + n]; //Cell index of current neighbor
            
            if(grid[c].m != 0){
                double dx = grid[c].x - par[p].x;
                double dy = grid[c].y - par[p].y;

                double dist = sqrt(dx*dx + dy*dy);
                
                if(dist >= EPSLON){
                    double force = (G * par[p].m * grid[c].m) / (dist*dist);
                    
                    fx += force * dx / dist;
                    fy += force * dy / dist;
                }
            }
        }
        double ax = fx / par[p].m;                                        //Calculate Acceleration X
        double ay = fy / par[p].m;                                        //Calculate Acceleration Y
                                                     
        par[p].x  = fmod(1 + fmod(par[p].x + par[p].vx + 0.5*ax, 1), 1);  //Calculate X Position
        par[p].y  = fmod(1 + fmod(par[p].y + par[p].vy + 0.5*ay, 1), 1);  //Calculate Y Position

        par[p].vx += ax;                                                  //Calculate X Velocity
        par[p].vy += ay;                                                  //Calculate Y Velocity
    }
}

void update_cmass(cell *grid, particle_t *par, long ncside, long long n_part){
    #pragma omp parallel for
    for(long long c = 0; c < ncside*ncside; c++){
        grid[c].m = 0;                      //Reset total mass
    }
    long long c;
    #pragma omp parallel for private(c)
    for(long long p = 0; p < n_part; p++){
        c = cell_index(p, ncside, par);
        
        #pragma omp atomic
        grid[c].m  += par[p].m;             //M, sum of all particles' masses in the cell
        #pragma omp atomic
        grid[c].mx += par[p].m * par[p].x;  //Sum of mass times x
        #pragma omp atomic
        grid[c].my += par[p].m * par[p].y;  //Sum of mass times y
        
        par[p].c = c;                       //Store the cell index of this particle
    }
    #pragma omp parallel for
    for(long long c = 0; c < ncside*ncside; c++){
        grid[c].x = grid[c].mx / grid[c].m; //Divide by total mass to obtain x
        grid[c].y = grid[c].my / grid[c].m; //Divide by total mass to obtain y

        grid[c].mx = 0;                     //Reset mx
        grid[c].my = 0;                     //Reset my
    }    
}

void overall_cmass(cell *grid, long ncside){
    double mx = 0, my = 0, m = 0;
    #pragma omp parallel for reduction(+:mx,my,m)
    for(long c = 0; c < ncside*ncside; c++){
        if(grid[c].m != 0){
            mx += grid[c].m * grid[c].x;
            my += grid[c].m * grid[c].y;
            m  += grid[c].m;
        }
    }
    printf("%.2f %.2f\n", mx/m, my/m);
}

int main(int argc, const char * argv[]) {
    time_t timer = time(NULL);

    omp_set_num_threads(16);

    unsigned long seed          = stol(argv[1]);    //Random seed
    unsigned long ncside        = stol(argv[2]);    //Grid size
    unsigned long long n_part   = stoll(argv[3]);   //Number of particles
    unsigned long timesteps     = stol(argv[4]);    //Number of timesteps

    particle_t* par = new particle_t[n_part];       //Create particles array
    cell* grid      = new cell[ncside*ncside];      //Create cells array
    long* neighbors = cell_neighbors(ncside);       //Precompute cell neighbors

    init_particles(seed, ncside, n_part, par);      //Initialize particles
    update_cmass(grid, par, ncside, n_part);        //Update center of mass of each cell

    for(int t = 0; t < timesteps; t++){
        update_particles(neighbors, grid, par, n_part); //Update particles position and velocity
        
        update_cmass(grid, par, ncside, n_part);        //Update center of mass of each cell
    }

    printf("%.2f %.2f\n", par[0].x, par[0].y);

    overall_cmass(grid, ncside); //GONCALO

    delete[] par;
    delete[] grid;
    delete[] neighbors;

    cout << difftime(time(NULL),timer) << " seconds\n";

    return 0;
}
