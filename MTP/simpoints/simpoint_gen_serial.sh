#!/bin/bash
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
	valgrind --tool=exp-bbv --interval-size=$interval ./$execute $argument
else
	valgrind --tool=exp-bbv --interval-size=$interval ./$execute $argument < $filein
fi
mv bb.out.* ../../../
cd ../../../
./bin/simpoint -maxK $maxk -loadFVFile bb.out.* -saveSimpoints simpoints -saveSimpointWeights weights

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
' simpoints weights > simpoint_output.temp

cut --complement -d' ' -f3 simpoint_output.temp > simpoint_output
intcompact=$((($interval)/1000000))
#resultdir=${benchmark%/*}
rm simpoints weights simpoint_output.temp bb.out.*
mkdir -p simpoint_results/$resultdir/${intcompact}M/
mv simpoint_output ./simpoint_results/$resultdir/${intcompact}M/
