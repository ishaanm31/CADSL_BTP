#!/bin/bash

while getopts i:k: flag
do
	case "${flag}" in
		i) interval=${OPTARG};;
		k) maxk=${OPTARG};;
	esac
done

./simpoint_gen.sh -b cpu2006/400.perlbench/perlbench -a 'splitmail.pl 1600 12 26 16 4500' -k $maxk -i $interval 
./simpoint_gen.sh -b cpu2006/401.bzip2/bzip2 -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/403.gcc/gcc -a 200.in -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/410.bwaves/bwaves -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/416.gamess/gamess -f cytosine.2.config -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/429.mcf/mcf -a inp.in -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/433.milc/milc -f su3imp.in -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/434.zeusmp/zeusmp -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/435.gromacs/gromacs -a '-nice 0 -deffnm gromacs -silent' -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/436.cactusADM/cactusADM -a benchADM.par -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/437.leslie3d/leslie3d -f leslie3d.in -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/444.namd/namd -a '--input namd.input --iterations 38' -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/445.gobmk/gobmk -a '--mode gtp' -f 13x13.tst -k $maxk -i $interval
#./simpoint_gen.sh -b cpu2006/447.dealII/dealII -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/450.soplex/soplex -a pds-50.mps -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/453.povray/povray -a SPEC-benchmark-ref.ini -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/454.calculix/calculix -a hyperviscoplastic -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/456.hmmer/hmmer -a nph3.hmm -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/458.sjeng/sjeng -a ref.txt -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/459.GemsFDTD/GemsFDTD -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/462.libquantum/libquantum -a '1397 8' -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/464.h264ref/h264ref -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/465.tonto/tonto -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/470.lbm/lbm -a '3000 reference.dat 0 0 100_100_130_ldc.of' -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/471.omnetpp/omnetpp -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/473.astar/astar -a BigLakes2048.cfg -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/481.wrf/wrf -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/482.sphinx3/sphinx_livepretend -a 'ctlfile . args.an4' -k $maxk -i $interval
./simpoint_gen.sh -b cpu2006/483.xalancbmk/Xalan -a 't5.xml xalanc.xsl' -k $maxk -i $interval
