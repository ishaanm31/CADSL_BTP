# CADSL Simpoints
This repo holds scripts that simplify the usage of SimPoint with standard benchmarks. These scripts are intended to be used on Ubuntu 18.04, running on x86 hardware.

# A brief description of the available scripts
## simpoint_install.sh
This script installs Valgrind, a toolkit that comes with a modern basic block generation tool, and SimPoint itself. All dependencies are installed by the script itself.

## sniper_install.sh
This script installs the architectural simulator Snipersim, along with all its dependencies.

## simpoint_gen.sh
```
./simpoint_gen.sh -b 'path to benchmark' -a 'input arguments' -f 'input file' -i 'interval size' -k 'maximum number of phases'
```

The script expects the benchmark to be placed in a `benchmarks` folder placed at the root of the repository.

The `input file` flag is given seperately since some benchmarks expect the input to be fed in a fashion that causes some issues with bash.

The results of the analysis are stored in the `simpoint_results` folder, in a subfolder corresponding to the benchmark and the interval size used.

### Example usage
```
./simpoint_gen.sh -b cpu2006/447.gobmk/gobmk -a '--mode gtp' -f 13x13.tst -k 30 -i 1000000000
```

The results would be stored in `cpu2006/447.gobmk/1000M/simpoint_output.gobmk`

## simpoint_gen_serial.sh

An older version of the previous script which does not support parallel execution of multiple instances.

## simpoint_cpu2006.sh
```
./simpoint_cpu2006.sh -i 'interval size' -k 'maximum number of phases'
```

The script runs `simpoint_gen.sh` parallelly for all benchmarks. excluding `dealII`, in the CPU2006 benchmark suite, assuming the reference load is being used

## simpoint_cpu2006_serial.sh

Uses `simpoint_gen_serial.sh` to run the CPU2006 benchmarks serially

# Some details about CPU2006

## Compilation

The CPU2006 binaries were compiled using `runspec`.
```
runspec --config=simpoint-pc.cfg --action=build --tune=base name_of_benchmark
```

Several errors were encountered while using newer compiler versions. These errors were often related to the fact that these benchmarks have been written to adhere to older standards of C, C++ and Fortran. Using the `4.4.7` release of `gcc`, `g++` and `gfortran` resolved these errors. A copy of `simpoint-pc.cfg` is provided in the `resources/cpu2006` folder of this repo. 

## Execution of individual benchmarks
The reference workloads were used to run the benchmarks. Therefore, all the contents of the `input/ref` folder of each benchmark is to be placed in the same directory as the binary. Steps specific to each benchmark are given below. The biggest available workload has been used wherever possible.

### perlbench
```
./perlbench splitmail.pl 1600 12 26 16 4500
```

### bzip2
```
./bzip2
```

### gcc
```
./gcc 200.in
```

### bwaves
```
./bwaves
```

### gamess
```
./gamess < cytosine.2.config
```

### mcf
```
./mcf inp.in
```

### milc
```
./milc < su3imp.in
```

### zeusmp
```
./zeusmp
```

### gromacs
```
./gromacs -nice 0 -deffnm gromacs -silent
```

### cactusADM
```
./cactusADM benchADM.par
```

### leslie3d
```
./leslie3d < leslie3d.in
```

### namd
```
./namd --input namd.input --iterations 38
```

### gobmk
```
./gobmk --mode gtp < 13x13.tst
```

### dealII
```
./dealII
```

`dealII` cannot be analysed using Valgrind's BBV generation tool due to its usage of 80-bit floating point numbers, which are incompatible with the latter.

### soplex
```
./soplex pds-50.mps
```

### povray
```
./povray SPEC-benchmark-ref.ini
```

### calculix
```
./calculix hyperviscoplastic
```

### hmmer
```
./hmmer nph3.hmm
```

### sjeng
```
./sjeng ref.txt
```

### GemsFDTD
```
./GemsFDTD
```

### libquantum
```
./libquantum 1397 8
```

### h264ref
```
./h264ref
```

`sss_encoder_main.cfg` was renamed as `encoder.cfg` to avoid passing arguments to the benchmark

### tonto
```
./tonto
```

### lbm
```
3000 reference.dat 0 0 100_100_130_ldc.of
```

### omnetpp
```
./omnetpp
```

### astar
```
./astar BigLakes2048.cfg
```

### wrf
```
./wrf
```

The file `RRTM_DATA` from `./le/32` has to be placed at `.`.

### sphinx3
```
./sphinx_livepretend ctlfile . args.an4
```

`ctlfile` was missing, and had to be manually defined going by copies of the file found on the internet. A load about double the size of the test set has been defined. A copy of `ctlfile` is present in the `resources/cpu2006` folder of this repo.

### xalancbmk
```
./Xalan t5.xml xalanc.xsl
```

