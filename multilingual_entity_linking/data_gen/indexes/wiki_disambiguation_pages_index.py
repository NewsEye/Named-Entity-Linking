print('==> Loading disambiguation index')
wiki_disambiguation_index = {}
with open('wiki_data/' + args.language + '/merge-wiki_disambiguation_pages.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        parts = line.split("\t")
        if len(parts) > 1:
            wiki_disambiguation_index[parts[1]] = 1
print('    Done loading disambiguation index')
