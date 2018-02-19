import random
from random import choice

import re
from collections import Counter
import nltk
from nltk.util import ngrams

def read_file(filename):
    with open(filename, "r", encoding='UTF-8') as file: 
        contents = file.read().replace('\n\n',' ').replace('[edit]', ' ').replace('\ufeff', '').replace('\n', ' ').replace('\u3000', ' ')
        rgx = '([XCILV]+)\w\.|([V]+)\.|([X]+)\.|([I]+)\.|([C]+)\.'
        contents = re.sub(rgx, '', contents)
        return contents

text=read_file('rubaiyat.txt')
text_start = [m.start() for m in re.finditer('I.', text)]
text_end = [m.start() for m in re.finditer('End of Project Gutenberg', text)]
text = text[text_start[1]:text_end[0]]

def collect_dict(corpus, n_grams):
    text_dict = {}
    words = nltk.word_tokenize(corpus)
    #Main dictionary will have "n_grams" as keys - 1, 2 and so on up to N.
    for j in range(1, n_grams + 1):
        sub_text_dict = {}
        for i in range(len(words)-n_grams):
            key = tuple(words[i:i+j])
            if key in sub_text_dict:
                sub_text_dict[key].append(words[i+n_grams])
            else:
                sub_text_dict[key] = [words[i+n_grams]]
        text_dict[j] = sub_text_dict
    
    return text_dict

def get_next_word(key_id, min_length):
    for i in range(len(key_id)):
        if key_id in word_pairs[len(key_id)]:
            if len(word_pairs[len(key_id)][key_id]) >= min_length:
                return random.choice(word_pairs[len(key_id)][key_id])
        else:
            pass
        
        if len(key_id) > 1:
            key_id = key_id[1:]

    return random.choice(word_pairs[len(key_id)][key_id])

def generate_text(words, limit = 100, min_length = 3):
    capitalized_keys = [i for i in words[max(words.keys())].keys() if len(i[0]) > 0 and i[0][0].isupper()]
    first_key = random.choice(capitalized_keys)
    markov_text = ' '.join(first_key)
    while len(markov_text.split(' ')) < limit:
        next_word = get_next_word(first_key, min_length)
        first_key = tuple(first_key[1:]) + tuple([next_word])
        markov_text += ' ' + next_word
    for i in ['.', '?', '!', ',', '\"', '\'']:
        markov_text = markov_text.replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?').replace(' ;', ';'.replace(' \"', '\"').replace(' \'', '\''))
    markov_text = re.sub('[#:"\']', '', markov_text)
    return markov_text

word_pairs = collect_dict(text, 2)
markov_text = generate_text(word_pairs, 140, 2)
print(markov_text)
