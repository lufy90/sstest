#!/bin/bash
# ltp test


SITE=https://github.com/linux-test-project/ltp/releases/
URL=http://tfs.i-soft.com.cn/TestRepos/TestTools/LTP/ltp-full-20180926.tar.bz2
TAR=ltp-full-20180926.tar.bz2
VER=${TAR:9:8}
TARGET=/tmp/ltp$VER
RESULTS=/tmp/

get_tar() {
	echo 192.168.45.3	tfs.i-soft.com.cn >> /etc/hosts
	local tar=$TAR
	local url=$URL
	[ -f $tar ] || \
	{
		wget $url || \
		{
			echo "ERROR: cannot get $tar from $url"
			exit 1
		}
	}
	wget $url.md5
	local md5=`md5sum $tar | cut -d ' ' -f 1`
	local expmd5=`cat $tar.md5 | cut -d ' ' -f 1`
	#echo $md5
	#echo $expmd5
	if [ $md5 != "$expmd5" ] ; then
		echo "WARN: failed check $tar md5sum."
	fi
}

install(){
	get_tar
	local tar=$TAR
	local target=$TARGET
	tar xf $tar || \
		{
			echo "ERROR: tar xf $tar"
			exit 1
		}
	cd ${tar%%.*} || \
		{
			echo "ERROR: cd ${tar%%.*}"
			exit 1
		}
	echo "Now configure ltp ..."
	./configure --prefix=$target &> configure.out || \
		{
			echo "ERROR: configure \
			       	--prefix=/opt/ltp${tar:8:9}"
			exit 1
		}
	echo "Now make ltp ..."
	make &> make.out || \
		{
			echo "ERROR: make"
			exit 1
		}
	echo "Now make install ltp ..."
	make install &> make_install.out || \
		{
			echo "ERROR: make install"
			echo "Output are redirected to xxxxxxxxxxx"
			exit 1
		}
}

install_from_src(){
	local vers=
}

start_service(){
	for i
	do
		systemctl start $i &> /dev/null || \
		       	{
			        service $i start &> /dev/null || \
					echo "ERROR: cannot start $i"
	                }
	done
}

runstress(){
	local t=$1
	local target=$TARGET
	local results=$RESULTS
	[ -z $t ] && \
		{
			echo "You need to specify test duration."
			echo "e.g: $0 stress 24"
			exit 2
		}
	[ -f $target/testscripts/ltpstress.sh ] || \
		{
			echo "ERROR: check ltpstress.sh failed, please ensure ltp is installed correctly."
			echo "WARN: please notice that ltpstress.sh has been deprecated after the version 20180926 !"
			exit 2
		}
	[ -f /bin/exportfs ] || ln /usr/sbin/exportfs /bin/
	[ -f /bin/rpc.nfsd ] || ln /usr/sbin/rpc.nfsd /bin/
	echo -ne 'rsh\nrlogin\nrexec' >> /etc/securetty
	echo localhost >> /root/.rhosts
	setenforce 0
	start_service rsh.socket rlogin.socket
	cd $target || \
		{
			echo "ERROR: cd $target failed."
			exit 2
		}
	[ -d $results ] || mkdir $results
	./testscripts/ltpstress.sh -d $results/sar.out.0 \
		-l $results/stress.log.0 -p -q \
		-t $t -S &> $results/stress.out.0 &
	echo "ltpstress is running ...."
	echo "ps -ef | grep stress "
	ps -ef | grep stress
}

runtests(){
	local target=$TARGET
        local results=$RESULTS
	cd $target || \
                {
                        echo "ERROR: cd $target failed."
                        exit 2
                }
	[ -d $results ] || mkdir $results
	./runltp &> $results/runltp.out &
	echo "runltp is running ...."
	echo "See ps -ef | grep ltp"

}


usage(){
	cat << eof
usage: $0 <OPTION>
OPTION:
    install  install ltp
    test     run default ltp test
    stress N run ltpstress test for N hours
    help     show usage
eof
}


main(){
	case $1 in
		"install")
			install ;;
		"test")
			runtest ;;
		"stress")
			shift
			runstress $1 ;;
		"-h")
			usage ;;
		"--help") 
			usage ;;
		"help")
			usage ;;
		""|* )
			usage ;;
		esac
}

main install
