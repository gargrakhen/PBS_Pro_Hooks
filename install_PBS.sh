#This script will take an argument to automatically configure the address of the PBS server
if [ -z "$1" ]; then
	echo "No hostname specified."
	echo "Usage: install_pbs.sh HOSTNAME"
	exit 1
fi
export PBS_SERVER=$1

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." 
   exit 1
fi

useradd --system -m pbsdata
curl -O -L https://github.com/PBSPro/pbspro/releases/download/v18.1.3/pbspro_18.1.3.centos7.zip
if ! hash unzip 2>/dev/null; then
	yum -y install unzip
fi
unzip pbspro_18.1.3.centos7.zip
cd pbspro_18.1.3.centos7
yum -y install pbspro-execution-18.1.3-0.x86_64.rpm

systemctl enable pbs
systemctl start pbs