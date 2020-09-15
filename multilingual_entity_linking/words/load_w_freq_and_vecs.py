from gensim.models import KeyedVectors
import urllib.request
from os import path

exec(open("words/stopwords.py").read())

print('==> Loading common w2v + top freq list of words')
freq_words = {}

print('   word freq index ...')
num_freq_words = 0
model = None
file_path = ""
f_words = []
with open("generated/" + args.language + "/word_wiki_freq.txt") as f:
    for line in f:
        parts = unquote(line.strip()).split('\t')
        w = parts[0]
        if not is_stop_word_or_number(w) and parts[1].isdigit():
            freq_words[w] = int(parts[1])
            num_freq_words += 1

if args.word_vecs == "w2v":
    model = KeyedVectors.load_word2vec_format('data/basic_data/wordEmbeddings/w2v/GoogleGoogleNews-vectors-negative300.bin', binary=True)
elif args.word_vecs == "fasttext":
    model = KeyedVectors.load_word2vec_format("data/basic_data/wordEmbeddings/fasttext/cc."+args.language+".300.vec", binary=False)
elif args.word_vecs == "muse":
    file_path = 'data/basic_data/wordEmbeddings/muse/wiki.multi.' + args.language + '.vec'
    if not path.exists(file_path):
        url = "https://dl.fbaipublicfiles.com/arrival/vectors/wiki.multi." + args.language + ".vec"
        urllib.request.urlretrieve(url, file_path)
    model = KeyedVectors.load_word2vec_format("data/basic_data/wordEmbeddings/muse/wiki.multi."+args.language+".vec", binary=False)

common_w2v_freq_words = [ word for word in model.vocab if word in freq_words ]
print("common_w2v_freq_words : ", len(common_w2v_freq_words))

we_word2id = {}
we_id2word = {}
if path.exists("generated/" + args.language + "/we_word_id.p"):
    we_word2id, we_id2word = pickle.load( open("generated/" + args.language + "/we_word_id.p", 'rb') )
else:
    for pos,w in enumerate(model.vocab):
        we_word2id[w] = pos
        we_id2word[pos] = w
    pickle.dump([we_word2id,we_id2word] , open("generated/" + args.language + "/we_word_id.p", 'wb'))

def get_we(word):
    return model[word]

def has_we(word):
    return word in we_word2id

def get_w_vec(word):
    if word in we_word2id:
        return word
    else:
        return [False]

def get_negative_we():
    idx = random.randint(0,len(we_id2word)-1)
    return we_id2word[idx]

def get_we_from_id(idx):
    word = str(we_id2word[idx])
    return np.array(model[word], dtype=np.float32)

def get_id_positive(word):
    if word in we_word2id:
        return we_word2id[word]

def get_id_negative():
    idx = random.randint(0,len(we_id2word)-1)
    return idx

def get_negative():
    idx = random.randint(0,len(we_id2word)-1)
    return we_id2word[idx]

exec(open('words/w_freq/w_freq_index.py').read())
