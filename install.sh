#!/bin/sh

if [ -z "$1" ]
 then
  echo "Try --help"
  exit
fi

while test $# -gt 0; do
  case "$1" in
    -h|--help)
        echo "Downloads and installs the factorio headless server binaries from the official webside www.factorio.com"
        echo "--update=VERSION       specify a version to install"
        echo "--latest               download the latest version"
        exit
        ;;
    --update)
        echo "Try --help."
        shift
        exit
        ;;
    --update*)
        export VERSION=`echo $1 | sed -e 's/^[^=]*=//g'`
        shift
        break
        ;;
    --latest)
        VERSION="latest"
        shift
        break
        ;;
    *)
        echo "Try --help"
        exit
  esac
done

if [ -z "$VERSION" ]
  then
    echo "Version expected."
    exit
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
[ -e factorio.tar.xz ] && rm factorio.tar.xz
curl -JL https://www.factorio.com/get-download/$VERSION/headless/linux64 -o factorio.tar.xz

if [ -e factorio.tar.xz ]
 then
  file_size=$(stat --printf="%s" factorio.tar.xz)
  if [ "$file_size" -gt "100000" ]
   then
    tar -xJf factorio.tar.xz
    #[ ! -e backup ] && mkdir backup
    [ -e backup/bin_backup ] && rm -rf backup/bin_backup
    [ -e backup/data_backup ] && rm -rf backup/data_backup
    [ -e bin ] && mv bin backup/bin_backup
    [ -e data ] && mv data backup/data_backup
    mv factorio/bin bin
    mv factorio/data data
    rm -rf factorio
    rm factorio.tar.xz
    echo "Version $VERSION successfully installed."
    exit
  fi
fi
echo "Installation failed. Possible invalid version: $VERSION."

