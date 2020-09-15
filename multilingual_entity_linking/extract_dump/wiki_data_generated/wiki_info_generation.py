#pipeline:
# 1) download wiki xml dump (for example, lastest russian wikipedia dump) http://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-pages-articles.xml.bz2)
# 2) Extract text info with Wikiextractor (https://github.com/attardi/wikiextractor, not json option)
# 3) Merge files from created subdirectories in one txt file with merge_files_in_folder function

import os, re

def merge_files_in_subfolders(path='./wiki', filename='textWithAnchorsFromAllWikipedia.txt',filetype='.txt'):
    """Merges all files in subfolders inside a folder in one file

    Parameters:
    path - root folder with subfolders
    filename (str) - name of file to write
    filetype (str) - type of files to merge

    Returns:
    -
    """
    import os
    if os.path.isfile(filename) :
        os.remove(filename)
    dirs = os.listdir(path=path)
    print(dirs)
    for directory in dirs:
        filenames = os.listdir(os.path.join(path,directory))
        with open(filename, 'a') as outfile:
            for fname in filenames:
                #if filetype in fname:
                with open(os.path.join(path,directory,fname)) as infile:
                    for line in infile:
                        outfile.write(line)
    return


def merge_files_in_folder(path='./wiki', filename='aida_train.txt',filetype='.txt',filler_start='',filler_end='',add_id=False,replace_spaces=False, wiki_id_name_dict=None,num_of_files = None):
    """Merges all files inside a folder in one file

    Parameters:
    path - root folder with subfolders
    filename (str) - name of file to write
    filetype (str) - type of files to merge
    filler_start (str) - string placed in the beginning of each merged file
    filler_end (str) - string placed in the end of each merged file
    add_id (boolean) - option to add '_fileid' after filler_start
    wiki_id_name_dict (dict) - dictionary with mapping wiki_id to name of the entity
    num_of_files (int) - maximum number of files to merge

    Returns:
    -
    """
    import os
    filenames = os.listdir(path)
    if num_of_files is not None:
        filenames = filenames[:num_of_files]
    with open(filename, 'a', encoding = 'utf-8') as outfile:
        for fname in filenames:
            if filetype in fname:
                with open(os.path.join(path,fname)) as infile:
                    if filler_start!='':
                        if add_id:
                            wiki_id =  fname.split('.')[0].split('_')[1]
                            if wiki_id_name_dict is not None:
                                wiki_name = wiki_id_name_dict[wiki_id]
                                if replace_spaces:
                                    wiki_name = '_'.join(wiki_name.split(' '))
                                outfile.write(filler_start+'_'+wiki_id+'_'+wiki_name)
                            else:
                                outfile.write(filler_start+'_'+wiki_id)
                        else:
                            outfile.write(filler_start)
                        outfile.write('\n')
                    for line in infile:
                        if line != '\n':
                            outfile.write(line)
                    if filler_end!='':
                        outfile.write(filler_end)
                        outfile.write('\n')
    return

def merge_filenames(path='./wiki', filenames_input=[],
                    filename_output='aida_train.txt',
                    filler_start='DOCSTART',
                    filler_end='DOCEND',
                    add_id=False,replace_spaces=False,
                    wiki_id_name_dict=None,
                    num_of_files = None):
    """Merges files from filenames_input in one filename_output file

    Parameters:
    path - root folder with subfolders
    filenames_input (list) - names of files to merge
    filename_output (str) - name of output file
    filler_start (str) - string placed in the beginning of each merged file
    filler_end (str) - string placed in the end of each merged file
    add_id (boolean) - option to add '_fileid' after filler_start
    wiki_id_name_dict (dict) - dictionary with mapping wiki_id to name of the entity
    num_of_files (int) - maximum number of files to merge


    Returns:
    -
    """
    import os
    import time
    from my_funcs import print_progress_stats
    if os.path.isfile(filename_output) :
        os.remove(filename_output)
    if num_of_files is not None:
        filenames_input = filenames_input[:num_of_files]
    with open(filename_output, 'a', encoding = 'utf-8') as outfile:
        start=time.time()
        for i,fname in enumerate(filenames_input):
            with open(os.path.join(path,fname)) as infile:
                if filler_start!='':
                    if add_id:
                        wiki_id =  fname.split('.')[0].split('_')[1]
                        if wiki_id_name_dict is not None:
                            wiki_name = wiki_id_name_dict[wiki_id]
                            if replace_spaces:
                                wiki_name = '_'.join(wiki_name.split(' '))
                            outfile.write(filler_start+'_'+wiki_id+'_'+wiki_name)
                        else:
                            outfile.write(filler_start+'_'+wiki_id)
                    else:
                        outfile.write(filler_start)
                    outfile.write('\n')
                for line in infile:
                    if line != '\n':
                        outfile.write(line)
                if filler_end!='':
                    outfile.write(filler_end)
                    outfile.write('\n')
                if i%1000==0 and i!=0:
                    print_progress_stats(len(filenames_input),
                                         i, 0, time_per_iteration=round((time.time()-start)/60/i,3),
                                         num_of_processes=1)
    return

