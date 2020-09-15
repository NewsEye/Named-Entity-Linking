import random, json, pickle
from tqdm import tqdm
import string

exec(open("words/stopwords.py").read())

def get_most_frequent_entities(max_entities):
    idx = 0
    most_frequent_entities = {}
    most_frequent_entities['0'] = 0
    with open("generated/"+args.language+"/nnid2wikiid.txt", "w", encoding="utf-8") as g:
        with open("generated/"+args.language+"/wikiid2nnid.txt", "w", encoding="utf-8") as f:
            with open("generated/"+args.language+"/ent_wiki_freq.txt", "r", encoding="utf-8") as read:
                for i,l in tqdm(enumerate(read)):
                    if i == max_entities:
                        break
                    l = l.strip().split('\t')
                    f.write(l[0] + '\t' + str(i+1) + '\n')
                    g.write(str(i+1) + '\t' + l[0] + '\n')
                    most_frequent_entities[l[0]] = i+1

    return most_frequent_entities

entities_list = get_most_frequent_entities(args.max_entities)

def get_mention_words(mention):
    words = mention.split()
    words_clean = [ ''.join([ w for w in word if w not in string.punctuation ]) for word in words ]
    correct_words = []
    for w, wc in zip(words, words_clean):
        if has_we(w.lower()) and not is_stop_word_or_number(w.lower()):
            correct_words.append( w.lower() )
        elif has_we(wc.lower()) and not is_stop_word_or_number(wc.lower()):
            correct_words.append( wc.lower() )
    return correct_words

def load_wiki_hyperlink_contexts():
    wiki_hyperlink_contexts = []
    corpus = "generated/"+ args.language + "/wiki_hyperlink_contexts.csv"
    ct = 0
    with open(corpus, encoding="utf-8") as f:
        for line in tqdm(f):
            line = unquote(line.strip())
            parts = line.split('\t')
            mention = parts[2].strip()
            grd_th = parts[-1].split(',')[-1].strip()
            left_ctx = parts[3].strip().split()
            left_ctx = [ w.lower() for w in left_ctx if has_we(w.lower()) and not is_stop_word_or_number(w.lower()) ]
            left_ctx = left_ctx[-args.ctx_size:]
            left_ctx = left_ctx + get_mention_words(grd_th)
            #print("##Left_ctx: ", left_ctx)
            right_ctx = parts[4].strip().split()
            right_ctx = [ w.lower() for w in right_ctx if has_we(w.lower()) and not is_stop_word_or_number(w.lower()) ]
            right_ctx = right_ctx[:args.ctx_size]
            if grd_th in e_id_name['ent_name2wikiid'] and e_id_name['ent_name2wikiid'][ grd_th ] in entities_list:
                wiki_hyperlink_contexts.append((mention, left_ctx, right_ctx, grd_th))
    pickle.dump(wiki_hyperlink_contexts, open("generated/" + args.language + "/wiki_hyperlink_contexts.p", 'wb'))
    return wiki_hyperlink_contexts

def load_wiki_canonical_words():
    wiki_canonical_words = []
    corpus = "generated/"+ args.language + "/wiki_canonical_words.txt"
    ct = 0
    with open(corpus, encoding="utf-8") as f:
        for line in tqdm(f):
            line = unquote(line.strip())
            parts = line.split('\t')
            grd_th = parts[1].strip()
            if grd_th in e_id_name['ent_name2wikiid'] and e_id_name['ent_name2wikiid'][ grd_th ] in entities_list:
                ctx = parts[2].strip().split()
                ctx = [ w.lower() for w in ctx if has_we(w.lower()) and not is_stop_word_or_number(w.lower()) ]
                ctx = ctx[:args.ctx_size] + get_mention_words(grd_th) + ctx[args.ctx_size:2*args.ctx_size]
                #print("--Ctx: ", ctx)
                wiki_canonical_words.append((None, ctx, None, grd_th))
    pickle.dump(wiki_canonical_words, open("generated/" + args.language + "/wiki_canonical_words.p", 'wb'))
    return wiki_canonical_words

def dataset_with_ids_and_embs(dataset):
    data = []
    size = 0
    for it in tqdm(range(len(dataset))):
        ent_wikiid = e_id_name['ent_name2wikiid'][ dataset[it][3] ]
        if ent_wikiid not in entities_list:
            continue
        entity_id = entities_list[ent_wikiid]
        positive_words = []
        if dataset[it][2] != None:
            positive_words = dataset[it][1][:] + dataset[it][2][:]
        else:
            positive_words = dataset[it][1][:]
        positive_we = [ get_w_vec(w) for w in positive_words ]
        context, targets = [], []
        i = 0
        valid = 0
        if len(positive_words) > 1:
            while i < args.positive_words:
                example = []
                grd_th_pos = random.randint(0,args.negative_words-1)
                ct = 0
                for j in range(args.negative_words):
                    if j == grd_th_pos:
                        p_word = positive_words[ random.randint(0,len(positive_words)-1) ]
                        while get_w_vec( p_word )[0] == False and ct < 5:
                            p_word = positive_words[ random.randint(0,len(positive_words)-1) ]
                            ct += 1
                        example.append( get_id_positive( p_word ) )
                    else:
                        example.append( get_id_negative() )
                if ct < 5:
                    context.append( example )
                    targets.append( grd_th_pos )
                    i += 1
                if valid == 2*args.positive_words:
                    break
                valid += 1

            if valid < 2*args.positive_words:
                data.append( (entity_id, targets, context) )
    pickle.dump(data, open('generated/' + args.language + '/train_ent_embs.dat', 'wb'))

if not path.exists("generated/" + args.language + "/train_ent_embs.dat"):
    if path.exists("generated/" + args.language + "/wiki_hyperlink_contexts.p"):
        print("Loading wiki_hyperlink_contexts file ....")
        wiki_hyperlink_contexts = pickle.load(open("generated/" + args.language + "/wiki_hyperlink_contexts.p", 'rb'))
    else:
        print("Building wiki_hyperlink_contexts file ....")
        wiki_hyperlink_contexts = load_wiki_hyperlink_contexts()
    if path.exists("generated/" + args.language + "/wiki_canonical_words.p"):
        print("Loading wiki_canonical_words file ....")
        wiki_canonical_words = pickle.load(open("generated/" + args.language + "/wiki_canonical_words.p", 'rb'))
    else:
        print("Building wiki_canonical_words file ....")
        wiki_canonical_words = load_wiki_canonical_words()
    print("Creating training dataset for entity embddings...")
    dataset_with_ids_and_embs(wiki_hyperlink_contexts + wiki_canonical_words)
