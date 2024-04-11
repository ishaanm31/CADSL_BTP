#!/bin/bash
start=$(date +%s)
SECONDS=0
#
# run_gem5_spec06_benchmark.sh 
 
while getopts ":b:o:f:w:m:c:-:" flag
do
	case "${flag}" in
		b) BENCHMARK=${OPTARG};;    # Benchmark name, e.g. bzip2
		o) OUTPUT_DIR=${OPTARG};;   # Directory to place run output. Make sure this exists!
		f) fastforwardinsts=${OPTARG};;
		w) warmupinsts=${OPTARG};;
		m) maximuminsts=${OPTARG};;
        c) CPU_TYPE=${OPTARG};;
        -)
            case "${OPTARG}" in
                recordbranchoutcomes) RecordBranchOutcomes=true;;
                *)
                    echo "Invalid option: --${OPTARG}"
                    exit 1
                    ;;
            esac
            ;;
        *)
            echo "Invalid option: -${flag}"
            exit 1
            ;;
	esac
done

ISA=X86                          # name of ISA (ARM,X86)

ISA_lower=$(echo "$ISA" | tr '[:upper:]' '[:lower:]')
############ DIRECTORY VARIABLES: MODIFY ACCORDINGLY #############
GEM5_DIR=/home/piyush/gem5                          # Install location of gem5
SPEC_DIR=/home/piyush/gem5/MTP/spec-"$ISA_lower"-cpu-2006                 # Install location of your SPEC2006 benchmarks
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
if [[ "$BENCHMARK" == "gobmk" ]] || [ "$BENCHMARK" == "gobmk_base.armv7-gcc" ]; then
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
    echo "Input benchmark selection $BENCHMARK did not match any known SPEC CPU2006 benchmarks! Exiting."
    exit 1
fi

##################################################################

# Create OUTPUT_DIR
OUTPUT_DIR+="/"$CPU_TYPE
mkdir -p $OUTPUT_DIR || echo "$OUTPUT_DIR already exists!"
# echo $OUTPUT_DIR
# Check OUTPUT_DIR existence
if [[ !(-d "$OUTPUT_DIR") ]]; then
    echo "Output directory $OUTPUT_DIR does not exist! Exiting."
    exit 1
fi

if [[ "$ISA" == "ARM" ]]; then
    RUN_DIR=$SPEC_DIR/benchspec/CPU2006/$BENCHMARK_CODE/build/build_base_armv7-gcc.0000     # Run directory for the selected SPEC benchmark
elif [[ "$ISA" == "X86" ]]; then
    RUN_DIR=$SPEC_DIR/benchspec/CPU2006/$BENCHMARK_CODE/build/build_base_gcc44-64bit.0000     # Run directory for the selected SPEC benchmark
else
    echo "ISA $ISA not supported for now"
fi
SCRIPT_OUT=$OUTPUT_DIR/runscript.log                                                                    # File log for this script's stdout henceforth
 
################## REPORT SCRIPT CONFIGURATION ###################
 
echo "Command line:"                                | tee $SCRIPT_OUT
echo "$0 $*"                                        | tee -a $SCRIPT_OUT
echo "================= Hardcoded directories ==================" | tee -a $SCRIPT_OUT
echo "GEM5_DIR:                                     $GEM5_DIR" | tee -a $SCRIPT_OUT
echo "SPEC_DIR:                                     $SPEC_DIR" | tee -a $SCRIPT_OUT
echo "==================== Script inputs =======================" | tee -a $SCRIPT_OUT
echo "BENCHMARK:                                    $BENCHMARK" | tee -a $SCRIPT_OUT
echo "OUTPUT_DIR:                                   $OUTPUT_DIR" | tee -a $SCRIPT_OUT
echo "==========================================================" | tee -a $SCRIPT_OUT
##################################################################
 
 
#################### LAUNCH GEM5 SIMULATION ######################
echo ""
echo "Changing to SPEC benchmark runtime directory: $RUN_DIR" | tee -a $SCRIPT_OUT
cd $RUN_DIR
 
echo "" | tee -a $SCRIPT_OUT
echo "" | tee -a $SCRIPT_OUT
echo "--------- Here goes nothing! Starting gem5! ------------" | tee -a $SCRIPT_OUT
echo "" | tee -a $SCRIPT_OUT
echo "" | tee -a $SCRIPT_OUT

# fastforwardinsts=1000000
# warmupinsts=2000000
# maximuminsts=1000000
memsize=4GB
cpuclock=3GHz
l1isize=32kB
l1iassoc=4
l1dsize=32kB
l1dassoc=4