def merge_jsons(path='./wiki', filenames=[],
                filename='prob_yago_crosswikis_wikipedia_p_e_m.txt',
                filetype='.json',
                wiki_id_name_dict=None,
                step=10000):
    """Merges files from filenames_input in one filename_output file

    Parameters:
    path - root folder with subfolders
    filenames_input (list) - names of files to merge
    filename_output (str) - name of output file
    filler_start (str) - string placed in the beginning of each merged file
    filler_end (str) - string placed in the end of each merged file
    add_id (boolean) - option to add '_fileid' after filler_start
    wiki_id_name_dict (dict) - dictionary with mapping wiki_id to name of the entity
    num_of_files (int) - maximum number of files to merge


    Returns:
    -
    """
    import os
    import json
    from nltk.tokenize import wordpunct_tokenize
    from my_funcs import print_progress_stats
    import time
#     import pymorphy2
#     morph = pymorphy2.MorphAnalyzer()
    errors=0
    print('Overall files number: ', len(filenames))
    wiki_p_e_m_all = {}
    wiki_p_e_m_return = {}
    start_time = time.time()
    jsons=0
    for fname in filenames:
        with open(os.path.join(path,fname)) as json_file:
            try:
                wiki_p_e_m = json.load(json_file)
            except ValueError:
                errors+=1
                print (errors, fname)
                continue
            del wiki_p_e_m['num_strings']
            del wiki_p_e_m['num_mentions']
            jsons+=1
            for mention in wiki_p_e_m.keys():
                for entity in wiki_p_e_m[mention].keys():
                    clear_mention = mention.strip('\n')
                    # clear_mention = clear_mention.lower()
#                     clear_mention = ' '.join(morph.parse(x)[0].normal_form for x in wordpunct_tokenize(clear_mention))
#                     clear_mention = clear_mention.rstrip('\n')
                    if clear_mention in wiki_p_e_m_all.keys():
                        if entity in wiki_p_e_m_all[clear_mention].keys():
                            wiki_p_e_m_all[clear_mention][entity]+=wiki_p_e_m[mention][entity]
                        else:
                            wiki_p_e_m_all[clear_mention][entity]=wiki_p_e_m[mention][entity]
                    else:
                        wiki_p_e_m_all[clear_mention]={}
                        wiki_p_e_m_all[clear_mention][entity]=wiki_p_e_m[mention][entity]
            if jsons%step==0:
                curr_time = time.time()
                print_progress_stats(len(filenames), jsons, time_per_iteration=(curr_time-start_time)/60/float(step), num_of_processes=1)
                start_time = curr_time
                wiki_p_e_m_return = wiki_p_e_m_all.copy()
                with open(filename, 'w', encoding = 'utf-8') as outfile:
                    for mention in wiki_p_e_m_all.keys():
                        total_freq = 0
                        ents=''
                        for entity in wiki_p_e_m_all[mention].keys():

                            total_freq+=wiki_p_e_m_all[mention][entity]
                            ents = ents+'\t'+entity+','+str(wiki_p_e_m_all[mention][entity])+','+wiki_id_name_dict[entity]
                        outfile.write(mention+'\t'+str(total_freq)+ents+'\n')

    return wiki_p_e_m_return

def merge_json_files_in_folder(path='./wiki', filename='prob_yago_crosswikis_wikipedia_p_e_m.txt',filetype='.json',wiki_id_name_dict=None, step=10000):
    """Merges all json files inside a folder in one txt file

    Parameters:
    path - root folder with subfolders
    filename (str) - name of file to write
    filetype (str) - type of files to merge
    step (int) - number of iterations to save file & print progress info

    Returns:
    wiki_p_e_m_all (dict) - dictionary with overal mention-entities counts
    """
    import os
    import json
    from nltk.tokenize import wordpunct_tokenize
    from my_funcs import print_progress_stats
    import time
