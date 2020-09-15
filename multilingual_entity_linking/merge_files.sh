#!/bin/bash

# Merge files of several languages
for main_language in "$@"; do
    # Delete old files
    rm -f wiki_data/$main_language/merge-wiki_disambiguation_pages.txt
    rm -f wiki_data/$main_language/merge-wiki_name_id_map.txt
    for language in "$@"; do
        # Merge wiki_disambiguation_pages.txt file
        cat wiki_data/$language/wiki_disambiguation_pages.txt >> wiki_data/$main_language/merge-wiki_disambiguation_pages.txt
        echo "\n" >> wiki_data/$main_language/merge-wiki_disambiguation_pages.txt

        # Merge wiki_name_id_map.txt
        cat wiki_data/$language/wiki_name_id_map.txt >> wiki_data/$main_language/merge-wiki_name_id_map.txt
        echo "\n" >> wiki_data/$main_language/merge-wiki_name_id_map.txt
    done
done
