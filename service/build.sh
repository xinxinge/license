#!/bin/bash
APPNAME=ims3d
WEBROOT=webui
BINROOT=service

# get version
VERSTR=`grep VERSION_NUM $BINROOT/common/const.py | cut -d'=' -f2`
VERSIONVAR=${VERSTR:-2.0}
VERSIONVAR=${VERSIONVAR## }
createdate=`date +%Y%m%d`
BUILDROOT=`mktemp -d`
BINDST=$BUILDROOT/$BINROOT

case $2 in
    "full")
        apptype=full
        ;;
    *)
        apptype=upgrade
        ;;
esac
case $1 in
    "win")
        os=Windows
        PKGNAME=$APPNAME-$apptype-$VERSIONVAR-$createdate.tgz
        # python3
        COMPCMD="env WINEDEBUG=-msvcrt wine python ./setup.py build_ext --compiler=mingw32"
        BINSRC=$BINROOT/build/lib.win-amd64-3.7
        PKGCMD="tar czf $PKGNAME -C $BUILDROOT ."
        ;;
    *)
        os=Linux
        PKGNAME=$APPNAME-$apptype-$VERSIONVAR-$createdate.sh
        BINSRC=$BINROOT/build/lib.linux-x86_64-3.5
        COMPCMD="python ./setup.py build_ext"
        PKGCMD="makeself -q $BUILDROOT $PKGNAME \"$APPNAME Ver: $VERSIONVAR\" ./setup.sh $os"
        ;;
esac
echo "======================================"
echo "Building $os $apptype package" 
echo "======================================"
read -p "Continue[y]?" input
case "${input:0:1}" in
    "Y" | "y")
        ;;
    *)
        echo "Quit"
        exit
        ;;
esac

echo "Compiling webui ......"
WEBSRC=$WEBROOT/dist
WEBDST=$BUILDROOT/$WEBROOT
cd $WEBROOT && npm run build:prod && cd ..
if [ $? -ne 0 ]; then
    echo "Failed"
    exit
fi
if [ -e $WEBDST ]; then
    rm -rf $WEBDST
fi
cp -af $WEBSRC $WEBDST

echo "Compiling service ......"
#if [ -e $BINROOT/build ]; then
#    rm -rf $BINROOT/build
#fi
cd $BINROOT && ${COMPCMD} && cd ..
if [ $? -ne 0 ]; then
    echo "Failed"
    exit
fi
cp -af $BINSRC $BINDST
# copy __init__.py
initlist=`find $BINROOT -name "__init__.py"`
for py in $initlist; do
    echo "$py ==> $BUILDROOT/$py"
    cp $py $BUILDROOT/$py
done
if [ "x$os" == "xLinux" ]; then
    find $BINDST -name "*.so" -exec strip -s {} +
fi
cp $BINROOT/config.yaml $BINDST/

echo -n "Creating $apptype package ......"
${PKGCMD}
echo "done"

echo -n "Cleaning ......"
#rm -rf $BUILDROOT
echo $BUILDROOT
echo "done"

echo "========================================"
echo "IMS3D package: ./$PKGNAME"
echo "========================================"