#     import pymorphy2
#     morph = pymorphy2.MorphAnalyzer()
    errors=0
    filenames = os.listdir(path)
    filenames=[x for x in filenames if filetype in x]
    print('Overall files number: ', len(filenames))
    wiki_p_e_m_all = {}
    wiki_p_e_m_return = {}
    start_time = time.time()
    jsons=0
    for fname in filenames:
        with open(os.path.join(path,fname)) as json_file:
            try:
                wiki_p_e_m = json.load(json_file)
            except ValueError:
                errors+=1
                print (errors, fname)
                continue
            del wiki_p_e_m['num_strings']
            del wiki_p_e_m['num_mentions']
            jsons+=1
            for mention in wiki_p_e_m.keys():
                for entity in wiki_p_e_m[mention].keys():
                    clear_mention = mention.strip('\n')
                    # clear_mention = clear_mention.lower()
#                     clear_mention = ' '.join(morph.parse(x)[0].normal_form for x in wordpunct_tokenize(clear_mention))
#                     clear_mention = clear_mention.rstrip('\n')
                    if clear_mention in wiki_p_e_m_all.keys():
                        if entity in wiki_p_e_m_all[clear_mention].keys():
                            wiki_p_e_m_all[clear_mention][entity]+=wiki_p_e_m[mention][entity]
                        else:
                            wiki_p_e_m_all[clear_mention][entity]=wiki_p_e_m[mention][entity]
                    else:
                        wiki_p_e_m_all[clear_mention]={}
                        wiki_p_e_m_all[clear_mention][entity]=wiki_p_e_m[mention][entity]
            if jsons%step==0:
                curr_time = time.time()
                print_progress_stats(len(filenames), jsons, time_per_iteration=(curr_time-start_time)/60/float(step), num_of_processes=1)
                start_time = curr_time
                wiki_p_e_m_return = wiki_p_e_m_all.copy()
                with open(filename, 'w', encoding = 'utf-8') as outfile:
                    for mention in wiki_p_e_m_all.keys():
                        total_freq = 0
                        ents=''
                        for entity in wiki_p_e_m_all[mention].keys():

                            total_freq+=wiki_p_e_m_all[mention][entity]
                            ents = ents+'\t'+entity+','+str(wiki_p_e_m_all[mention][entity])+','+wiki_id_name_dict[entity]
                        outfile.write(mention+'\t'+str(total_freq)+ents+'\n')

    return wiki_p_e_m_return




