#!/bin/bash

for language in 'lang'
do
rm data/new_datasets/$language/*
rm -r data/tfrecords/$language
cd code
  python3 -m preprocessing.prepro_newseye --language $language
  python3 -m preprocessing.prepro_util --language $language

  CUDA_VISIBLE_DEVICES=8 python3 -m model.train  \
                    --batch_size=2   --experiment_name=corefmerge \
                    --training_name=global_model_$language \
                    --ent_vecs_regularization=l2dropout  --evaluation_minutes=10 --nepoch_no_imprv=10 \
                    --span_emb="boundaries"  \
                    --dim_char=50 --hidden_size_char=50 --hidden_size_lstm=150 \
                    --nn_components=pem_lstm_attention_global \
                    --fast_evaluation=True  \
                    --attention_ent_vecs_no_regularization=True --final_score_ffnn=0_0 \
                    --attention_R=10 --attention_K=200 \
                    --train_datasets=$language-train \
                    --ed_datasets=$language-dev\_z_$language-test --ed_val_datasets=0 \
                    --global_thr=0.001 --global_score_ffnn=0_0 \
                    --language=$language

done
