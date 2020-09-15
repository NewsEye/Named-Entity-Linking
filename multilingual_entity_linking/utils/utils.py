def string_starts(s, m):
    return s[:len(m)] == m

def split_sentence_in_words(s):
    return s.split()

def modify_uppercase_phrase(s):
    if s == s.upper():
        words = split_sentence_in_words( s.lower() )
        res = [ w.capitalize() for w in words ]
        return ' '.join( res )
    else:
        return s
