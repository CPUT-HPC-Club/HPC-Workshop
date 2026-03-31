#!/bin/bash
#SBATCH --job-name=dftb_water
#SBATCH --partition=club
#SBATCH --nodelist=com[xx-xx]
#SBATCH --nodes=xx
#SBATCH --ntasks-per-node=xx
#SBATCH --ntasks=xx
#SBATCH --cpus-per-task=xx
#SBATCH --time=01:00:00
#SBATCH --output=dftb_%j.out
#SBATCH --error=dftb_%j.err
 
# Load modules
ml purge
ml gcc openmpi openBLAS scalapack
 
# Environment
export PATH=${HOME}/opt/dftbplus/bin:${PATH}
export OMP_NUM_THREADS=xx
ulimit -s unlimited
 
# Fix username placeholder
sed -i "s|<username>|$(whoami)|g" dftb_in.hsd
 
echo "=== Job Info ==="
echo "Job ID:    $SLURM_JOB_ID"
echo "Nodes:     $SLURM_JOB_NODELIST"
echo "Tasks:     $SLURM_NTASKS"
echo "Directory: $(pwd)"
echo "Started:   $(date)"
echo "================"
 
# Run
mpirun -np $SLURM_NTASKS dftb+ | tee water.out
 
echo ""
echo "=== Results ==="
 
# Total energy
ENERGY=$(grep "Total Energy:" water.out | tail -1 | awk '{print $3, $4}')
echo "Total Energy:      $ENERGY"
 
# Wall clock time
WALLTIME=$(grep "^Total" water.out | tail -1 | awk '{print $(NF-1)}')
echo "Total Wall Clock:  $WALLTIME s"
 
# CPU time
CPUTIME=$(grep "^Total" water.out | tail -1 | awk '{print $(NF-3)}')
echo "Total CPU Time:    $CPUTIME s"
 
# SCC iterations
SCC_ITER=$(awk '/^ *[0-9]+ +-.+E/ {last=$1} END {print last}' water.out)
echo "SCC Cycles:        $SCC_ITER"
 
# Convergence
if grep -q "Total Energy:" water.out; then
    echo "SCC Status:        CONVERGED"
else
    echo "SCC Status:        NOT CONVERGED"
fi
 
echo "Completed:         $(date)"
echo "================"