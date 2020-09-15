import argparse, os
from urllib.parse import unquote
import os.path
from os import path
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
args = ap.parse_args()

exec(open("utils/utils.py").read())
exec(open("data_gen/parse_wiki_dump/parse_wiki_dump_tools.py").read())

print('Computing Wikipedia p_e_m')

wiki_e_m_counts = {}
num_lines = 0
parsing_errors = 0
list_ent_errors = 0
diez_ent_errors = 0
disambiguation_ent_errors = 0
num_valid_hyperlinks = 0

with open('wiki_data/' + args.language + '/' + args.language + '-wikidataid-TextWithAnchorsFromAllWikipedia.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        num_lines += 1
        if num_lines % 5000000 == 0:
            print('Processed ' + str(num_lines) + ' lines. Parsing errs = ' +\
                str(parsing_errors) + ' List ent errs = ' + \
                str(list_ent_errors) + ' diez errs = ' + str(diez_ent_errors) +\
                ' disambig errs = ' + str(disambiguation_ent_errors) + \
                ' . Num valid hyperlinks = ' + str(num_valid_hyperlinks))

        if not '<doc id="' in line:
            list_hyp, text, le_errs, p_errs, dis_errs, diez_errs = extract_text_and_hyp(line, False)
            parsing_errors += p_errs
            list_ent_errors += le_errs
            disambiguation_ent_errors += dis_errs
            diez_ent_errors += diez_errs
            for el in list_hyp:
                mention = el
                ent_wikiid = list_hyp[el]['ent_wikiid']

                num_valid_hyperlinks += 1

                if mention not in wiki_e_m_counts:
                    wiki_e_m_counts[mention] = {}
                if ent_wikiid not in wiki_e_m_counts[mention]:
                    wiki_e_m_counts[mention][ent_wikiid] = 0
                wiki_e_m_counts[mention][ent_wikiid] += 1

print('    Done computing Wikipedia p(e|m). Num valid hyperlinks = ', num_valid_hyperlinks)

print('Now sorting and writing ..')
with open('generated/' + args.language + '/wikipedia_p_e_m.txt', "w", encoding="utf-8") as f:
    for mention in wiki_e_m_counts:
        tbl = {}
        for ent_wikiid in wiki_e_m_counts[mention]:
            tbl[ent_wikiid] = wiki_e_m_counts[mention][ent_wikiid]

        tbl = {k: v for k, v in sorted(tbl.items(), key=lambda item: item[1], reverse=True)}

        text = ''
        total_freq = 0
        for ent_wikiid in tbl:
            text += str(ent_wikiid) + ',' + str(tbl[ent_wikiid])
            text += ',' + get_ent_name_from_wikiid(ent_wikiid).replace(' ', '_') + '\t'
            total_freq = total_freq + tbl[ent_wikiid]

        f.write(mention + '\t' + str(total_freq) + '\t' + text + '\n')

print('    Done sorting and writing.')
