#!/bin/bash

# Compute p(e|m)
for language in "$@"; do
    mkdir -p generated/$language
    # Create wikipedia_p_e_m.txt
    python3 data_gen/gen_p_e_m/gen_p_e_m_from_wiki.py -l $language
done

# Merge probabilities tables
python3 data_gen/gen_p_e_m/merge_crosswikis_wiki.py -l1 $1 -l2 $2 -l3 $3
python3 data_gen/gen_p_e_m/merge_crosswikis_wiki.py -l1 $2 -l2 $3 -l3 $1
python3 data_gen/gen_p_e_m/merge_crosswikis_wiki.py -l1 $3 -l2 $1 -l3 $2
