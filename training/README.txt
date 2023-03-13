python training-data-converter.py
cd training
python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./train.spacy --initialize.vectors ru_core_news_lg
