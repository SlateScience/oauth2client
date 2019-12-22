#!/bin/bash

rm *.pickle || echo no prior pickles

echo === first py2 run ===
python2 -c 'from test_pickle_compatibility import main; main()'
echo === first py3 run ===
python3 -c 'from test_pickle_compatibility import main; main()'
echo === second py2 run ===
python2 -c 'from test_pickle_compatibility import main; main()'
echo === second py3 run ===
python3 -c 'from test_pickle_compatibility import main; main()'

rm *.pickle
