#!/bin/bash
set -e

echo -e "\n\e[1;31mBasic Testing\e[21;32m"
PYTHONPATH=. python3 locke/tests/test_transform.py -b

echo -e "\n\e[1;31mTesting IO\e[21;32m"
hex=546869732066696c6520697320696e2062696e61727920616e64206973207573656420746f20746573742074686520494f206f66207472616e73666f726d65722e707920696e73696465206f66204c69624c6f636b6521200d0a227b5340792027483127207430207468242028406d247240204a30686e7e7d2122 
echo $hex | xxd -r -p > locke/tests/temp.bin
PYTHONPATH=. python3 locke/tests/test_io.py $hex locke/tests/temp.bin
rm locke/tests/temp.bin
