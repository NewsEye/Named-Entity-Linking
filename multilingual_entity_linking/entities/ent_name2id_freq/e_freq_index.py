print('==> Loading entity freq map')

min_freq = 1
e_freq = {}
e_freq['ent_f_start'] = {}
e_freq['ent_f_end'] = {}
e_freq['total_freq'] = 0
e_freq['sorted'] = {}

cur_start = 1
cnt = 0
with open('generated/' + args.language + '/ent_wiki_freq.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        parts = line.split('\t')
        ent_wikiid = parts[0]
        ent_f = int(parts[2])

        e_freq['ent_f_start'][ent_wikiid] = cur_start
        e_freq['ent_f_end'][ent_wikiid] = cur_start + ent_f - 1
        e_freq['sorted'][cnt] = ent_wikiid
        cur_start = cur_start + ent_f
        cnt += 1

e_freq['total_freq'] = cur_start - 1

print('    Done loading entity freq index. Size = ' + str(cnt))

def get_ent_freq(ent_wikiid):
    if ent_wikiid in e_freq['ent_f_start']:
        return e_freq['ent_f_end'][ent_wikiid] - e_freq['ent_f_start'][ent_wikiid] + 1
    return 0
