exec(open("entities/ent_name2id_freq/ent_name_id.py").read())

def extract_text_and_hyp(line, mark_mentions):
    list_hyp = {} #-- (mention, entity) pairs
    text = ''
    list_ent_errors = 0
    parsing_errors = 0
    disambiguation_ent_errors = 0
    diez_ent_errors = 0

    end_end_hyp = 0
    begin_end_hyp = 0
    begin_start_hyp = line.find('<a href="')
    end_start_hyp = begin_start_hyp + len('<a href="') # -1

    num_mentions = 0

    while begin_start_hyp > 0 and begin_start_hyp <= len(line)+1:
        # print('----------------------')
        # print(text)
        text += line[end_end_hyp:begin_start_hyp]
        #print(begin_start_hyp)
        next_quotes = line[end_start_hyp:].find('">') + end_start_hyp
        end_quotes = next_quotes + len('">')

        if next_quotes:
            ent_name = line[end_start_hyp: next_quotes]
            begin_end_hyp = line[end_quotes:].find('</a>') + end_quotes
            end_end_hyp = begin_end_hyp + len('</a>')

            if begin_end_hyp:
                mention = line[end_quotes: begin_end_hyp].strip()
                mention_marker = False

                good_mention = True
                good_mention = good_mention and (mention.find('Wikipedia') < 0)
                good_mention = good_mention and (mention.find('wikipedia') < 0)
                good_mention = good_mention and (len(mention) >= 1)

                if good_mention:
                    i = ent_name.find('wikt:')
                    if i == 0:
                        ent_name = ent_name[5:]
                    ent_name = preprocess_ent_name(ent_name)
                    i = ent_name.find('List of ')
                    if i == -1:
                        if ent_name.find('#') > -1:
                            diez_ent_errors = diez_ent_errors + 1
                        else:
                            ent_wikiid = get_ent_wikiid_from_name(ent_name, True)
                            if ent_wikiid == unk_ent_wikiid:
                                disambiguation_ent_errors = disambiguation_ent_errors + 1
                            else:
                                # A valid (entity,mention) pair
                                num_mentions = num_mentions + 1
                                list_hyp[mention] = {'ent_wikiid': ent_wikiid, 'cnt': num_mentions}
                                if mark_mentions:
                                    mention_marker = True
                    else:
                        list_ent_errors = list_ent_errors + 1

                if not mention_marker:
                    text += ' ' + mention + ' '
                else:
                    text += ' MMSTART' + str(num_mentions) + ' ' + mention + ' MMEND' + str(num_mentions) + ' '

            else:
                parsing_errors = parsing_errors + 1
                begin_start_hyp = -1
        else:
            parsing_errors = parsing_errors + 1
            begin_start_hyp = -1

        if begin_start_hyp:
            if line[end_start_hyp:].find('<a href="') > 0:
                begin_start_hyp = line[end_start_hyp:].find('<a href="') + end_start_hyp
                end_start_hyp = begin_start_hyp + len('<a href="')
            else:
                begin_start_hyp, end_start_hyp = -1,-1

    if end_end_hyp:
        text += line[end_end_hyp:]
    else:
        if not mark_mentions:
            text = line #-- Parsing did not succed, but we don't throw this line away.
        else:
            text = ''
            list_hyp = {}

    return list_hyp, text, list_ent_errors, parsing_errors, disambiguation_ent_errors, diez_ent_errors

def extract_page_entity_title(line):
    startoff = line.find('<doc id="')
    endoff = startoff + len('<doc id="')
    startquotes = line[endoff:].find('"') + endoff
    ent_wikiid = line[endoff:startquotes]
    starttitlestartoff = line.find(' title="')
    starttitleendoff = starttitlestartoff + len(' title="')
    endtitleoff = line.find('">')
    ent_name = line[starttitleendoff:endtitleoff]
    if ent_wikiid != get_ent_wikiid_from_name(ent_name, True):
        # Most probably this is a disambiguation or list page
        new_ent_wikiid = get_ent_wikiid_from_name(ent_name, True)
        return new_ent_wikiid
    return ent_wikiid
