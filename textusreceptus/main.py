#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

import re
import pandas as pd
from os.path import isfile
from remarkuple import helper as h
from IPython.display import HTML
from isopsephy import greek_letters as letters
from isopsephy import isopsephy, unicode_isopsephy, to_roman, find_cumulative_indices

__version__ = "0.0.1"

booknames = {
"40N": "Matthew",
"41N": "Mark",
"42N": "Luke",
"43N": "John",
"44N": "Acts of the Apostles",
"45N": "Romans",
"46N": "1 Corinthians",
"47N": "2 Corinthians",
"48N": "Galatians",
"49N": "Ephesians",
"50N": "Philippians",
"51N": "Colossians",
"52N": "1 Thessalonians",
"53N": "2 Thessalonians",
"54N": "1 Timothy",
"55N": "2 Timothy",
"56N": "Titus",
"57N": "Philemon",
"58N": "Hebrews",
"59N": "James",
"60N": "1 Peter",
"61N": "2 Peter",
"62N": "1 John",
"63N": "2 John",
"64N": "3 John",
"65N": "Jude",
"66N": "Revelation"
}

# will be transformed to pandas DataFrame
textus_vocabulary = {}

sletters = ''.join(letters)
c = '([%s]+) ([^%s]+)' % (sletters, sletters)
#c = "([%s]+.*?.-.{3})" % sletters
regex_word_strong_morph = re.compile(c)

c = '([%s]+)' % sletters
regex_word_isopsephy = re.compile(c)

c = '{VAR1: ([%s0-9A-Z\- ]+)}' % sletters

regex_variation1 = re.compile(c)

c = '{VAR2: ([%s0-9A-Z\- ]+)}' % sletters

regex_variation2 = re.compile(c)

regex_word_strong_morph_brackets = re.compile('\[(.*)\]')

textus_receptus_original_dir = "data_original/textus_receptus/"
textus_receptus_processed_dir = "data_processed/textus_receptus/"

#letters = "αΑβΒγΓδΔεΕϛϚϜϝζΖηΗθΘιΙυϒYκΚϡϠͲͳλΛωΩμΜτΤνΝξΞοΟσΣϹϲςπΠχΧϙϘϞϟρΡψΨφΦ"
#c = '([%s]+) ([^%s]+)' % (letters, letters)
#c = "([αΑβΒγΓδΔεΕϛϚϜϝζΖηΗθΘιΙυϒYκΚϡϠͲͳλΛωΩμΜτΤνΝξΞοΟσΣϹϲςπΠχΧϙϘϞϟρΡψΨφΦ]+.*?.-.{3})"
#c = u'([Ͱ-ϡ]+) ([A-Z0-9-]+)(?: ([A-Z0-9-]+))? ([A-Z0-9-]+)(?=\\s|$)'

def load_dataframe(filename):
    global textus_vocabulary
    csvOriginalFileName = textus_receptus_original_dir+filename
    csvProcessedFileName = textus_receptus_processed_dir+filename

    if isfile(csvProcessedFileName + ".csv"):
        print "Retrieving data from local csv copy..."
        textus_vocabulary = pd.read_csv(csvProcessedFileName + "_dict.csv")
        df = pd.read_csv(csvProcessedFileName + ".csv")
        df['text'] = df['text'].fillna('missing')
        df['text_isopsephy'] = df['text'].apply(lambda verse: verse_isopsephy_numbers(verse))
        df['total_isopsephy'] = df['text_isopsephy'].apply(lambda x: sum(x))
        return df

    print "Processing data from original csv file..."

    df = pd.read_csv(csvOriginalFileName + ".csv", sep="	", index_col=False)

    del df['orig_subverse']
    del df['order_by']

    df['orig_book_index'] = df['orig_book_index'].apply(lambda index: booknames[index])
    df['text'] = df['text'].apply(lambda verse: parse_verse(verse))
    #df['text'] = df['text'].fillna('missing')
    df.to_csv(csvProcessedFileName + ".csv", index=False)

    df['text_isopsephy'] = df['text'].apply(lambda verse: verse_isopsephy_numbers(verse))
    df['total_isopsephy'] = df['text_isopsephy'].apply(lambda x: sum(x))

    textus_vocabulary = pd.DataFrame(textus_vocabulary)
    textus_vocabulary.to_csv(csvProcessedFileName + "_dict.csv", index=False)

    return df

#v = "βιβλος G976 N-NSF γενεσεως G1078 N-GSF ιησου G2424 N-GSM χριστου G5547 N-GSM υιου G5207 N-GSM δαβιδ G1138 N-PRI υιου G5207 N-GSM αβρααμ G11 N-PRI"
#print pd.DataFrame(parse_verse(v))

