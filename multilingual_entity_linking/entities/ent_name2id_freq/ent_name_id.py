import os.path
from os import path
import pickle

exec(open("data_gen/indexes/wiki_disambiguation_pages_index.py").read())
exec(open("data_gen/indexes/wiki_redirects_index.py").read())

def preprocess_mention(ent_name):
    ent_name = ent_name.replace('&amp;', '&')
    ent_name = ent_name.replace('&quot;', '"')
    ent_name = ent_name.replace('_', ' ')
    return ent_name

def preprocess_ent_name(ent_name):
    ent_name = ent_name.replace('&amp;', '&')
    ent_name = ent_name.replace('&quot;', '"')
    ent_name = ent_name.replace('_', ' ')
    ent_name = get_redirected_ent_title(ent_name)
    return ent_name

print('==> Loading entity wikiid - name map')
if path.exists("generated/" + args.language + "/e_id_name.p"):
    print("Loading " + "generated/" + args.language + "/e_id_name.p")
    unk_ent_wikiid, e_id_name, unk_ent_thid = pickle.load(open("generated/" + args.language + "/e_id_name.p", 'rb'))
else:
    print("Building " + "generated/" + args.language + "/e_id_name.p")
    unk_ent_wikiid = '0'
    cnt = 0
    cnt_freq = 0

    e_id_name = {}
    e_id_name['ent_name2wikiid'] = {}
    e_id_name['ent_wikiid2name'] = {}

    e_id_name['ent_wikiid2thid'] = {}
    e_id_name['ent_thid2wikiid'] = {}

    e_id_name['ent_wikiid2thid'][unk_ent_wikiid] = cnt
    e_id_name['ent_thid2wikiid'][cnt] = unk_ent_wikiid
    unk_ent_thid = e_id_name['ent_wikiid2thid'][unk_ent_wikiid]

    e_id_name['ent_wikiid2name'][unk_ent_wikiid] = 'UNK_ENT'
    e_id_name['ent_name2wikiid']['UNK_ENT'] = unk_ent_wikiid

    cnt += 1
    with open('wiki_data/' + args.language + '/merge-wiki_name_id_map.txt', encoding="utf-8") as f:
        for line in f:
            line = unquote(line.strip())
            parts = line.split('\t')
            if len(parts) > 1:
                #ent_name = preprocess_ent_name(parts[0])
                ent_name = preprocess_mention(parts[0])
                ent_wikiid = parts[1]

                if ent_wikiid not in wiki_disambiguation_index:
                    e_id_name['ent_wikiid2name'][ent_wikiid] = ent_name
                    e_id_name['ent_name2wikiid'][ent_name] = ent_wikiid

                    e_id_name['ent_wikiid2thid'][ent_wikiid] = cnt
                    e_id_name['ent_thid2wikiid'][cnt] = ent_wikiid
                    cnt += 1

    pickle.dump([unk_ent_wikiid, e_id_name, unk_ent_thid] , open("generated/" + args.language + "/e_id_name.p", 'wb'))
print(len(e_id_name['ent_name2wikiid']))
print('      Done loading entity wikiid - name map')

def get_ent_wikiid_from_name(ent_name, not_verbose = False):
    verbose = not not_verbose
    ent_name = preprocess_ent_name(ent_name)
    if ent_name in e_id_name['ent_name2wikiid']:
        ent_wikiid = e_id_name['ent_name2wikiid'][ent_name]
    else:
        ent_wikiid = False
    if (not ent_wikiid) or (not ent_name):
        if verbose:
            print('Entity ' + ent_name + ' not found. Redirects file needs to be loaded for better performance.')
        return unk_ent_wikiid
    return ent_wikiid

def get_ent_name_from_wikiid(ent_wikiid):
    if not ent_wikiid or ent_wikiid not in e_id_name['ent_wikiid2name']:
        return 'NIL'
    return e_id_name['ent_wikiid2name'][ent_wikiid]

def is_valid_ent(ent_wikiid):
    if ent_wikiid in e_id_name["ent_wikiid2name"]:
        return True
    return False

def get_map_all_valid_ents():
    m = []
    for ent_wikiid in e_id_name['ent_wikiid2name']:
        m.append(ent_wikiid)
    return m

# ent wiki id -> thid
def get_thid(ent_wikiid):
    ent_thid = e_id_name['ent_wikiid2thid'][ent_wikiid]

    if not ent_wikiid or not ent_thid:
        return unk_ent_thid

    return ent_thid

def contains_thid(ent_wikiid):
    ent_thid = e_id_name['ent_wikiid2thid'][ent_wikiid]

    if ent_wikiid == 'NIL' or ent_thid == 'NIL':
        return False

    return True

def get_total_num_ents():
    return len(e_id_name['ent_thid2wikiid'])

def get_wikiid_from_thid(ent_thid):
    ent_wikiid = e_id_name['ent_thid2wikiid'][ent_thid]

    if ent_wikiid == 'NIL' or ent_thid == 'NIL':
        return unk_ent_wikiid

    return ent_wikiid