def wiki_txt_files_creating(wikiid_to_wikidataid, PATH_WIKI_XML = './',
    FILENAME_WIKI = 'ruwiki-latest-pages-articles.xml',
    FILENAME_ARTICLES = 'wiki_name_id_map.csv',
    FILENAME_REDIRECT = 'wiki_redirects.csv',
    FILENAME_DISAMBIG = 'wiki_disambiguation_pages.csv',
    ENCODING = "utf-8"):

    """Creates three csv and txt files based on xml wikipedia dump, containing
    1) mapping article names to id
    2) redirections between articles
    3) disambiguation pages

    Parameters:
    PATH_WIKI_XML - path to wiki xml dump file and for created files
    FILENAME_WIKI (str) - wiki xml dump file name,
    FILENAME_ARTICLES (str) - file with name of article '\t' article id,
    FILENAME_REDIRECT (str) - file with name of article '\t' name of article it redirects (for example 'Речь Посполита -> Речь Посполитая'),
    FILENAME_DISAMBIG (str) - file with names of articles containing "(значения)" in the title,
    ENCODING (str) - кодировка

    Returns:
    -
    """
    # Simple example of streaming a Wikipedia
    # Copyright 2017 by Jeff Heaton, released under the The GNU Lesser General Public License (LGPL).
    # http://www.heatonresearch.com
    # -----------------------------
    import xml.etree.ElementTree as etree
    import codecs
    import csv
    import time
    import os

    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/

    # Nicely formatted time string
    def hms_string(sec_elapsed):
        h = int(sec_elapsed / (60 * 60))
        m = int((sec_elapsed % (60 * 60)) / 60)
        s = sec_elapsed % 60
        return "{}:{:>02}:{:>05.2f}".format(h, m, s)


    def strip_tag_name(t):
        t = elem.tag
        idx = k = t.rfind("}")
        if idx != -1:
            t = t[idx + 1:]
        return t


    pathWikiXML = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)
    pathArticlesRedirect = os.path.join(PATH_WIKI_XML, FILENAME_REDIRECT)
    pathDisambigRedirect = os.path.join(PATH_WIKI_XML, FILENAME_DISAMBIG)

    totalCount = 0
    templateCount = 0
    articleCount = 0
    redirectCount = 0
    disambigCount = 0
    title = None
    start_time = time.time()

    with codecs.open(pathArticles, "w", ENCODING) as articlesFH, \
            codecs.open(pathArticlesRedirect, "w", ENCODING) as redirectFH, \
            codecs.open(pathDisambigRedirect, "w", ENCODING) as disambigFH:
        articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL)
        redirectWriter = csv.writer(redirectFH, quoting=csv.QUOTE_MINIMAL)
        disambigWriter = csv.writer(disambigFH, quoting=csv.QUOTE_MINIMAL)

        articlesWriter.writerow(['id', 'title'])
        redirectWriter.writerow(['title', 'redirect'])
        disambigWriter.writerow(['id', 'title'])

        for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
            tname = strip_tag_name(elem.tag)

            if event == 'start':
                if tname == 'page':
                    title = ''
                    id_ = -1
                    redirect = ''
                    disambig = ''
                    inrevision = False
                    ns = 0
                elif tname == 'revision':
                    # Do not pick up on revision id's
                    inrevision = True
            else:
                if tname == 'title':
                    title = elem.text
                    #print(title)
                    #if title.find('(значения)')!=-1:
                    if re.search(r'[\w ]+\([\w -]+\)',title):
                        #print("ok - ", title)
                        disambig = title
                elif tname == 'id' and not inrevision:
                    id_ = int(elem.text)
                elif tname == 'redirect':
                    redirect = elem.attrib['title']
                elif tname == 'ns':
                    ns = int(elem.text)
                elif tname == 'page':
                    totalCount += 1

                    if ns == 10:
                        templateCount += 1
                    else:
                        enable = False
                        if str(id_) in wikiid_to_wikidataid:
                            id_ = wikiid_to_wikidataid[str(id_)]
                            enable = True
                        if enable:
                            articleCount += 1
                            articlesWriter.writerow([id_, title])
                            if len(redirect) > 0:
                                # if redirect in title_to_wikiid and title_to_wikiid[redirect] in wikiid_to_wikidataid:
                                redirectCount += 1
                                redirectWriter.writerow([title, redirect])
                            if len(disambig) > 0:
                                disambigCount += 1
                                disambigWriter.writerow([id_, title])

                    # if totalCount > 100000:
                    #  break

                    if totalCount > 1 and (totalCount % 100000) == 0:
                        print("{:,}".format(totalCount))
                        print("Disambiguation pages: {:,}".format(disambigCount))
                        print("Article pages: {:,}".format(articleCount))
                        print("Redirect pages: {:,}".format(redirectCount))

                elem.clear()

    elapsed_time = time.time() - start_time

    print("Total pages: {:,}".format(totalCount))
    print("Disambiguation pages: {:,}".format(disambigCount))
    print("Article pages: {:,}".format(articleCount))
    print("Redirect pages: {:,}".format(redirectCount))
    print("Elapsed time: {}".format(hms_string(elapsed_time)))

    def convert_csv_to_txt(filename,path = PATH_WIKI_XML):
        csv_file = filename
        txt_file = filename.split('.')[0]+'.txt'
        with open(os.path.join(path, txt_file), "w", encoding='utf_8') as my_output_file:
            with open(os.path.join(path, csv_file), "r", encoding='utf_8') as my_input_file:
                # [ my_output_file.write("\t".join([row[1],row[0]]).lower()+'\n') for i,row in enumerate(csv.reader(my_input_file)) if i!=0]
                [ my_output_file.write("\t".join([row[1],row[0]])+'\n') for i,row in enumerate(csv.reader(my_input_file)) if i!=0]
        my_output_file.close()
        return
    convert_csv_to_txt(FILENAME_ARTICLES)
    convert_csv_to_txt(FILENAME_REDIRECT)
    convert_csv_to_txt(FILENAME_DISAMBIG)

    return