if [[ "$CPU_TYPE" == "OoO" ]]; then
    cputype=DerivO3CPU
elif [[ "$CPU_TYPE" == "OoOasInO" ]]; then
    cputype=DerivO3CPU
elif [[ "$CPU_TYPE" == "InO" ]]; then
    cputype=X86MinorCPU
else
    echo "Unsupported CPU Type $CPU_TYPE"
fi
echo $cputype
# Actually launch gem5!
if [ -n "$fastforwardinsts" ] && [ -n "$warmupinsts" ]; then
    echo "Simpoints"
    $GEM5_DIR/build/"$ISA"/gem5.opt --debug-flags=BranchOutcomes --debug-file=${BENCHMARK}_branchtrace --outdir=$OUTPUT_DIR $GEM5_DIR/MTP/se.py --fast-forward $fastforwardinsts --standard-switch $warmupinsts --warmup-insts $warmupinsts --maxinsts $maximuminsts --cpu-type=$cputype --cpu-clock $cpuclock --caches --l1i_size $l1isize --l1i_assoc $l1iassoc --l1d_size $l1dsize --l1d_assoc $l1dassoc --l2cache --mem-size $memsize --benchmark=$BENCHMARK --benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
else
    echo "No Simpoints"
    # $GEM5_DIR/build/"$ISA"/gem5.opt --debug-flags=BranchOutcomes --debug-file=${BENCHMARK}_branchtrace --outdir=$OUTPUT_DIR $GEM5_DIR/MTP/se.py --maxinsts $maximuminsts --cpu-type=DerivO3CPU --cpu-clock $cpuclock --caches --l1i_size $l1isize --l1i_assoc $l1iassoc --l1d_size $l1dsize --l1d_assoc $l1dassoc --l2cache --mem-size $memsize --benchmark=$BENCHMARK --benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
    # $GEM5_DIR/build/"$ISA"/gem5.opt --debug-flags=O3CPUAll --debug-file=${BENCHMARK}_O3CPUAlltraceInOaftersquashing --outdir=$OUTPUT_DIR $GEM5_DIR/MTP/se.py --maxinsts $maximuminsts --cpu-type=DerivO3CPU --cpu-clock $cpuclock --caches --l1i_size $l1isize --l1i_assoc $l1iassoc --l1d_size $l1dsize --l1d_assoc $l1dassoc --l2cache --mem-size $memsize --benchmark=$BENCHMARK --benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
    $GEM5_DIR/build/"$ISA"/gem5.opt --outdir=$OUTPUT_DIR $GEM5_DIR/MTP/se.py --maxinsts $maximuminsts --cpu-type=$cputype --cpu-clock $cpuclock --caches --l1i_size $l1isize --l1i_assoc $l1iassoc --l1d_size $l1dsize --l1d_assoc $l1dassoc --l2cache --mem-size $memsize --benchmark=$BENCHMARK --benchmark_stdout=$OUTPUT_DIR/$BENCHMARK.out --benchmark_stderr=$OUTPUT_DIR/$BENCHMARK.err | tee -a $SCRIPT_OUT
fi

if [ -n "$RecordBranchOutcomes" ]; then
    echo "Extracting trace"
    # Output file to store extracted values
    output_file="$OUTPUT_DIR/${BENCHMARK}_branchoutcomes.txt"

    # Ensure the output file is empty initially
    > "$output_file"

    # Loop through each line in the input file
    while IFS= read -r line; do
        # Use grep and sed to extract the values and store them in variables
        # branch_pc=$(echo "$line" | grep -o '0x[0-9a-fA-F]\+,' | sed 's/,//')
        # target_address=$(echo "$line" | grep -o '0x[0-9a-fA-F]\+$')

        branch_pc=$(echo "$line" | awk -F ': ' '{print $3}')
        target_address=$(echo "$line" | awk -F ': ' '{print $4}')
        branch_direction=$(echo "$line" | awk -F ': ' '{print $5}')

        # Append the extracted values to the output file
        echo "$branch_pc $target_address $branch_direction" >> "$output_file"
    done < $OUTPUT_DIR/${BENCHMARK}_branchtrace
else
    echo "Not Extracting trace"
fi

end=$(date +%s)
# echo "Elapsed Time: $(($end - $start)) seconds" > $OUTPUT_DIR/time_elapsed
duration=$SECONDS
echo "$(($duration / 3600)) hours, $(($duration / 60)) minutes and $(($duration % 60)) seconds" > $OUTPUT_DIR/time_elapsed
