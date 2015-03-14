#!/bin/sh
#Count the lines of code in the project
# cd to the directory where this file is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo  
echo ----------------------------------------
echo Obj-C
echo ----------------------------------------
echo  

find . \( -iname \*.m -o -iname \*.mm -o -iname \*.c -o -iname \*.cc -o -iname \*.h -o -iname \*.hpp -o -iname \*.cpp -o -iname \*.hh \) -not \( -ipath "*/LiveSDK/*" -o -ipath "*/GooglePlus.framework/*" -o -ipath "*/FacebookSDK.framework/*" -o -ipath "*/GoogleOpenSource.framework/*" \) -exec wc -l '{}' \+

echo  
echo ----------------------------------------
echo Swift
echo ----------------------------------------
echo  

find . \( -iname \*.swift \) -exec wc -l '{}' \+

echo  
echo ----------------------------------------
echo Python
echo ----------------------------------------
echo  

find . \( -iname \*.py \) -exec wc -l '{}' \+

echo  
echo ----------------------------------------
echo Java
echo ----------------------------------------
echo  

read -n1 -r -p "Press any key to continue..." key