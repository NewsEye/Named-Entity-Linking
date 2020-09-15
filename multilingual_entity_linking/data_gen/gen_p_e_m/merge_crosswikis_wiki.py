import argparse, json
from urllib.parse import unquote

ap = argparse.ArgumentParser()

ap.add_argument("-l1", "--language", default='en',type = str,
   help="path")
ap.add_argument("-l2", "--language2", default='en',type = str,
   help="path")
ap.add_argument("-l3", "--language3", default='en',type = str,
   help="path")
args = ap.parse_args()

exec(open("utils/utils.py").read())
exec(open("entities/ent_name2id_freq/ent_name_id.py").read())

print('Merging Wikipedia and Crosswikis p_e_m')

print("Loading wikipedia_p_e_m file ...")
merged_e_m_counts = {}
with open('generated/' + args.language + '/wikipedia_p_e_m.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        parts = line.split("\t")
        if len(parts) > 1:
            mention = parts[0]

            if mention.find('Wikipedia') == -1 and mention.find('wikipedia') == -1:
                if mention not in merged_e_m_counts:
                    merged_e_m_counts[mention] = {}

                total = int(parts[1])
                num_ents = len(parts)
                for i in range(2, num_ents):
                    ent_str = parts[i].split(",")
                    ent_wikiid = ent_str[0]
                    freq = int(ent_str[1])

                    if ent_wikiid not in merged_e_m_counts[mention]:
                        merged_e_m_counts[mention][ent_wikiid] = 0

                    merged_e_m_counts[mention][ent_wikiid] += freq

print("    Done loading wikipedia_p_e_m file ...")

with open('generated/' + args.language2 + '/wikipedia_p_e_m.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        parts = line.split("\t")
        if len(parts) > 1:
            mention = parts[0]

            if mention.find('Wikipedia') == -1 and mention.find('wikipedia') == -1:
                if mention not in merged_e_m_counts:
                    merged_e_m_counts[mention] = {}

                total = int(parts[1])
                num_ents = len(parts)
                for i in range(2, num_ents):
                    ent_str = parts[i].split(",")
                    ent_wikiid = ent_str[0]
                    freq = int(ent_str[1])

                    if ent_wikiid not in merged_e_m_counts[mention]:
                        merged_e_m_counts[mention][ent_wikiid] = 0

                    merged_e_m_counts[mention][ent_wikiid] += freq

print("    Done loading wikipedia_p_e_m file ...")

with open('generated/' + args.language3 + '/wikipedia_p_e_m.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        parts = line.split("\t")
        if len(parts) > 1:
            mention = parts[0]

            if mention.find('Wikipedia') == -1 and mention.find('wikipedia') == -1:
                if mention not in merged_e_m_counts:
                    merged_e_m_counts[mention] = {}

                total = int(parts[1])
                num_ents = len(parts)
                for i in range(2, num_ents):
                    ent_str = parts[i].split(",")
                    ent_wikiid = ent_str[0]
                    freq = int(ent_str[1])

                    if ent_wikiid not in merged_e_m_counts[mention]:
                        merged_e_m_counts[mention][ent_wikiid] = 0

                    merged_e_m_counts[mention][ent_wikiid] += freq

print("    Done loading wikipedia_p_e_m file ...")

print('Process Crosswikis')
with open('data/basic_data/crosswikidataids_p_e_m.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.rstrip())
        parts = line.split("\t")
        if len(parts) > 1:
            mention = parts[0]

            if mention != "" and mention.find('Wikipedia') == -1 and mention.find('wikipedia') == -1:
                if mention not in merged_e_m_counts:
                    merged_e_m_counts[mention] = {}

                total = int(parts[1])
                num_ents = len(parts)
                for i in range(2, num_ents):
                    ent_str = parts[i].split(",")
                    ent_wikiid = ent_str[0]
                    freq = int(ent_str[1])

                    if ent_wikiid not in merged_e_m_counts[mention]:
                        merged_e_m_counts[mention][ent_wikiid] = 0

                    merged_e_m_counts[mention][ent_wikiid] += freq

print('    Done process Crosswikis')

print('Now sorting and writing ..')
with open('generated/' + args.language + '/merge-wikipedia_p_e_m.txt', 'w', encoding="utf-8") as out:
    for mention in merged_e_m_counts:
        if len(mention) >= 1:
            tbl = {}
            for ent_wikiid in merged_e_m_counts[mention]:
                tbl[ent_wikiid] = merged_e_m_counts[mention][ent_wikiid]

            tbl = {k: v for k, v in sorted(tbl.items(), key=lambda item: item[1], reverse=True)}

            text = ''
            total_freq = 0
            num_ents = 0
            for ent_wikiid in tbl:
                if is_valid_ent(ent_wikiid):
                    text += ent_wikiid + ',' + str( tbl[ent_wikiid] )
                    text += ',' + get_ent_name_from_wikiid(ent_wikiid).replace(' ', '_') + '\t'
                    num_ents += 1
                    total_freq += tbl[ent_wikiid]

                    if num_ents >= 100: # At most 100 candidates
                        break

            if total_freq > 0:
                out.write(mention.strip() + '\t' + str(total_freq) + '\t' + text + '\n')

print('    Done sorting and writing.')
