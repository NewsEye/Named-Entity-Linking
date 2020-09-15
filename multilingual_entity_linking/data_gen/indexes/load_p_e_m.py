exec(open("entities/ent_name2id_freq/ent_name_id.py").read())

ent_p_e_m_index = {}
mention_lower_to_one_upper = {}
mention_total_freq = {}
num_lines = 0

print("Loading " + 'generated/' + args.language + '/merge-wikipedia_p_e_m.txt' + " ...")
with open('generated/' + args.language + '/merge-wikipedia_p_e_m.txt', encoding="utf-8") as f:
    for line in f:
        num_lines += 1
        if num_lines % 5000000 == 0:
            print('Processed ' + str(num_lines) + ' lines. ')

        line = unquote(line.strip())
        parts = line.split('\t')
        mention = parts[0]
        total = len(parts)
        if total >= 1:
            ent_p_e_m_index[mention] = {}
            mention_lower_to_one_upper[mention.lower()] = mention
            mention_total_freq[mention] = total
            num_parts = len(parts)
            for i in range(2,num_parts):
                ent_str = parts[i].split(',')
                ent_wikiid = ent_str[0]
                freq = int(ent_str[1])
                ent_p_e_m_index[mention][ent_wikiid] = freq / float(total + 0.0) # not sorted

def preprocess_mention(mention):
    cur_m = modify_uppercase_phrase(mention)
    if cur_m not in ent_p_e_m_index:
        cur_m = mention

    if mention in mention_total_freq and mention_total_freq[mention] > mention_total_freq[cur_m]:
        cur_m = mention # Cases like 'U.S.' are handed badly by modify_uppercase_phrase

    # If we cannot find the exact mention in our index, we try our luck to find it in a case insensitive index.
    if cur_m not in ent_p_e_m_index and cur_m.lower() in mention_lower_to_one_upper:
        cur_m = mention_lower_to_one_upper[ cur_m.lower() ]

    return cur_m
