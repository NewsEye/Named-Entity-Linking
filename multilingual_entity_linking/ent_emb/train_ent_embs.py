import argparse, json, os, pickle
from urllib.parse import unquote
import numpy as np
from tqdm import tqdm
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
import torch as t
from model_entities import Word2Vec, SGNS
import pickle
import os.path
from os import path
import torch
import spacy
ap = argparse.ArgumentParser()

ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
ap.add_argument("-epoch", "--epoch", type=int, default=101,
   help="Number of epochs.")
ap.add_argument("-batch_size", "--batch_size", type=int, default=128,
   help="Batch size.")
ap.add_argument("-ctx_size", "--ctx_size", type=int, default=5,
   help="Context size.")
ap.add_argument("-positive_words", "--positive_words", type=int, default=10,
   help="Number of positive words.")
ap.add_argument("-max_entities", "--max_entities", type=int, default=2000000,
   help="Number max of entities.")
ap.add_argument("-negative_words", "--negative_words", type=int, default=10,
   help="Number of negatif words.")
ap.add_argument("-word_vecs", "--word_vecs", type=str, default="muse",
   help="Word embeddings (defaut: 'muse'): 'muse', 'fasttext' and 'w2v'")
args = ap.parse_args()

class Args:
    base_folder = ""
config = Args()

exec(open("utils/utils.py").read())
exec(open("entities/ent_name2id_freq/ent_name_id.py").read())
exec(open("words/load_w_freq_and_vecs.py").read())
exec(open("data_gen/gen_ent_emb/gen_training_ent_emb_dataset.py").read())

class PermutedSubsampledCorpus(Dataset):

    def __init__(self, datapath, ws=None):
        data = pickle.load(open(datapath, 'rb'))
        if ws is not None:
            self.data = []
            for entity_id, targets, context in data:
                print(entity_id, targets,context)
                if random.random() > 0.3:
                    self.data.append((entity_id, targets, context))
        else:
            self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        entity_id, targets, context = self.data[idx]
        return torch.from_numpy(np.array(entity_id)), torch.from_numpy(np.array(targets)), torch.from_numpy(np.array(context))

model_w2v = Word2Vec(vocab_size=len(entities_list), embedding_size=300)
print(len(entities_list))
sgns = SGNS(embedding=model_w2v, vocab_size=300, n_negs=args.negative_words)
sgns = sgns.cuda()
optim = Adam(sgns.parameters())

for epoch in range(1, args.epoch + 1):
    dataset = PermutedSubsampledCorpus('generated/' + args.language + '/train_ent_embs.dat')
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    total_batches = int(np.ceil(len(dataset) / args.batch_size))
    pbar = tqdm(dataloader)
    pbar.set_description("[Epoch {}]".format(epoch))
    for entity_id, targets, context in pbar:
        context = torch.tensor([ [ [ get_we_from_id(idx) for idx in positive_case.numpy() ] for positive_case in example ] for example in context ])
        loss = sgns(entity_id, targets, context)
        optim.zero_grad()
        loss.backward()
        optim.step()
        pbar.set_postfix(loss=loss.item())

    idx2vec = model_w2v.ent_vectors.weight.data.cpu().numpy()
    np.save("generated/" + args.language + "/ent_vecs.npy", idx2vec)
    with open("generated/" + args.language + "/ent_emb.vec", "w", encoding="utf-8") as f:
        f.write(str(len(idx2vec)) + " " + str(len(idx2vec[0])) + "\n")
        for pos, idx in enumerate(idx2vec):
            wikiid = get_wikiid_from_thid(pos)
            f.write(wikiid)
            for value in idx2vec[pos]:
                f.write(" " + str(value))
            f.write("\n")
