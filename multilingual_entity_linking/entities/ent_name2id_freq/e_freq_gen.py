import argparse, json
from urllib.parse import unquote
import os.path
from os import path
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
args = ap.parse_args()

exec(open("utils/utils.py").read())
exec(open("entities/ent_name2id_freq/ent_name_id.py").read())

entity_freqs = {}
num_lines = 0
with open('generated/'+args.language+'/merge-wikipedia_p_e_m.txt', encoding="utf-8") as f:
    for line in f:
        num_lines += 1
        if num_lines % 5000000 == 0:
            print('Processed ' + str(num_lines) + ' lines. ')

        line = unquote(line.strip())
        parts = line.split('\t')
        num_parts = len(parts)
        for i in range(2, num_parts):
            ent_str = parts[i].split(',')
            ent_wikiid = ent_str[0]
            freq = int(ent_str[1])

        if ent_wikiid not in entity_freqs:
            entity_freqs[ent_wikiid] = 0

        entity_freqs[ent_wikiid] += freq

print('Sorting and writing')
sorted_ent_freq = {}
for ent_wikiid in entity_freqs:
    sorted_ent_freq[ent_wikiid] = entity_freqs[ent_wikiid]

sorted_ent_freq = {k: v for k, v in sorted(sorted_ent_freq.items(), key=lambda item: item[1], reverse=True)}

with open('generated/'+args.language+'/ent_wiki_freq.txt', "w", encoding="utf-8") as f:
    total_freq = 0
    for ent_wikiid in sorted_ent_freq:
        f.write( ent_wikiid + '\t' + get_ent_name_from_wikiid(ent_wikiid) + '\t' + str(sorted_ent_freq[ent_wikiid]) + '\n' )
        total_freq += sorted_ent_freq[ent_wikiid]

print('Total freq = ' + str(total_freq) + '\n')
