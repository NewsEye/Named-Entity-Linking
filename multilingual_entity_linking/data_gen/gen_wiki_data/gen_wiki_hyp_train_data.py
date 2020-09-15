import argparse, json
from urllib.parse import unquote
import spacy

ap = argparse.ArgumentParser()

ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
args = ap.parse_args()

exec(open("utils/utils.py").read())
exec(open("data_gen/parse_wiki_dump/parse_wiki_dump_tools.py").read())
exec(open("data_gen/indexes/load_p_e_m.py").read())

print('Generating training data from Wiki dump')

num_lines = 0
num_valid_hyp = 0

cur_words_num = 0
cur_words = []
cur_mentions = {}
cur_mentions_num = 0
cur_ent_wikiid = '-1'

with open('generated/' + args.language + '/wiki_hyperlink_contexts.csv','w', encoding="utf-8") as out:
    with open('wiki_data/' + args.language + '/' + args.language + '-wikidataid-TextWithAnchorsFromAllWikipedia.txt', encoding="utf-8") as inp:
        for line in inp:
            line = unquote(line.strip())
            num_lines += 1
            if num_lines % 5000000 == 0:
                print('Processed ' + str(num_lines) + ' lines. Num valid hyp = ' + str(num_valid_hyp))

            if (line.find('<doc id="') == -1) and (line.find('</doc>') == -1):
                list_hyp, text, _, _ , _ , _ = extract_text_and_hyp(line, True)
                #TODO: improve split()
                words_on_this_line = split_sentence_in_words(text)
                num_added_hyp = 0
                line_mentions = {}
                for w in words_on_this_line:
                    wstart = string_starts(w, 'MMSTART')
                    wend = string_starts(w, 'MMEND')
                    if (not wstart) and (not wend):
                        cur_words.append(w)
                        cur_words_num += 1
                    elif wstart:
                        mention_idx = int(w[len('MMSTART'):])
                        line_mentions[mention_idx] = {}
                        line_mentions[mention_idx]['start_off'] = cur_words_num + 1
                        line_mentions[mention_idx]['end_off'] = -1
                    elif wend:
                        num_added_hyp += 1
                        mention_idx = int(w[len('MMEND'):])
                        line_mentions[mention_idx]['end_off'] = cur_words_num

                for mention in list_hyp:
                    cur_mentions_num += 1
                    cur_mentions[cur_mentions_num] = {}
                    cur_mentions[cur_mentions_num]['mention'] = mention
                    cur_mentions[cur_mentions_num]['ent_wikiid'] = list_hyp[mention]['ent_wikiid']
                    cur_mentions[cur_mentions_num]['start_off'] = line_mentions[ list_hyp[mention]['cnt'] ]['start_off']
                    cur_mentions[cur_mentions_num]['end_off'] = line_mentions[ list_hyp[mention]['cnt'] ]['end_off']

            elif line.find('<doc id="') > -1:
                if cur_ent_wikiid != unk_ent_wikiid and is_valid_ent(cur_ent_wikiid):
                    header = cur_ent_wikiid + '\t' + get_ent_name_from_wikiid(cur_ent_wikiid) + '\t'

                    for idx in cur_mentions:
                        if cur_mentions[idx]['mention'] in ent_p_e_m_index and len(ent_p_e_m_index[ cur_mentions[idx]['mention'] ]) > 0:
                            text = header + cur_mentions[idx]['mention'] + '\t'

                            left_ctxt = []
                            for i in range(max(0, cur_mentions[idx]['start_off'] - 100), cur_mentions[idx]['start_off'] - 1):
                                left_ctxt.append(cur_words[i])

                            if len(left_ctxt) == 0:
                                left_ctxt.append('EMPTYCTXT')

                            text += ' '.join(left_ctxt) + '\t'

                            right_ctxt = []
                            for i in range(cur_mentions[idx]['end_off'], min( cur_words_num, cur_mentions[idx]['end_off'] + 100 )):
                                right_ctxt.append(cur_words[i])

                            if len(right_ctxt) == 0:
                                right_ctxt.append('EMPTYCTXT')

                            text += ' '.join(right_ctxt) + '\tCANDIDATES\t'

                            #-- Entity candidates from p(e|m) dictionary
                            unsorted_cand = {}
                            for ent_wikiid in ent_p_e_m_index[ cur_mentions[idx]['mention'] ]:
                                unsorted_cand[ent_wikiid] = ent_p_e_m_index[ cur_mentions[idx]['mention'] ][ent_wikiid]

                            unsorted_cand = {k: v for k, v in sorted(unsorted_cand.items(), key=lambda item: item[1], reverse=True)}

                            candidates = []
                            gt_pos = -1
                            for pos, ent_wikiid in enumerate(unsorted_cand):
                                if pos <= 32:
                                    candidates.append( ent_wikiid + ',' + format(unsorted_cand[ent_wikiid], '.3f') + ',' + get_ent_name_from_wikiid(ent_wikiid) )
                                    if ent_wikiid == cur_mentions[idx]['ent_wikiid']:
                                        gt_pos = pos
                                else:
                                    break

                            text += '\t'.join(candidates) + '\tGT:\t'

                            if gt_pos > 0:
                                num_valid_hyp += 1
                                out.write(text + str(gt_pos) + ',' + candidates[gt_pos] + '\n')

                cur_ent_wikiid = extract_page_entity_title(line)
                cur_words = []
                cur_words_num = 0
                cur_mentions = {}
                cur_mentions_num = 0

print('    Done generating training data from Wiki dump. Num valid hyp = ' + str(num_valid_hyp))
