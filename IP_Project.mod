############## Data Stes ########################

set BLOCKS; 
set FACILITIES;

############### Parameters ######################

param pop {i in BLOCKS}; 
#population of block i

param val {i in BLOCKS}; 
#vale of the cost of vaccinating no one in block i

param eq {i in BLOCKS}; 
#min vaccines to be distributed to block i

param vac {i in BLOCKS}; 
#number of vaccinated individuals in block i

param mincap {j in FACILITIES}; 
#between 0 and 1 - min percent of max capacity for a facility to open

param maxcap {j in FACILITIES}; 
#maximum capacity of facility j

param dist {BLOCKS,FACILITIES}; 
#cost of distributing a vaccine to tract i from facility j

param supply; 
#number of vaccines available

############### Variables #######################

var X {i in BLOCKS, j in FACILITIES} integer; 
#number of vaccines distributed from facility j to tract i

var Y {j in FACILITIES} binary; 
#1 if facility j is open, 0 otherwise

############### Objective Function ##############
minimize Cost: sum {i in BLOCKS} (sum {j in FACILITIES} ((dist[i,j]-val[i]/(2*pop[i]))*X[i,j]));
#minimizes the cost of the non-vaccinated individuals

############### Constraints ##################### 

subject to Positivity {i in BLOCKS, j in FACILITIES}: X[i,j] >= 0;
#0 is the minimum vaccines a facility can distribute to a tract

subject to Supply: sum {i in BLOCKS} (sum {j in FACILITIES} X[i,j]) <= supply;
#Total vaccines distributed must be less than the available supply

subject to Population {i in BLOCKS}: sum {j in FACILITIES} (X[i,j]) <= 0.7*pop[i] - vac[i]; 
#Once Herd Immunity is reached, there is no additional value in vaccinating an area

subject to Equity {i in BLOCKS}: sum {j in FACILITIES} (X[i,j]) >= eq[i];
#Minimum amount of vaccines to be shipped to tract i

subject to MinCapacity {j in FACILITIES}: mincap[j]*maxcap[j]*Y[j] <= sum {i in BLOCKS} (X[i,j]);
#ratio of max capacity necessary to ensure a facility is open

subject to MaxCapacity {j in FACILITIES}: sum {i in BLOCKS} (X[i,j]) <= maxcap[j]*Y[j];
#no facility can distribute more than its max capacity

#reset; model IP_Project.mod; data IP_Project_Big.dat; option solver cplex; solve; display Y; display {i in BLOCKS} sum {j in FACILITIES} X[i,j]; display {i in BLOCKS} sum {j in FACILITIES} X[i,j]/pop[i]; display X;

