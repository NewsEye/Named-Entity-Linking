# -*- coding: utf-8 -*-

import numpy as np
import torch as t
import torch.nn as nn

from torch import LongTensor as LT
from torch import FloatTensor as FT
import torch.nn.functional as F

class Bundler(nn.Module):

    def forward(self, data):
        raise NotImplementedError

    def forward_i(self, data):
        raise NotImplementedError

    def forward_o(self, data):
        raise NotImplementedError


class Word2Vec(Bundler):

    def __init__(self, vocab_size=20000, embedding_size=300, padding_idx=0):
        super(Word2Vec, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.ent_vectors = nn.Embedding(self.vocab_size, self.embedding_size, padding_idx=padding_idx)
        self.ent_vectors.weight = nn.Parameter(t.cat([t.zeros(1, self.embedding_size), FT(self.vocab_size - 1, self.embedding_size).uniform_(-0.5 / self.embedding_size, 0.5 / self.embedding_size)]))
        self.ent_vectors.weight.requires_grad = True

    def forward(self, data):
        return self.forward_i(data)

    def forward_i(self, data):
        v = LT(data)
        v = v.cuda() if self.ent_vectors.weight.is_cuda else v
        return self.ent_vectors(v)

class SGNS(nn.Module):

    def __init__(self, embedding, vocab_size=20000, ent_emb_size=300, n_negs=20, weights=None):
        super(SGNS, self).__init__()
        self.embedding = embedding
        self.vocab_size = vocab_size
        self.n_negs = n_negs
        self.ent_emb_size = ent_emb_size

    def forward(self, entities, targets, contexts):
        batch_size = contexts.size()[0]
        # Entities
        entities_embs = self.embedding.forward_i(entities)
        entities_embs = entities_embs.unsqueeze(2)
        # Contexts
        contexts_embs = contexts.view(batch_size, -1, self.ent_emb_size)
        contexts_embs = contexts_embs.cuda() if self.embedding.ent_vectors.weight.is_cuda else contexts_embs

        mult = t.bmm(contexts_embs, entities_embs).squeeze()

        m = nn.LogSoftmax(dim=1)
        softmax = m( mult.view(-1, self.n_negs) )
        targets = targets.cuda() if self.embedding.ent_vectors.weight.is_cuda else targets
        targets_v = targets.view(-1)
        loss = nn.NLLLoss()
        output = loss(softmax, targets_v)

        return output