#output: -
def wiki_name_id_txt_to_json(PATH='./',
                            FILENAME_ARTICLES = 'wiki_name_id_map.txt'):
    """Converts txt mapping of article name to id to two json dictionaries "wiki_name_id.json", "wiki_id_name.json"

    Parameters:
    PATH - path to txt FILENAME_ARTICLES file and for created files
    FILENAME_ARTICLES (str) - file with name of article '\t' article id

    Returns:
    -
    """
    import json
    import os
    wiki_name_id_dict = {}
    wiki_id_name_dict = {}
    with open (os.path.join(PATH, FILENAME_ARTICLES),'r') as f:
        for s in f:
            line = s.split('\n')[0]
            wiki_title,wiki_id = line.split('\t')
            # wiki_title = wiki_title.lower()
            wiki_name_id_dict[wiki_title] = wiki_id
            wiki_id_name_dict[wiki_id] = wiki_title
    wiki_name_id_json = json.dumps(wiki_name_id_dict)
    f = open(os.path.join(PATH,"wiki_name_id.json"),"w")
    f.write(wiki_name_id_json)
    f.close()
    wiki_id_name_json = json.dumps(wiki_id_name_dict)
    f = open(os.path.join(PATH,"wiki_id_name.json"),"w")
    f.write(wiki_id_name_json)
    f.close()
    return



def wiki_redirections_txt_to_json(PATH='./',
                            FILENAME_REDIRECTIONS = 'wiki_redirects.txt'):
    """Adds information about redirections to id_name and name_id dictionaries and turns them to wiki_name_id_with_redirections.json
and /wiki_id_name_with_redirections.json

    Parameters:
    PATH - path to txt FILENAME_ARTICLES file and for created files
    FILENAME_ARTICLES - file with name of article '\t' article id

    Returns:
    -
    """
    import json
    import os
    wiki_redirects = {}
    with open (os.path.join(PATH,FILENAME_REDIRECTIONS),'r') as f:
        for s in f:
            line = s.split('\n')[0]
            wiki_title_1,wiki_title_2 = line.split('\t')
            # wiki_title_1 = wiki_title_1.lower()
            # wiki_title_2 = wiki_title_2.lower()
            wiki_redirects[wiki_title_1] = wiki_title_2
    wiki_name_id_dict_redir = {}
    wiki_id_name_dict_redir = {}
    with open (os.path.join(PATH,"wiki_name_id.json")) as json_file:
        wiki_name_id_dict = json.load(json_file)
    with open (os.path.join(PATH,"wiki_id_name.json")) as json_file:
        wiki_id_name_dict = json.load(json_file)
    with open (os.path.join(PATH,'wiki_name_id_map.txt'),'r') as f:
        for s in f:
            line = s.split('\n')[0]
            wiki_title,wiki_id = line.split('\t')
            # wiki_title = wiki_title.lower()
            if wiki_title in wiki_redirects.keys() and wiki_redirects[wiki_title] in wiki_name_id_dict.keys():
                wiki_name_id_dict_redir[wiki_title] = wiki_name_id_dict[wiki_redirects[wiki_title]]
                wiki_id_name_dict_redir[wiki_id] = wiki_redirects[wiki_title]
            else:
                wiki_name_id_dict_redir[wiki_title] = wiki_id
                wiki_id_name_dict_redir[wiki_id] = wiki_title
    wiki_name_id_json = json.dumps(wiki_name_id_dict_redir)
    f = open(os.path.join(PATH,"wiki_name_id_with_redirections.json"),"w")
    f.write(wiki_name_id_json)
    f.close()
    wiki_id_name_json = json.dumps(wiki_id_name_dict_redir)
    f = open(os.path.join(PATH,"wiki_id_name_with_redirections.json"),"w")
    f.write(wiki_id_name_json)
    f.close()
    wiki_redirects_json = json.dumps(wiki_redirects)
    f = open(os.path.join(PATH,"wiki_redirects_names.json"),"w")
    f.write(wiki_redirects_json)
    f.close()
    return



def creating_several_txt_files_from_wiki_txt_dump(path = './wiki_articles',
                                                  filename = './textWithAnchorsFromAllWikipedia2014Feb.txt'):
    """Converts txt wiki dump to article per txt file with names 'id_article_id.txt'

    Parameters:
    path - folder to save created files
    filename (str) - file with txt wiki dump

    Returns:
    -
    """
    from html.parser import HTMLParser
    import os
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text=''
            self.filename=''
            self.doc=False

        def handle_starttag(self, tag, attrs):
            if tag == 'doc':
                attrs = dict(attrs)
                self.filename='_'.join(['id',attrs['id']])+'.txt'

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            self.text=data


    parser = MyHTMLParser()
    num_files = 0
    new_file=False
    with open(filename,'r') as f:
        for i,s in enumerate(f):
            if 'id='in s:
                parser.feed(s)
                num_files+=1
                new_file=True
            elif s!='\n':
                with open(os.path.join(path, parser.filename),'a') as f_w:
                    f_w.write(s)
            if num_files%10000==0 and new_file:
                print(num_files)
                new_file=False

    return
