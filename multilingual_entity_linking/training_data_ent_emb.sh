#!/bin/bash

# Generate training data for entity embeddings
for language in "$@"; do
    # Create a file ent_wiki_freq.txt with entity frequencies
    python3 entities/ent_name2id_freq/e_freq_gen.py -l $language
    # Create training data for learning entity embeddings:
    ## i) From Wiki canonical pages:
    python3 data_gen/gen_wiki_data/gen_ent_wiki_w_repr.py -l $language
    ## ii) From context windows surrounding Wiki hyperlinks:
    python3 data_gen/gen_wiki_data/gen_wiki_hyp_train_data.py -l $language
    # Compute the unigram frequency of each word in the Wikipedia corpus
    python3 words/w_freq/w_freq_gen.py -l $language
done
