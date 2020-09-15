import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--path_wiki_xml", default='./',type = str,
   help="path to Wiki xml dump")
ap.add_argument("-w", "--filename_wiki", default='ruwiki-latest-pages-articles.xml',type = str,
   help="Name of Wiki xml dump")
ap.add_argument("-a", "--filename_articles", default='wiki_name_id_map.csv',type = str,
   help="Output filename of wiki id-name map")
ap.add_argument("-r", "--filename_redirect", default='wiki_redirects.csv',type = str,
   help="Output filename of wiki redirected pages")
ap.add_argument("-d", "--filename_disambig", default='wiki_disambiguation_pages.csv',type = str,
   help="Output filename of wiki disambiguation pages")
ap.add_argument("-e", "--encoding", default='utf-8',type = str,
   help="Encoding of files")
ap.add_argument("-l", "--language", default='en',type = str,
   help="path")

args = ap.parse_args()

from wiki_data_generated.wiki_info_generation import wiki_txt_files_creating

def load_wikidata(language):
    wikidataid_to_wikiid, wikiid_to_wikidataid = {}, {}
    with open("wikidataids/wikidataid-wikiid:"+language+".txt", "r") as f:
        for l in f:
            wikidataid, wikiid = l.strip().split("\t")
            wikidataid_to_wikiid[wikidataid] = wikiid
            wikiid_to_wikidataid[wikiid] = wikidataid
    return wikidataid_to_wikiid, wikiid_to_wikidataid

# def load_wikiname(language):
#     wikiid_to_title, wikiid_to_wikiid = {}, {}
#     with open("wikidataids//"+language+"_wiki_name_id_map.txt", "r", encoding="utf-8") as f:
#         for l in f:
#             title, wikiid = l.strip().split("\t")
#             wikiid_to_title[wikiid] = title
#             title_to_wikiid[title] = wikidataid
#     return wikiid_to_title, title_to_wikiid

_, wikiid_to_wikidataid = load_wikidata(args.language)
# _, title_to_wikiid = load_wikidata(args.language)
wiki_txt_files_creating(wikiid_to_wikidataid, PATH_WIKI_XML = args.path_wiki_xml,
    FILENAME_WIKI = args.filename_wiki,
    FILENAME_ARTICLES = args.filename_articles,
    FILENAME_REDIRECT = args.filename_redirect,
    FILENAME_DISAMBIG = args.filename_disambig,
    ENCODING = args.encoding)
