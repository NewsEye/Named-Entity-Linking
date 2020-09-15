#!/bin/bash

if [ $# -eq 0 ] ; then
    echo 'ERROR: Choose a language to download the dumps of Wikipedia'
    exit 1
fi

for language in "$@"; do
    # Download the language version of the Wikipedia
    wget http://dumps.wikimedia.org/${language}wiki/latest/${language}wiki-latest-pages-articles.xml.bz2
    mkdir -p wiki_data/${language}/
    mv ${language}wiki-latest-pages-articles.xml.bz2 wiki_data/${language}/
    # Extract Wikipages : https://github.com/attardi/wikiextractor
    python3 extract_dump/WikiExtractor.py -l -o wiki_data/${language}/wiki${language} wiki_data/${language}/${language}wiki-latest-pages-articles.xml.bz2
    # Concatenate pages : https://github.com/korney3/EL
    python3 extract_dump/WikiDumpTxt_join.py -p wiki_data/${language}/wiki${language} -o wiki_data/${language}/${language}TextWithAnchorsFromAllWikipedia.txt
    python3 extract_dump/convert2wikidata.py -l ${language}
    bzip2 -d wiki_data/${language}/${language}wiki-latest-pages-articles.xml.bz2
    # Create files: wiki_disambiguation_pages, wiki_name_id_map and wiki_redirects. https://github.com/korney3/EL
    python3 extract_dump/wiki_info_create.py -p wiki_data/${language}/ -w ${language}wiki-latest-pages-articles.xml -l $language
    rm -r wiki_data/${language}/wiki${language}
done
