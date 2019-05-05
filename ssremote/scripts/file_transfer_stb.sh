#!/bin/bash

function gen()
{

local nameprefix=tst
local srcdir=$1
local count=$2
local ddcount=$3
local bs=$4

local namesuffix=0

local num=0
for i in `seq $count`
do
echo "Generating $cout ${ddcount}*${bs}: ${srcdir}/${nameprefix}_${namesuffix}..."
namesuffix=$(printf "%04d" $num)
dd if=/dev/urandom of=${srcdir}/${nameprefix}_${namesuffix} count=$ddcount bs=$bs >> ./dd.log 2>&1
num=$((num+1))
echo "Generate $cout ${ddcount}*${bs} OK: ${srcdir}/${nameprefix}_${namesuffix}"
done
}

tst_mv()
{

local gencmd="$1"
local srcdir=$2
local dstdir=$3


$gencmd
sleep 3600 &
sleep_pid1=$!
while [[ $(ps -p $sleep_pid1 -o comm=) == "sleep" ]]
do
mv $srcdir/tst_* $dstdir/
echo $(date +%Y%m%d%H%M%S) "mv from $srcdir to $dstdir OK"
mv $dstdir/tst_* $srcdir/
echo $(date +%Y%m%d%H%M%S) "mv from $dstdir to $srcdir OK"
done

rm -rf $srcdir/tst_*
rm -rf $dstdir/tst_*

}

run_tst()
{
echo "4GB file, sda2 -> sda3 ========================"
tst_mv "gen /sda2/ 1 128 32M" /sda2/ /sda3/

echo "512KB file, sda2 -> sda3 ========================"
tst_mv "gen /sda2/ 4096 1 512K"  /sda2/ /sda3/

}

run_tst
