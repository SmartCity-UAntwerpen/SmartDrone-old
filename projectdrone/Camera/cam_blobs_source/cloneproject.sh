

if [ "$#" -ne 2 ]; then
	echo "Invalid syntax"
	echo "Copies the rpi-irpos-template project to a new location with a new name"
	echo "param 1: path to new location"
	echo "param 2: new project name"
	exit -1
fi

mkdir $1 || true
cp -rf * $1
cd $1
make clean
sed -i s/rpi-irpos-template/$2/g rpi-irpos-template.cbp
sed -i s/rpi-irpos-template/$2/g rpi-irpos-template.project
sed -i s/rpi-irpos-template/$2/g Makefile
sed -i s/rpi-irpos-template/$2/g cloneproject.sh
mv rpi-irpos-template.cbp $2.cbp
mv rpi-irpos-template.project $2.project
rm -f *~ || true
rm -f *.workspace || true
rm -f *.layout || true
echo "DONE"

