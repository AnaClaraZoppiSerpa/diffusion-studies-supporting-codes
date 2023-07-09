for key in {0..255}
do
    echo "key $key"
   # python3 ddt3_fix_2.py $key 1 2 3 > $key-123.txt
   # python3 ddt3_fix_2.py $key 2 3 4 > $key-234.txt
   # python3 ddt3_fix_2.py $key 3 4 5 > $key-345.txt
   # python3 ddt3_fix_2.py $key 4 5 6 > $key-456.txt
    python3 ddt3_fix_2.py $key 5 6 7 > $key-567.txt
    echo "done 567"
    python3 ddt3_fix_2.py $key 6 7 8 > $key-678.txt
    echo "done 678"
    python3 ddt3_fix_2.py $key 7 8 1 > $key-781.txt
    echo "done 781"
    python3 ddt3_fix_2.py $key 8 1 2 > $key-812.txt
    echo "done 812"
done
