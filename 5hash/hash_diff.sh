#1 /bin/bash

#cant handle long int/binaries
declare -A HASH_DICT
HASH_DICT+=( ["md5sum"]=128
             ["sha1sum"]=160
             ["sha224sum"]=224
             ["sha256sum"]=256
             ["sha384sum"]=384
             ["sha512sum"]=512 )

declare -a ORDER
ORDER+=( "md5sum" "sha1sum" "sha224sum" "sha256sum" "sha384sum" "sha512sum" )


echo -e "Wykonane polecenia i wyniki:\n\n" >> hash.txt

for key in ${ORDER[@]}; do
  echo $key ${HASH_DICT[$key]}
  cat hash.pdf personal.txt | md5sum >> hash1.txt
  cat hash.pdf personal_.txt | md5sum >> hash2.txt
  hash1=($(<hash1.txt))
  hash2=($(<hash2.txt))
  int1=$(echo "obase=2;ibase=16;${hash1^^}" | BC_LINE_LENGTH=0 bc)
  echo $int1
  int2=$(echo "obase=2;ibase=16;${hash2^^}" | BC_LINE_LENGTH=0 bc)
  echo $int2
  XOR=$(( int1 ^ int2 )) #OVERFLOW
  echo $XOR
  bin=$(echo "ibase=10;obase=2;${XOR}" | BC_LINE_LENGTH=0 bc)
  echo $bin
  count=0
  while [ $bin -gt 0 ]; do
    count=$((count+1))
    bin=$(( bin & (bin-1) ))
  done
  echo $count
done


echo -e "cat hash.pdf personal.txt | md5sum >> hash.txt\ncat hash.pdf personal_.txt | md5sum >> hash.txt" >> hash.txt


#bin=$(echo "ibase=16;obase=2;${hash^^}" | BC_LINE_LENGTH=0 bc)
#bin1=$(echo "ibase=16;obase=2;${hash1^^}" | BC_LINE_LENGTH=0 bc)

#xor hash1.txt hash.txt > xor.txt
#counter++ for each xor.txt binshift
#echo -e "Liczba bitow rozniaca wyniki: {$counter} czyli {((counter/128*100))}" >> hash.txt
