import argparse, json
from urllib.parse import unquote
import spacy

ap = argparse.ArgumentParser()

ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
args = ap.parse_args()

exec(open("utils/utils.py").read())
exec(open("data_gen/parse_wiki_dump/parse_wiki_dump_tools.py").read())
exec(open("entities/ent_name2id_freq/e_freq_index.py").read())

print("Calculating the canonical words ....")

num_lines = 0
num_valid_ents = 0
num_error_ents = 0 # Probably list or disambiguation pages.

empty_valid_ents = get_map_all_valid_ents()

cur_words = ''
cur_ent_wikiid = '-1'

with open('generated/' + args.language + '/wiki_canonical_words.txt','w', encoding="utf-8") as out:
    with open('wiki_data/' + args.language + '/' + args.language + '-wikidataid-TextWithAnchorsFromAllWikipedia.txt', encoding="utf-8") as inp:
        for line in inp:
            line = unquote(line.strip())
            num_lines += 1
            if num_lines % 5000000 == 0:
                print('Processed ' + str(num_lines) + ' lines. Num valid ents = ' + str(num_valid_ents) + '. Num errs = ' + str(num_error_ents))

            if (line.find('<doc id="') == -1) and (line.find('</doc>') == -1):
                _, text, _, _ , _ , _ = extract_text_and_hyp(line, False)
                #TODO: improve split
                words = split_sentence_in_words(text)
                cur_words += ' '.join(words) + ' '
            elif line.find('<doc id="') > -1:
                if (cur_ent_wikiid != '-1' and cur_words != ''):
                    if cur_ent_wikiid != unk_ent_wikiid and is_valid_ent(cur_ent_wikiid):
                        out.write( cur_ent_wikiid + '\t' + get_ent_name_from_wikiid(cur_ent_wikiid) + '\t' + cur_words + '\n' )
                        empty_valid_ents.append(cur_ent_wikiid)
                        num_valid_ents += 1
                    else:
                        num_error_ents += 1

                cur_ent_wikiid = extract_page_entity_title(line)
                cur_words = ''

print('    Done extracting text only from Wiki dump. Num valid ents = ' + str(num_valid_ents) + '. Num errs = ' + str(num_error_ents))

print('Create file with all entities with empty Wikipedia pages.')
empty_ents = {}
for ent_wikiid in empty_valid_ents:
    empty_ents[ent_wikiid] = get_ent_freq(ent_wikiid)

empty_ents = {k: v for k, v in sorted(empty_ents.items(), key=lambda item: item[1], reverse=True)}

with open('generated/' + args.language + '/empty_page_ents.txt','w', encoding="utf-8") as out:
    for ent_wikiid in empty_ents:
        out.write( ent_wikiid + '\t' + get_ent_name_from_wikiid(ent_wikiid) + '\t' + str(empty_ents[ent_wikiid]) + '\n' )

print('    Done')
