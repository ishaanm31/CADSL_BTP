#!/bin/bash
start=$(date +%s)
filein="null"
maxk=30
count=0
while getopts b:a:f:i:k: flag
do
	case "${flag}" in
		b) BENCHMARK=${OPTARG};;
		a) argument=${OPTARG};;
		f) filein=${OPTARG};;
		i) interval=${OPTARG};;
		k) maxk=${OPTARG};;
	esac
done

############ DIRECTORY VARIABLES: MODIFY ACCORDINGLY #############
GEM5_DIR=/home/piyush/gem5                          # Install location of gem5
SPEC_DIR=/home/piyush/gem5/MTP/spec-x86-cpu-2006                 # Install location of your SPEC2006 benchmarks
##################################################################

######################### BENCHMARK CODENAMES ####################
PERLBENCH_CODE=400.perlbench
BZIP2_CODE=401.bzip2
GCC_CODE=403.gcc
BWAVES_CODE=410.bwaves
GAMESS_CODE=416.gamess
MCF_CODE=429.mcf
MILC_CODE=433.milc
ZEUSMP_CODE=434.zeusmp
GROMACS_CODE=435.gromacs
CACTUSADM_CODE=436.cactusADM
LESLIE3D_CODE=437.leslie3d
NAMD_CODE=444.namd
GOBMK_CODE=445.gobmk
DEALII_CODE=447.dealII
SOPLEX_CODE=450.soplex
POVRAY_CODE=453.povray
CALCULIX_CODE=454.calculix
HMMER_CODE=456.hmmer
SJENG_CODE=458.sjeng
GEMSFDTD_CODE=459.GemsFDTD
LIBQUANTUM_CODE=462.libquantum
H264REF_CODE=464.h264ref
TONTO_CODE=465.tonto
LBM_CODE=470.lbm
OMNETPP_CODE=471.omnetpp
ASTAR_CODE=473.astar
WRF_CODE=481.wrf
SPHINX3_CODE=482.sphinx3
XALANCBMK_CODE=483.xalancbmk
SPECRAND_INT_CODE=998.specrand
SPECRAND_FLOAT_CODE=999.specrand
##################################################################
 
# Check BENCHMARK input
#################### BENCHMARK CODE MAPPING ######################
BENCHMARK_CODE="none"
 
if [[ "$BENCHMARK" == "perlbench" ]]; then
    BENCHMARK_CODE=$PERLBENCH_CODE
fi
if [[ "$BENCHMARK" == "bzip2" ]]; then
    BENCHMARK_CODE=$BZIP2_CODE
fi
if [[ "$BENCHMARK" == "gcc" ]]; then
    BENCHMARK_CODE=$GCC_CODE
fi
if [[ "$BENCHMARK" == "bwaves" ]]; then
    BENCHMARK_CODE=$BWAVES_CODE
fi
if [[ "$BENCHMARK" == "gamess" ]]; then
    BENCHMARK_CODE=$GAMESS_CODE
fi
if [[ "$BENCHMARK" == "mcf" ]]; then
    BENCHMARK_CODE=$MCF_CODE
fi
if [[ "$BENCHMARK" == "milc" ]]; then
    BENCHMARK_CODE=$MILC_CODE
fi
if [[ "$BENCHMARK" == "zeusmp" ]]; then
    BENCHMARK_CODE=$ZEUSMP_CODE
fi
if [[ "$BENCHMARK" == "gromacs" ]]; then
    BENCHMARK_CODE=$GROMACS_CODE
fi
if [[ "$BENCHMARK" == "cactusADM" ]]; then
    BENCHMARK_CODE=$CACTUSADM_CODE
fi
if [[ "$BENCHMARK" == "leslie3d" ]]; then
    BENCHMARK_CODE=$LESLIE3D_CODE
fi
if [[ "$BENCHMARK" == "namd" ]]; then
    BENCHMARK_CODE=$NAMD_CODE
fi
if [[ "$BENCHMARK" == "gobmk" ]]; then
    BENCHMARK_CODE=$GOBMK_CODE
fi
if [[ "$BENCHMARK" == "dealII" ]]; then # DOES NOT WORK
    BENCHMARK_CODE=$DEALII_CODE
fi
if [[ "$BENCHMARK" == "soplex" ]]; then
    BENCHMARK_CODE=$SOPLEX_CODE
fi
if [[ "$BENCHMARK" == "povray" ]]; then
    BENCHMARK_CODE=$POVRAY_CODE
fi
if [[ "$BENCHMARK" == "calculix" ]]; then
    BENCHMARK_CODE=$CALCULIX_CODE
