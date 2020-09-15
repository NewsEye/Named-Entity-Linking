import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--language", default='en',type = str,
   help="path")
args = ap.parse_args()

def load_wikidata(language):
    wikidataid_to_wikiid, wikiid_to_wikidataid = {}, {}
    with open("wikidataids/wikidataid-wikiid:"+language+".txt", "r", encoding="utf-8") as f:
        for l in f:
            wikidataid, wikiid = l.strip().split("\t")
            wikidataid_to_wikiid[wikidataid] = wikiid
            wikiid_to_wikidataid[wikiid] = wikidataid
    return wikidataid_to_wikiid, wikiid_to_wikidataid

def export_wikidataids(wikiid_to_wikidataid, language):
    output = "wiki_data/"+language+"/"+language+"-wikidataid-TextWithAnchorsFromAllWikipedia.txt"
    source = "wiki_data/"+language+"/"+language+"TextWithAnchorsFromAllWikipedia.txt"
    doc = []
    with open(output, 'w', encoding="utf-8") as out:
        with open(source, 'r', encoding="utf-8") as f:
            doc_val = False
            for l in f:
                l = l.rstrip()
                if "<doc id=" in l and doc == []:
                    title = l.split("title=\"")[1].split("\">")[0].rstrip()
                    wikiid = l.split("id=\"")[1].split("\" url")[0].rstrip()
                    # print(title, wikiid)
                    if wikiid in wikiid_to_wikidataid:
                        wikidataid = wikiid_to_wikidataid[wikiid]
                        url = "https://www.wikidata.org/wiki/" + wikidataid
                        doc.append( '<doc id="'+wikidataid +'" url="'+url+'" title="'+title+'">' )
                        doc_val = True
                elif "</doc>" in l:
                    if doc_val:
                        doc.append(l)
                        for p in doc:
                            out.write(p + "\n")
                    doc = []
                    doc_val = False
                elif doc_val:
                    doc.append(l)

_, wikiid_to_wikidataid = load_wikidata(args.language)
export_wikidataids(wikiid_to_wikidataid, args.language)
