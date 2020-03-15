#!/bin/bash

python train.py
python probs_and_symbols.py
python G.py
fstcompile --isymbols=syms.txt --osymbols=syms.txt G.txt G.fst
python I.py
fstcompile --isymbols=syms.txt --osymbols=syms.txt I.txt I.fst
python A1.py
fstcompile --isymbols=syms.txt --osymbols=syms.txt A1.txt A1.fst
fstrmepsilon A1.fst | fstdeterminize | fstminimize >A1_opt.fst
python A2.py
fstcompile --isymbols=syms.txt --osymbols=syms.txt A2.txt A2.fst
fstrmepsilon A2.fst | fstdeterminize | fstminimize >A2_opt.fst
fstunion A1_opt.fst A2_opt.fst A1and2.fst
fstunion G.fst I.fst GandI.fst
fstclosure GandI.fst closure.fst
fstarcsort A1and2.fst A1and2.fst
fstcompose closure.fst A1and2.fst T.fst
fstarcsort T.fst T.fst
python accuracy.py
python otrain.py
python oI.py
fstcompile --isymbols=syms.txt --osymbols=syms.txt oI.txt oI.fst
python oE.py
fstcompile --isymbols=syms.txt --osymbols=syms.txt oE.txt oE.fst
fstclosure oI.fst oI*.fst
fstconcat oI*.fst oE.fst out.fst
fstconcat out.fst oI*.fst oS1.fst
fstarcsort oS1.fst oS1.fst
fstcompose oS1.fst oS1.fst oS2.fst
python oaccuracy1.py
python oaccuracy2.py
fstcompose T.fst oS1.fst T.fst
python accuracy.py