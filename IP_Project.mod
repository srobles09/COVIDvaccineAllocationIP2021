set BLOCKS;
set FACILITIES;

param pop {i in BLOCKS};
param val {i in BLOCKS};
param eq {i in BLOCKS};
param vac {i in BLOCKS};
param mincap {j in FACILITIES};
param maxcap {j in FACILITIES};
param dist {BLOCKS,FACILITIES};
param supply;

var X {i in BLOCKS, j in FACILITIES} integer;
var Y {j in FACILITIES} binary;

minimize Cost: sum {i in BLOCKS} (sum {j in FACILITIES} ((dist[i,j]-val[i]/(2*pop[i]))*X[i,j]));

subject to Positivity {i in BLOCKS, j in FACILITIES}: X[i,j] >= 0;
subject to Supply: sum {i in BLOCKS} (sum {j in FACILITIES} X[i,j]) <= supply;
subject to Population {i in BLOCKS}: sum {j in FACILITIES} (X[i,j]) <= 0.7*pop[i] - vac[i]; #needs to be updated in iterative step
subject to Equity {i in BLOCKS}: sum {j in FACILITIES} (X[i,j]) >= eq[i];
subject to MinCapacity {j in FACILITIES}: mincap[j]*maxcap[j]*Y[j] <= sum {i in BLOCKS} (X[i,j]);
subject to MaxCapacity {j in FACILITIES}: sum {i in BLOCKS} (X[i,j]) <= maxcap[j]*Y[j];


#reset; model IP_Project.mod; data IP_Project_Big.dat; option solver cplex; solve; display Y; display {i in BLOCKS} sum {j in FACILITIES} X[i,j]; display {i in BLOCKS} sum {j in FACILITIES} X[i,j]/pop[i]; display X;

