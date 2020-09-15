print('==> Loading redirects index')
wiki_redirects_index = {}
with open('wiki_data/' + args.language + '/wiki_redirects.txt', encoding="utf-8") as f:
    for line in f:
        line = unquote(line.strip())
        parts = line.split("\t")
        if len(parts) > 1:
            wiki_redirects_index[parts[1]] = parts[0]
print('    Done loading redirects index')

def get_redirected_ent_title(ent_name):
    if ent_name in wiki_redirects_index:
        return wiki_redirects_index[ent_name]
    else:
        return ent_name
