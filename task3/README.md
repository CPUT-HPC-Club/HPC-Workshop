# Benchmark: HPL
HPL is a benchmark which solves a dense linear system of double-precision values. It is one of the most popular HPC benchmarks.<br>
HPL requires a Message Passing Interface and a Basic Linear Algebra Subprogram.<br>
## Running your first benchmark
In order to compile the HPL benchmark, the two dependencies need to be installed and setup.
### MPI: OpenMPI
First, load OpenMPI from lmod:
```
ml openmpi
```
Next, run the following command to confirm it has been loaded and find where the OpenMPI C Compiler is:
```
which mpicc
```
### BLAS: Atlas
Atlas has already been preinstalled for you. Run the following to confirm the library files:
```
ls /usr/lib64/atlas
```
### HPL
With the dependencies ready, we shall now compile the benchmark.<br>
Download the source files using:
```
cd $HOME
wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
tar -xf hpl-2.3.tar.gz
```
Next, prepare the makefile by copying one of the templates:
```
mv hpl-2.3 hpl
cd hpl
cp setup/Make.Linux_PII_CBLAS_gm Make.Tutorial3
```
This template isn't usable as is, and needs to be editted. Open the file for editting and alter it so that the following parameters have these values:
```
ARCH         = Tutorial3

MPdir        = /usr/lib64/openmpi
MPlib        = $(MPdir)/lib/libmpi.so

LAdir        = /usr/lib64/atlas
LAlib        = $(LAdir)/libtatlas.so $(LAdir)/libsatlas.so

LINKER       = mpicc
```
With this, everything should be ready to compile our benchmark.
```
make arch=Tutorial3
cd bin/Tutorial3
ls
```
If successful, you should see ```xhpl``` and ```HPL.dat```. Remove and replace the ```HPL.dat``` file with the following text:
```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
4            Ns
1            # of NBs
1            NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
1            Ps
1            Qs
16.0         threshold
3            # of panel fact
0 1 2        PFACTs (0=left, 1=Crout, 2=Right)
2            # of recursive stopping criterium
2 4          NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
3            # of recursive panel fact.
0 1 2        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```
With this, we can now run our benchmark:
```
./xhpl
```
This should quickly produce an output. Your output will have a line that looks something like this:
```
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR00L2L2           4     1     1     1               0.00             7.1014e-04
```
This is the summary of your benchmark result. In this case, the benchmark got a score of 7.1014e-04 Gflops. If you see this or something similar, you have successfully completed your first benchmark.
## Base upload
Upload the ```HPL.dat``` textfile, the ```xhpl``` executable file, and the entire resulting output from your HPL benchmark to your GitHub repo, in a directory ```.../tut3/base/```. The actual score here does not matter, only that you did get a score.
## Task
Learn more about the HPL benchmark, either using online resources or the README in the source files. Attempt the following:
- Your output currently goes to the terminal. Change your configuration such that it goes into a file called ```Tutorial3.out``` instead.
- Your benchmark currently runs multiple tests with a single call. Change the configuration to run only one test.
- Your BLAS library, Atlas, is not the best choice. Try using a different set of libraries, such as Lapack or OpenBLAS.
Upload ```HPL.dat```, ```xhpl```and your result to ```.../tut3/task/```. Include a file called ```improvements.txt``` containing a list of changes you have made. Any improvements not listed will be considered incomplete.<br>
Scores will be compared across teams. The benchmark score will be marked upwards for the following checkpoints:
- Output automatically goes into ```Tutorial3.out```: +3.0000e-01
- Benchmark only runs a single test: +4.0000e-01
- Benchmark uses different BLAS libraries: +7.0000e-01