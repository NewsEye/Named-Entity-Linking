w_freq = dict()
# UNK word id
unk_w_id = 0

if path.exists("generated/" + args.language + "/w_freq.p"):
    print(" Loading w_freq file ...")
    w_freq = pickle.load(open("generated/" + args.language + "/w_freq.p", 'rb'))
else:
    print(" Building w_freq file ...")
    w_freq['id2word'] = dict()
    w_freq['word2id'] = dict()

    w_freq['word2id']['UNK_W'] = unk_w_id
    w_freq['id2word'][unk_w_id] = 'UNK_W'

    tmp_wid = 0
    for w in common_w2v_freq_words:
        tmp_wid += 1
        w_id = tmp_wid
        w_freq['id2word'][w_id] = w
        w_freq['word2id'][w] = w_id
    w_freq['total_num_words'] = tmp_wid
    pickle.dump(w_freq, open('generated/' + args.language + '/w_freq.p', 'wb'))

def total_num_words():
    return w_freq['total_num_words']

def contains_w_id(w_id):
    if w_id >= 0 and w_id <= total_num_words():
        return w_id != unk_w_id
    return False

# id -> word
def get_word_from_id(w_id):
    if w_id in w_freq['id2word']:
        return w_freq['id2word'][w_id]

# word -> id
def get_id_from_word(w):
    if w in w_freq['word2id']:
        return w_freq['word2id'][w]
    else:
        return unk_w_id

def contains_w(w):
    return contains_w_id(get_id_from_word(w))
