import argparse, json, os
from urllib.parse import unquote
import spacy

ap = argparse.ArgumentParser()

ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
args = ap.parse_args()

exec(open("utils/utils.py").read())

print('==> Loading wiki_canonical_words file ...')
word_freqs = {}
num_lines = 0

with open('generated/' + args.language + '/wiki_canonical_words.txt', encoding="utf-8") as f:
    for line in f:
        num_lines += 1
        if num_lines % 100000 == 0:
            print('Processed ' + str(num_lines) + ' lines. ')

        line = unquote(line.strip())
        parts = line.split("\t")
        words = parts[2].split(' ')
        for w in words:
            if len(w.strip()) > 0:
                if w not in word_freqs:
                    word_freqs[w] = 0

                word_freqs[w] += 1

print('   Done loading wiki_canonical_words file ...')

#-- Writing word frequencies
print('Sorting and writing')
sorted_word_freq = {}
for w in word_freqs:
    if word_freqs[w] >= 2:
        sorted_word_freq[w] = word_freqs[w]

sorted_word_freq = {k: v for k, v in sorted(sorted_word_freq.items(), key=lambda item: item[1], reverse=True)}

total_freq = 0
with open('generated/' + args.language + '/word_wiki_freq.txt','w', encoding="utf-8") as out:
    for w in sorted_word_freq:
        out.write( w + '\t' + str(sorted_word_freq[w]) + '\n' )
        total_freq += sorted_word_freq[w]

print('Total freq = ' + str(total_freq) + '\n')
