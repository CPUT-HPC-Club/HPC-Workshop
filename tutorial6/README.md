# DFTB+
## What is DFTB+?  
DFTB+ (Density Functional Tight-Binding) is a quantum chemistry software package used in scientific research to simulate the behaviour of atoms and molecules. It is used in fields like drug discovery, materials science, and nanotechnology, and it is exactly the kind of software that HPC clusters are built to run.
You give it a molecule and it tells you how the electrons are arranged and how much total energy the system holds.  

---

## Building DFTB+

### Step 1 — Load dependencies

```bash
ml purge
ml gcc openmpi openBLAS scalapack
```

Confirm everything loaded correctly:

```bash
ml
```

You should see `gcc`, `openmpi`, `openBLAS`, and `scalapack` all listed. If anything is missing, re-run `ml purge` and try again.

> [!CAUTION]
> Always start with `ml purge`. Leftover modules from a previous session can cause silent library conflicts that only surface as cryptic errors deep into the build.

### Step 2 — Get the source

```bash
mkdir -p ~/dftb_workspace
cd ~/dftb_workspace
git clone https://github.com/dftbplus/dftbplus.git
cd dftbplus
```

### Step 3 — Fetch optional external components

```bash
./utils/get_opt_externals
```

This downloads additional components DFTB+ needs. Wait for it to finish before moving on.

### Step 4 — Export your compilers

The cluster has multiple GCC versions installed. You need to explicitly tell CMake to use the one loaded by your module, not the system default:

```bash
export CC=$(which gcc)
export CXX=$(which g++)
export FC=$(which gfortran)
```
> [!CAUTION]
> Skipping this step causes CMake to fall back to the system GCC (version 11.5), which is too old for DFTB+. The build will fail with `GNU Fortran compiler is too old`.

### Step 5 — Configure the build

```bash
cd ~/dftb_workspace/dftbplus
rm -rf build && mkdir build && cd build

cmake .. \
  -DCMAKE_INSTALL_PREFIX=${HOME}/opt/dftbplus \
  -DCMAKE_Fortran_COMPILER=$(which gfortran) \
  -DCMAKE_C_COMPILER=$(which gcc) \
  -DSCALAPACK_LIBRARY=/mnt/beegfs/scalapack/2.2.3/openmpi-5.0.10-gcc-15.2.0-vectorized/lib64/libscalapack.a \
  -DWITH_MPI=YES \
  -DWITH_OMP=YES
```

### Step 6 — Compile and install

```bash
make -j$(nproc)
make install
```

This will take several minutes. Once done, confirm the executable exists:

```bash
ls ${HOME}/opt/dftbplus/bin/dftb+
```

### Step 7 — Update your environment

```bash
export PATH=${HOME}/opt/dftbplus/bin:${PATH}
dftb+ --version
```

If a version number prints, DFTB+ is ready.

---

## Slater-Koster Parameters

DFTB+ needs **Slater-Koster parameter files** to describe how electrons behave between each pair of atom types. Without these, it cannot run any calculation.

Download the `3ob-3-1` parameter set:

```bash
cd ~/dftb_workspace
mkdir -p dftb_parameters && cd dftb_parameters
wget https://github.com/dftbparams/3ob/releases/download/v3.1.0/3ob-3-1.tar.xz
tar -xf 3ob-3-1.tar.xz
```

Confirm the files extracted correctly:

```bash
ls ~/dftb_workspace/dftb_parameters/3ob-3-1/O-O.skf
```

---

## Your First Calculation

### Step 1 — Set up a working directory

```bash
mkdir -p $HOME/dftb_water
cd $HOME/dftb_water
```

### Step 2 — Download the input files

Download the following files from the repo into your working directory:

- `water.gen` - the geometry of the water system
- `dftb_in.hsd` - the DFTB+ input configuration

### Step 3 — Fix the username placeholder

The input file contains a placeholder for the Slater-Koster path. Replace it with your actual username:

```bash
sed -i "s|<username>|$(whoami)|g" dftb_in.hsd
```

## The Final Task

Your team will attempt to get the **most negative Total Energy** with the **lowest Wall Clock time** for the water system.

You are free to research and modify any parameters in `dftb_in.hsd` and `run_dftb.sh`. All tools on the system are available to you.

Some things worth investigating and writing to README.md:

- What does `SCCTolerance` control?
- What does `MaxSCCIterations` do?
- What does the `Driver` block do when it is not empty?
- How do MPI processes and OMP threads interact, and what combination is fastest on this hardware?
- What does the `Parallel` block in `dftb_in.hsd` allow you to configure?

> [!TIP]
> The DFTB+ documentation is at https://dftbplus-recipes.readthedocs.io/en/stable/. Read carefully - the answers are in there(somewhere there).

> [!CAUTION]
> Do not change the `SlaterKosterFiles` path or `ParserVersion`. Calculations that fail to run will receive no score.

### Running on the cluster

Download the Slurm submission script from the repo into your working directory. Before submitting, fill in all `xx` placeholders:
> [!CAUTION]
> `--ntasks` must equal `--nodes` × `--ntasks-per-node`. `OMP_NUM_THREADS` must match `--cpus-per-task`. Mismatches will cause the job to fail or produce incorrect results.

Submit your job:
```bash
sbatch run_dftb.sh
```
Monitor progress:

```bash
squeue -u $(whoami)
tail -f water.out
```
### Scoring

Teams are ranked by **Total Wall Clock time** and **Total Energy**. Lower wall clock = faster. More negative energy = better physics. Both metrics count.

### What to submit

Upload the following to in your repo before the deadline:

- `dftb_in.hsd` - input file used for your best score
- `run_dftb.sh` - Slurm script used for your best score
- `water.out` - full DFTB+ output from your best run
- `dftb_XX.out` - full Slurm output showing the results summary
- `README.md` - Upload a README.md answering the questions above and also explaining in simple terms what you did  

---