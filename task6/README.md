# DFTB+
## What is DFTB+?  
DFTB+ (Density Functional Tight-Binding) is a quantum chemistry software package used in scientific research to simulate the behaviour of atoms and molecules. It is used in fields like drug discovery, materials science, and nanotechnology, and it is exactly the kind of software that HPC clusters are built to run.
You give it a molecule and it tells you how the electrons are arranged and how much total energy the system holds.  

## Building DFTB+

### Step 1 - Load dependencies

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

### Step 2 - Get the source

```bash
mkdir -p ~/dftb_workspace
cd ~/dftb_workspace
git clone https://github.com/dftbplus/dftbplus.git
cd dftbplus
```

### Step 3 - Fetch optional external components

```bash
./utils/get_opt_externals
```

This downloads additional components DFTB+ needs. Wait for it to finish before moving on.

### Step 4 - Export your compilers

The cluster has multiple GCC versions installed. You need to explicitly tell CMake to use the one loaded by your module, not the system default:

```bash
export CC=$(which gcc)
export CXX=$(which g++)
export FC=$(which gfortran)
```
> [!CAUTION]
> Skipping this step causes CMake to fall back to the system GCC (version 11.5), which is too old for DFTB+. The build will fail with `GNU Fortran compiler is too old`.

### Step 5 - Configure the build

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

### Step 6 - Compile and install

```bash
make -j$(nproc)
make install
```

This will take several minutes. Once done, confirm the executable exists:

```bash
ls ${HOME}/opt/dftbplus/bin/dftb+
```

### Step 7 - Update your environment

```bash
export PATH=${HOME}/opt/dftbplus/bin:${PATH}
dftb+ --version
```

If a version number prints, DFTB+ is ready.

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

## Your First Calculation

### Step 1 - Set up a working directory

```bash
mkdir -p $HOME/dftb_water
cd $HOME/dftb_water
```

### Step 2 - Download the input files

Download the following files from the repo into your working directory:

- `water.gen` - the geometry of the water system
- `dftb_in.hsd` - the DFTB+ input configuration

### Step 3 - Fix the username placeholder

The input file contains a placeholder for the Slater-Koster path. Replace it with your actual username:

```bash
sed -i "s|<username>|$(whoami)|g" dftb_in.hsd
```

## The Final Task

Your team will attempt to get the **most negative Total Energy** with the **lowest Wall Clock time** for the water system.

You are free to research and modify any parameters in `dftb_in.hsd` and `run_dftb.sh`. All tools on the system are available to you.

Some things worth investigating and writing to README.md:

### Investigation Questions Part 1  
> [!NOTE]
> Please answer the investigation questions in your own words. We will be checking submissions for AI-generated responses. Marks will not be awarded for answers that appear to be AI-generated.
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

### Post-Processing with dptools and Python  
> [!CAUTION]
> You are advised to skip this section if you have fallen behind the pace recommended by the course coordinators. Skipping this section will NOT stop you from completing the remainder of the tutorials.

After your calculation finishes, you will process and visualise the results using **dptools** and **Python**. This section walks you through setting up the environment, generating the data files, and producing the plots.
 
#### Step 1 - Load Python and set up the dptools environment
 
The dptools environment must be built using the cluster's Python 3.12.6 module. The system Python is too old and will fail. Do this once:
 
```bash
ml python3.12/3.12.6-gcc-15.2.0
python3 --version   # Must show 3.12.6 before continuing
 
cd ~/dftb_workspace/dftbplus/tools/dptools/
rm -rf dptools_env # If there's an existing environment
python3 -m venv dptools_env
source dptools_env/bin/activate
 
pip install .
pip install matplotlib numpy
```
 
> [!CAUTION]
> Always load `ml python3.12/3.12.6-gcc-15.2.0` **before** activating the environment. The dptools package requires Python >= 3.10 and will refuse to install on the system Python.
 
#### Step 2 - Update dftb_in.hsd to produce band output
 
Your `dftb_in.hsd` needs a proper k-point mesh and `WriteBandOut = Yes` to generate the files needed for post-processing. Make sure your `KPointsAndWeights` and `Analysis` blocks look like this:
 
```
KPointsAndWeights = SupercellFolding {
  4 0 0
  0 4 0
  0 0 4
  0.5 0.5 0.5
}
```
 
```
Analysis {
  WriteBandOut = Yes
  MullikenAnalysis = Yes
}
```
 
Re-submit your job after making these changes:
 
```bash
sbatch run_dftb.sh
```
 
After the job finishes, confirm `band.out` was created:
 
```bash
ls band.out
```
 
#### Step 3 - Generate data files with dptools
 
Activate your environment and run dptools from your calculation directory:
 
```bash
cd ~/dftb_water
source ~/dftb_workspace/dftbplus/tools/dptools/dptools_env/bin/activate
 
dp_dos band.out dos_total.dat
dp_bands -A band.out water_bands
```
 
This creates two files: `dos_total.dat` and `water_bands_tot.dat`.
 
#### Step 4 - Download and run the plotting scripts
 
Download the two Python plotting scripts from the repo into your working directory:
 
- `plot_results.py` - plots the DOS and band structure from `dos_total.dat` and `water_bands_tot.dat`
- `plot_water.py` - plots the atomic charges and energy components from `detailed.out`
 
Then run them:
 
```bash
python3 plot_results.py
python3 plot_water.py
```
 
You should end up with four PNG files: `dos_plot.png`, `bands_plot.png`, `charges_plot.png`, and `energy_plot.png`.
 
> [!TIP]
> Both scripts use `matplotlib.use('Agg')` which writes plots directly to PNG files without needing a display. If you remove this line the script will crash.

### Investigation Questions Part 2  
> [!CAUTION]
> You are advised to skip this section if you have fallen behind the pace recommended by the course coordinators. Skipping this section will NOT stop you from completing the remainder of the tutorials. If you're unable to get to the post-processing and plots you can skip this section, it should be noted that the use of AI to respond to these questions is discouraged. 

- What does the `KPointsAndWeights` block control, and why does using more k-points give a better result but take longer?
- Look at your atomic charges plot - why are the oxygen atoms always negative and the hydrogen atoms always positive? What does this tell you about how water molecules share electrons?
- What is the band gap of your water system? How can you read it from either the DOS plot or the band structure plot?
- What does the `WriteBandOut` option in the `Analysis` block do, and what file does it produce?
- Look at your energy components plot - the H0 energy is large and negative, but the SCC and Repulsive terms partially cancel it. What does each of these three terms physically represent?

### Scoring

For the main task, teams are ranked by **Total Wall Clock time** and **Total Energy**. Lower wall clock = faster. More negative energy = better physics. Both metrics count.  

| Component | Marks |
|---|---|
| Main DFTB+ Task (Total Energy + Wall Clock time) | 7% |
| Visualisation (all 4 plots generated and submitted) | 2% |
| Investigation Questions | 1% |
| **Total** | **10%** |

### What to submit

Upload the following to in your repo before the deadline:

- `dftb_in.hsd` - input file used for your best score
- `run_dftb.sh` - Slurm script used for your best score
- `water.out` - full DFTB+ output from your best run
- `dftb_XX.out` - full Slurm output showing the results summary  
- `dos_plot.png` - Density of States
- `bands_plot.png` - Band structure
- `charges_plot.png` - Atomic gross charges
- `energy_plot.png` - Energy components
- `README.md` - Upload a README.md answering the investigation questions above and also explaining in simple terms what you did  

> [!NOTE]
> You may submit multiple runs, but only your best scoring run needs to be in the repo. Make sure the files you submit all come from the same run.
