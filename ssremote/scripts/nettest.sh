#!/bin/bash
# nettest.sh
# 20190320


server=$1

looping01()
{
  local looptimes=5
  local cmd="$1"
  local option="$2"
  local i=

  for i in $(seq $looptimes)
    do 
#     echo ${i}th test ------------------
#     echo TestCmd: "$cmd" "$option"

### bug here ###

      if [[ $i -eq 1 ]]; then
        $cmd -P1 $option
      else
        $cmd -P0 $option
      fi
      sleep 5
    done

}

looping02()
{
  local cmd="$1"
  local opt="$2"
  local i=
  for i in $opt
    do
      echo ----------------------------------------
      echo TestCMD: "$cmd" "$i"
      looping01 "$cmd" "$i"
    done
}



# global options
option1="-l20 -l40 -l60 -l80 -l100 -l120"
option2="-n2 -n4 -n6 -n8 -n16 -n32 -n64"

# test specific options
option3="-m32 -m128 -m512 -m1K -m4K -m16K"
option4="-M32 -M128 -M512 -M1K -M4K -M16K"
option5="-s1K -s128K -s512K -s1M -s4M -s16M -s32M"
option6="-S1K -S128K -S512K -S1M -S4M -S16M -S32M"

GL_TCPCMD="netperf -H $server -t TCP_STREAM"
SP_TCPCMD="netperf -H $server -t TCP_STREAM -l 30 --"

GL_UDPCMD="netperf -H $server -t UDP_STREAM"
SP_UDPCMD="netperf -H $server -t UDP_STREAM -l 30 --"

echo "************************************************"
echo "TCP_STREAM test starts ..."
echo ================================================
echo "Global options test starts ... "
looping02 "$GL_TCPCMD" "$option1"
looping02 "$GL_TCPCMD" "$option2"

echo ================================================
echo "Test-specific options test starts ... "
looping02 "$SP_TCPCMD" "$option3"
looping02 "$SP_TCPCMD" "$option4"
looping02 "$SP_TCPCMD" "$option5"
looping02 "$SP_TCPCMD" "$option6"


echo "************************************************"
echo "UDP_STREAM test starts ..."
echo ================================================
echo "Global options test starts ... "
looping02 "$GL_UDPCMD" "$option1"
looping02 "$GL_UDPCMD" "$option2"

echo ================================================
echo "Test-specific options test starts ... "
looping02 "$SP_UDPCMD" "$option3"
looping02 "$SP_UDPCMD" "$option4"
looping02 "$SP_UDPCMD" "$option5"
looping02 "$SP_UDPCMD" "$option6"





:<< commmm
echo =========================================================
echo "Global options test starts ... "
for options in $option1 $option2
do 
  for opt in $options
    do
      echo -----------------------------------------------------
      echo TestCmd: $GL_CMD $opt
      looping01 "$GL_CMD" "$opt"
    done
  done


echo =========================================================
echo "test specific options test starts ... "
for options in $option3 $option4 $option5 $option6
do 
  for opt in $options
    do 
      echo -----------------------------------------------------
      echo TestCmd: $SP_CMD $opt
      looping01 "$SP_CMD" "$opt"
    done
  done
commmm

