DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
curl -JL https://www.factorio.com/get-download/0.15.40/headless/linux64 -o factorio.tar.xz
tar -xJf factorio.tar.xz
rm -rf backup/bin_backup
rm -rf backup/data_backup
mv bin backup/bin_backup
mv data backup/data_backup
mv factorio/bin bin
mv factorio/data data
rm -rf factorio
rm factorio.tar.xz
