language=$1
python -m gerbil.server --training_name=global_model_$language --experiment_name=corefmerge --persons_coreference_merge=True --ed_mode --language=$language
