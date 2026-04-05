
# Training Guide for High Performance Linpack  
### By Anthony Joseph

---

# What is HPL?

High Performance Linpack (HPL) is a benchmark used to measure the floating-point computing power of a supercomputer or cluster.

It solves a system of linear equations using LU decomposition and measures how fast the computer performs floating point operations (FLOPS).

The final result is measured in:

GFLOPS – Giga Floating Point Operations per Second  
TFLOPS – Tera Floating Point Operations per Second

HPL is used to rank the world’s fastest supercomputers in the TOP500 list.

---

# Why HPL is Important

HPL is widely used because it:

• Measures raw CPU performance  
• Tests network communication between nodes  
• Evaluates memory bandwidth and latency  
• Helps tune HPC clusters  

HPL stresses

(Hint: These are main things when it comes to HPL, this will alow you to know how to tune your HPL.dat for maxinmum performance)


║ CPU             
║ Memory      
║ MPI communication           


---

# HPC Concepts that you Must understand

Before running HPL, you must understand:

## Nodes

A node is a computer inside a cluster.

Example cluster:

Head Node 
Compute Node 1 
Compute Node 2 

---

# MPI (Message Passing Interface)

HPL uses OpenMPI or MPICH for communication between nodes.

MPI allows programs to run across multiple machines.

Hint MPI is the software you use to run your HPL across the multiple computers or aka CLUSTER. And it also allows you to run your application with multiple cores.

Example: This runs HPL on 8 processes.

```bash
mpirun -np 8 ./xhpl
```

Example: This runs HPL across the Cluster on 32 processors

```bash
mpirun -np 32 --host head:8,com1:8,com2:8 ./xhpl
```

---

# BLAS Libraries

HPL depends heavily on optimized BLAS libraries.

Examples:

• OpenBLAS (60% of theoretical peak)  
• ATLAS  
• Intel Math Kernel Library (60%-80% of theoretical peak) meaning the best in the business only for intel cores.

These libraries make matrix calculations much faster.

---

#  HPL Algorithm (Core Idea)

HPL solves:

Ax = b

Where:

A = matrix  
x = unknown vector  
b = result vector  

It uses LU decomposition:

A = LU

Where:

L = lower triangular matrix  
U = upper triangular matrix  

The algorithm then solves the system efficiently using parallel computation.

---

#  HPL Software Components

To run HPL, you need:

| Component | Purpose |
|-----------|--------|
| MPI | Communication between nodes |
| BLAS | Fast matrix operations |
| GCC | Compiler |
| HPL | Benchmark program |

Typical stack:

```
GCC
OpenMPI
BLAS (OpenBLAS / ATLAS)
HPL
```

---

#  Installing HPL (Basic Steps)

## Step 1: Install dependencies

```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install gfortran git gcc wget make
```

Install MPI

```bash
sudo dnf install openmpi openmpi-devel
```

Download OpenBlas

```bash
git clone https://github.com/xianyi/OpenBLAS.git
cd OpenBLAS
git checkout v0.3.26
make
make PREFIX=/home/user/software/openblas install
```

( ' /home/user/software/openblas install ' : This is the directory of where your openblas software is installed)

---

# Download HPL

```bash
wget http://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
tar -xzf hpl-2.3.tar.gz
mv hpl-2.3 hpl
cd hpl
```

Copy a the make file to this directory. You can get example from the setup directory

```bash
cp ./setup/Make.Linux_PII_CBLAS_gm ./Make.<arch>
```

Replace `<arch>` with your team name or your name or any name to be honest, so ill replace mine with Make.Linux

---

# Edit your make file

```bash
nano Make.Linux
```

Or

```bash
vi Make.Linux
```

---

# Now configure your make file

```
ARCH         = Linux

MPdir        = /usr/lib64/openmpi
MPlib        = $(MPdir)/lib/libmpi.so

LAdir        = /home/user/software/openblas
LAlib        = $(LAdir)/lib/libopenblas.a $(LAdir)/lib/libopenblas.so

LINKER       = mpicc
```

---

Before compiling your hpl make sure that the environments of your software is loaded, like your gcc, openmpi, openblas

To see this just use these following commands

```bash
which gcc
```

```bash
mpirun --version
```

```bash
which mpicc
```

```bash
ls /home/user/software/openblas
```

Once you have confirmed all of this

Then lets compile our HPL

```bash
make arch=Linux
```

```bash
cd bin/Linux
ls
```

If successful, you should see

```
xhpl
HPL.dat
```

Remove and replace the HPL.dat file with the following text:

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

---

# Now lets run the hpl benchmark

```bash
./xhpl 
```
This only allows you to run the hpl benchmark on one processor,tune the HPL.dat file to run on more.

---

# Tuning
---

# Problem size N

NBs represents the problem size, with Ns the number of problems.

To calculate the maximum problem size, use:

```
Nmax = ( (Total cluster memory in bytes) / 8 ) ^ 0.5
```

However, the system will need some memory space for its own processes, and so using the max theoretical problem size is ill-advised.

The standard is to instead use 80% of the maximum:

```
Nrecommend = Nmax * 0.8
```

This therefore gives:

```
N = (0.1 * Total cluster memory in bytes) ^ 0.5
```

---

# Process grid ratio P x Q

P and Q should be as close to equal as possible, with Q > P where necessary.

---

# Block size NB

The smaller it is, the more balanced the load becomes. However, making it too small will reduce data reuse, so start high and refine lower.
