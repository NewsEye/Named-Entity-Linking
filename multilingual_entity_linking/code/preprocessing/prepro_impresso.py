import argparse
import os
import preprocessing.util as util

def process_wiki(in_filepath, out_filepath, language):
    # _, wiki_id_name_map = util.load_wiki_name_id_map(lowercase=False)
    #_, wiki_id_name_map = util.entity_name_id_map_from_dump()
    entityNameIdMap = util.EntityNameIdMap()
    entityNameIdMap.init_compatible_ent_id(language)
    unknown_gt_ids = 0   # counter of ground truth entity ids that are not in the wiki_name_id.txt
    ent_id_changes = 0
    with open(in_filepath) as fin, open(out_filepath, "w") as fout:
        in_mention = False   # am i inside a mention span or not
        first_document = True
        for line in fin:
            l = line.strip().split('\t')
            if in_mention and not (len(l) == 5 and l[1]=='I'):
                # if I am in mention but the current line does not continue the previous mention
                # then print MMEND and be in state in_mention=FALSE
                fout.write("MMEND\n")
                in_mention = False

            if line.startswith("-DOCSTART-"):
                if not first_document:
                    fout.write("DOCEND\n")
                # line = "-DOCSTART- (967testa ATHLETICS)\n"
                doc_title = line[len("-DOCSTART- ("): -2]
                fout.write("DOCSTART_"+doc_title.replace(' ', '_')+"\n")
                first_document = False
            elif line == "\n":
                fout.write("*NL*\n")
            elif len(l) == 5 and l[1] == 'B':  # this is a new mention
                wikidataid = l[4]
                wikidataid = wikidataid[len("https://www.wikidata.org/wiki/"):]
                if entityNameIdMap.is_valid_entity_id(wikidataid):
                    fout.write("MMSTART_"+wikidataid+"\n")
                    fout.write(l[0]+"\n")  # write the word
                    in_mention = True
                else:
                    unknown_gt_ids += 1
                    fout.write(l[0]+"\n")  # write the word
                    print(line)
            else:
                # words that continue a mention len(l) == 7: and l[1]=='I'
                # or normal word outside of mention, or in mention without disambiguation (len(l) == 4)
                fout.write(l[0].rstrip()+"\n")
        fout.write("DOCEND\n")  # for the last document
    print("process_wiki     unknown_gt_ids: ", unknown_gt_ids)

def create_necessary_folders():
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--impresso_folder", default="../data/basic_data/test_datasets/impresso/")
    parser.add_argument("--output_folder", default="../data/new_datasets/")
    parser.add_argument("--language", default="en")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    args.output_folder = args.output_folder + args.language + "/"
    create_necessary_folders()
    if args.language != "en":
        process_wiki(args.impresso_folder+"HIPE-data-v1.2-train-"+args.language+".conll", args.output_folder+"HIPE-data-v1.2-train-"+args.language+".conll", args.language)
        process_wiki(args.impresso_folder+"HIPE-data-v1.2-dev-"+args.language+".conll", args.output_folder+"HIPE-data-v1.2-dev-"+args.language+".conll", args.language)
        process_wiki(args.impresso_folder+"HIPE-data-v1.2-train+dev-"+args.language+".conll", args.output_folder+"HIPE-data-v1.2-train+dev-"+args.language+".conll", args.language)
    process_wiki(args.impresso_folder+"HIPE-data-v1.2-test-"+args.language+".conll", args.output_folder+"HIPE-data-v1.2-test-"+args.language+".conll", args.language)
