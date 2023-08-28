#!/bin/bash
start=$(date +%s)
filein="null"
maxk=30
count=0
while getopts b:a:f:i:k: flag
do
	case "${flag}" in
		b) benchmark=${OPTARG};;
		a) argument=${OPTARG};;
		f) filein=${OPTARG};;
		i) interval=${OPTARG};;
		k) maxk=${OPTARG};;
	esac
done

#echo ./benchmarks/$benchmark $argument
resultdir=${benchmark%/*}
execute=${benchmark##*/}
echo ./$execute ${argument}
cd benchmarks/$resultdir
#gedit 13x13.tst
#~/sniper/record-trace -o vector -b $interval -- $path $argument
if [ $filein == "null" ]
then
	valgrind --tool=exp-bbv --interval-size=$interval --bb-out-file=bb.out.$execute ./$execute $argument
else
	valgrind --tool=exp-bbv --interval-size=$interval --bb-out-file=bb.out.$execute ./$execute $argument < $filein
fi
mv bb.out.$execute ../../../
cd ../../../
./bin/simpoint -maxK $maxk -loadFVFile bb.out.$execute -saveSimpoints simpoints.$execute -saveSimpointWeights weights.$execute

#while IFS= read -r line; do
    #echo "Text read from file: $line"
#done < simpoints

#while read word _; do 
#	var=$word
#	skip=$((($var-1)*$interval))
#	name="trace$count"
#	~/sniper/record-trace -o $name -f $skip -d $interval -- $path $argument 
#	#printf '%s\n' "$name"
#	count=$(($count+1))
#done < simpoints

awk '
    BEGIN { FS=OFS=" " }
    NR==FNR { a[NR]=$0; next }
    {
        split(a[FNR],f)
        for (i=1;i<=NF;i++) {
            printf "%s%s%s%s", f[i], OFS, $i, (i<NF?OFS:ORS)
        }
    }
' simpoints.$execute weights.$execute > simpoint_output.$execute.temp

cut --complement -d' ' -f3 simpoint_output.$execute.temp > simpoint_output.$execute
intcompact=$((($interval)/1000000))
#resultdir=${benchmark%/*}
rm simpoints.$execute weights.$execute simpoint_output.$execute.temp bb.out.$execute
mkdir -p simpoint_results/$resultdir/${intcompact}M/
mv simpoint_output.$execute ./simpoint_results/$resultdir/${intcompact}M/
end=$(date +%s)
echo "Elapsed Time: $(($end - $start)) seconds" > ./simpoint_results/$resultdir/${intcompact}M/time_elapsed