# [] are found 14 times on manuscripts and are removed on this application
#v = "μονω G3441 A-DSM σοφω G4680 A-DSM θεω G2316 N-DSM δια G1223 PREP ιησου G2424 N-GSM χριστου G5547 N-GSM  {VAR1: ω G3739 R-DSM } η G3588 T-NSF δοξα G1391 N-NSF εις G1519 PREP τους G3588 T-APM αιωνας G165 N-APM αμην G281 HEB [προς G4314 PREP ρωμαιους G4514 A-APM εγραφη G1125 G5648 V-2API-3S απο G575 PREP κορινθου G2882 N-GSF δια G1223 PREP φοιβης G5402 N-GSF της G3588 T-GSF διακονου G1249 N-GSF της G3588 T-GSF εν G1722 PREP κεγχρεαις G2747 N-DPF εκκλησιας G1577 N-GSF]"
#print pd.DataFrame(parse_verse(v))

# {VAR1: } and {VAR2: } are found few hundred times on manuscripts. VAR2 is removed and VAR1 is kept.
#v = "και G2532 CONJ υμας G5209 P-2AP νεκρους G3498 A-APM οντας G5607 G5752 V-PXP-APM εν G1722 PREP τοις G3588 T-DPN παραπτωμασιν G3900 N-DPN και G2532 CONJ τη G3588 T-DSF ακροβυστια G203 N-DSF της G3588 T-GSF σαρκος G4561 N-GSF υμων G5216 P-2GP  {VAR1: συνεζωποιησεν G4806 V-AAI-3S } {VAR2: συνεζωοποιησεν G5656 V-AAI-3S } συν G4862 PREP αυτω G846 P-DSM χαρισαμενος G5483 G5666 V-ADP-NSM  {VAR1: ημιν G2254 P-1DP } {VAR2: υμιν G5213 P-2DP } παντα G3956 A-APN τα G3588 T-APN παραπτωματα G3900 N-APN"
#print pd.DataFrame(parse_verse(v))

def parse_verse(verse):
    global textus_vocabulary
    verse = verse.decode('utf-8')
    # uncertain parts marked between [] are removed
    x = regex_word_strong_morph_brackets.search(verse)
    if x:
        verse = verse.replace('['+x.group(1)+']', '')
    # variation 1 marked with {VAR1 ...} is left
    x = regex_variation1.findall(verse)
    if x:
        for y in x:
            verse = verse.replace('{VAR1: '+y+'}', y).replace('  ', ' ')
    # variation 2 marked with {VAR2 ... } is removed
    x = regex_variation2.findall(verse)
    if x:
        for y in x:
            verse = verse.replace('{VAR2: '+y+'}', '').replace('  ', ' ')
    # collecting and returning words from verse
    verse_words = []
    #for x in regex_word_strong_morph.findall(verse):
    for tupleitem in [[x[0]] + x[1].split() for x in regex_word_strong_morph.findall(verse)]:
        #tupleitem = x.split()
        # adding isopsephy value to (word, strongs, morph) tuple
        item = []
        item.append(tupleitem[0].encode('utf-8'))
        item.append(tupleitem[1].encode('utf-8'))
        if len(tupleitem) == 4:
            item.append(tupleitem[3].encode('utf-8'))
        else:
            item.append(tupleitem[2].encode('utf-8'))

        item.append(isopsephy(item[0]))
        # adding transliteration
        item.append(to_roman(item[0]))
        # add word for verse
        verse_words.append(item[0])
        # adding item to textus dictionary, but removing first item (greek word) from tuple
        textus_vocabulary[item[0]] = item[1:]
    return " ".join(verse_words)

def verse_isopsephy_numbers(verse):
    return map(isopsephy, verse.split()) if type(verse) is str else []

def match_isopsephy_combinations(num):
    global dataframe
    dataframe['search'] = dataframe['text_isopsephy'].apply(lambda numbers: find_cumulative_indices(numbers, num))
    rows = dataframe[dataframe['search'] != ''].sort('orig_book_index', ascending=True)
    del dataframe['search']
    return rows.sort(['orig_book_index', 'orig_chapter', 'orig_verse'])

def match_phrase(phrase, books = []):
    dataframe['text'] = dataframe['text'].fillna('missing')
    if books:
        rows = dataframe[dataframe['orig_book_index'].str.contains('|'.join(books))]
        rows = rows[rows['text'].str.contains(phrase)]
    else:
        rows = dataframe[dataframe['text'].str.contains(phrase)]
    rows['search'] = rows['text_isopsephy'].apply(lambda numbers: find_cumulative_indices(numbers, isopsephy(phrase)))
    return rows

def get_verse(book, chapter, verse):
    return ''.join(dataframe[dataframe['orig_book_index']==book][dataframe['orig_chapter']==chapter][dataframe['orig_verse']==verse].text)

def list_rows(rows):
    ul = h.ul()
    for idx, row in rows.iterrows():
        words = row.text.split(" ")
        for i in row.search:
            for j in i:
                words[j] = str(h.b(words[j], style="color: brown; text-decoration: underline; cursor: pointer", title=to_roman(words[j])))
        reference = h.span(h.b("%s %s:%s" % (row['orig_book_index'], row.orig_chapter, row.orig_verse)))
        ul += h.li(reference, " - ", h.span(' '.join(words)))

    return HTML(str(ul))

dataframe = load_dataframe("greek_textus_receptus_utf8")