fi
if [[ "$BENCHMARK" == "hmmer" ]]; then
    BENCHMARK_CODE=$HMMER_CODE
fi
if [[ "$BENCHMARK" == "sjeng" ]]; then
    BENCHMARK_CODE=$SJENG_CODE
fi
if [[ "$BENCHMARK" == "GemsFDTD" ]]; then
    BENCHMARK_CODE=$GEMSFDTD_CODE
fi
if [[ "$BENCHMARK" == "libquantum" ]]; then
    BENCHMARK_CODE=$LIBQUANTUM_CODE
fi
if [[ "$BENCHMARK" == "h264ref" ]]; then
    BENCHMARK_CODE=$H264REF_CODE
fi
if [[ "$BENCHMARK" == "tonto" ]]; then
    BENCHMARK_CODE=$TONTO_CODE
fi
if [[ "$BENCHMARK" == "lbm" ]]; then
    BENCHMARK_CODE=$LBM_CODE
fi
if [[ "$BENCHMARK" == "omnetpp" ]]; then
    BENCHMARK_CODE=$OMNETPP_CODE
fi
if [[ "$BENCHMARK" == "astar" ]]; then
    BENCHMARK_CODE=$ASTAR_CODE
fi
if [[ "$BENCHMARK" == "wrf" ]]; then
    BENCHMARK_CODE=$WRF_CODE
fi
if [[ "$BENCHMARK" == "sphinx3" ]]; then
    BENCHMARK_CODE=$SPHINX3_CODE
fi
if [[ "$BENCHMARK" == "Xalan" ]]; then # DOES NOT WORK
    BENCHMARK_CODE=$XALANCBMK_CODE
fi
if [[ "$BENCHMARK" == "specrand_i" ]]; then
    BENCHMARK_CODE=$SPECRAND_INT_CODE
fi
if [[ "$BENCHMARK" == "specrand_f" ]]; then
    BENCHMARK_CODE=$SPECRAND_FLOAT_CODE
fi
if [[ "$BENCHMARK" == "hello" ]]; then
    BENCHMARK_CODE=hello
fi
 
# Sanity check
if [[ "$BENCHMARK_CODE" == "none" ]]; then
    echo "Input BENCHMARK selection $BENCHMARK did not match any known SPEC CPU2006 benchmarks! Exiting."
    exit 1
fi
##################################################################

RUN_DIR=$SPEC_DIR/benchspec/CPU2006/$BENCHMARK_CODE/build/build_base_gcc44-64bit.0000     # Run directory for the selected SPEC BENCHMARK

echo ""
echo "Changing to SPEC BENCHMARK runtime directory: $RUN_DIR"
cd $RUN_DIR

if [ $filein == "null" ]
then
	valgrind --tool=exp-bbv --interval-size=$interval --bb-out-file=bb.out.$BENCHMARK ./$BENCHMARK $argument
else
	valgrind --tool=exp-bbv --interval-size=$interval --bb-out-file=bb.out.$BENCHMARK ./$BENCHMARK $argument < $filein
fi

mv bb.out.$BENCHMARK /home/piyush/gem5/MTP/simpoints/
cd /home/piyush/gem5/MTP/simpoints/
./bin/simpoint -maxK $maxk -loadFVFile bb.out.$BENCHMARK -saveSimpoints simpoints.$BENCHMARK -saveSimpointWeights weights.$BENCHMARK

awk '
    BEGIN { FS=OFS=" " }
    NR==FNR { a[NR]=$0; next }
    {
        split(a[FNR],f)
        for (i=1;i<=NF;i++) {
            printf "%s%s%s%s", f[i], OFS, $i, (i<NF?OFS:ORS)
        }
    }
' simpoints.$BENCHMARK weights.$BENCHMARK > simpoint_output.$BENCHMARK.temp

cut --complement -d' ' -f3 simpoint_output.$BENCHMARK.temp > simpoint_output.$BENCHMARK
intcompact=$((($interval)/1000000))
rm simpoints.$BENCHMARK weights.$BENCHMARK simpoint_output.$BENCHMARK.temp
mkdir -p simpoint_results/$BENCHMARK/${intcompact}M/
mv bb.out.$BENCHMARK simpoint_output.$BENCHMARK ./simpoint_results/$BENCHMARK/${intcompact}M/
end=$(date +%s)
echo "Elapsed Time: $(($end - $start)) seconds" > ./simpoint_results/$BENCHMARK/${intcompact}M/time_elapsed
