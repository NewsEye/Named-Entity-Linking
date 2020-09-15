import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--files_path", default='./wiki',type = str,
   help="Folder with extractes articles")
ap.add_argument("-o", "--filename_output", default='textWithAnchorsFromAllWikipedia.txt',type = str,
   help="Name of created file")

args = ap.parse_args()

FILES_PATH = args.files_path
FILENAME_OUTPUT = args.filename_output

from wiki_data_generated.wiki_info_generation import merge_files_in_subfolders

merge_files_in_subfolders(path=args.files_path, filename=args.filename_output,filetype='.txt')
