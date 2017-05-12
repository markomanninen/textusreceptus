#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

import re
import pandas as pd
from . search import find_cumulative_indices

data = {}

"""

Data mapping between roman and greek letters, isopsephy values and linguistic components

Resources:

- http://en.wikipedia.org/wiki/Greek_alphabet
- http://www.chlt.org/FirstGreekBook/JWW_FGB1.html
- http://www.webtopos.gr/eng/languages/greek/alphabet/alpha.htm
- http://www.class.uh.edu/mcl/faculty/pozzi/grnl1/intr/0.2.1.pract.vow.htm

Segments:
- vowel
- consonant
- numeral

Subsegments:
- semivowel (liquid, siblant and γ-nasal not specified on data table)
- double
- mute

Mutes (not specified on data table):

{class-order} {letter}

labial-smooth π
labial-middle β
labial-rought φ

palatal-smooth κ
palatal-middle γ
palatal-rought χ

lingual-smooth τ
lingual-middle δ
lingual-rought θ

Seven vowels: α ε η ι ο υ ω (a e h i o u w)

Numerals: ϛ ϙ ϡ (6, 90, 900)

If numerals are found on greek text, their values are used on isopsephy calculation
but there are no corresponding roman letters for them. This is mainly because roman alphabet
has only 26 letters, so one would need to use arbitrary 2 letters (like j, v) and some other special
character for the last letter like _ or number or anything. But it doesn't really make sense.

My choice was just to use numerical value on transliterated text, so ϛ, ϙ and ϡ will be transliterated to 6, 90, 900. 
However, if you transform roman to greek, only literals are handled, no numbers at all.

"""

# letters from α to θ (1 to 9)
# alpha:http://en.wiktionary.org/wiki/ἄλφα
data[1] = {'greek': u'α', 
           'capital': u'Α',
           'name': u'αλφα',
           'segment': 'vowel',
           'subsegment': 'short',
           'roman': 'a',
           'value': 1}
# beta:http://en.wiktionary.org/wiki/βῆτα
data[2] = {'greek': u'β',
           'capital': u'Β',
           'name': u'βητα',
           'segment': 'consonant',
           'subsegment': 'mute',
           'roman': 'b',
           'value': 2}
# gamma:http://en.wiktionary.org/wiki/γάμμα
data[3] = {'greek': u'γ',
           'capital': u'Γ',
           'name': u'γαμμα',
           'segment': 'consonant',
           'subsegment': 'mute',
           'roman': 'g',
           'value': 3}
# delta:http://en.wiktionary.org/wiki/δέλτα
data[4] = {'greek': u'δ',
           'capital': u'Δ',
           'name': u'δελτα',
           'segment': 'consonant',
           'subsegment': 'mute',
           'roman': 'd',
           'value': 4}
# epsilon:http://en.wiktionary.org/wiki/epsilon
data[5] = {'greek': u'ε',
           'capital': u'Ε',
           'name': u'ε ψιλον',
           'segment': 'vowel',
           'subsegment': 'short',
           'roman': 'e',
           'value': 5}
# digamma/stigma/episemon/wau
# http://en.wikipedia.org/wiki/Digamma
data[6] = {'greek': u'ϛ', 'small2': u'ϝ',
           'capital': u'Ϛ', 'capital2': u'Ϝ',
           'name': u'διγαμμα', 'name2': u'στιγμα', 'name3': u'επισημον', 'name4': u'βαυ',
           'segment': 'numeral',
           #'subsegment': '',
           'roman': '6',
           'value': 6}
# zeta:http://en.wiktionary.org/wiki/ζῆτα
data[7] = {'greek': u'ζ',
           'capital': u'Ζ',
           'name': u'ζητα',
           'segment': 'consonant',
           'subsegment': 'double',
           'roman': 'z',
           'value': 7}
# eta:http://en.wiktionary.org/wiki/ἦτα
data[8] = {'greek': u'η',
           'capital': u'Η',
           'name': u'ητα',
           'segment': 'vowel',
           'subsegment': 'long',
           'roman': 'h',
           'value': 8}
# theta:http://en.wiktionary.org/wiki/θῆτα
data[9] = {'greek': u'θ',
           'capital': u'Θ',
           'name': u'θητα',
           'segment': 'consonant',
           'subsegment': 'mute',
           'roman': 'q',
           'value': 9}

# letters from ι to ϙ (10 to 90)
# iota:http://en.wiktionary.org/wiki/ἰῶτα
data[10] = {'greek': u'ι',
            'capital': u'Ι',
            'name': u'ιωτα',
            'segment': 'vowel',
            'subsegment': 'short',
            'roman': 'i',
            'value': 10}
# kappa:http://en.wiktionary.org/wiki/κάππα
data[20] = {'greek': u'κ',
            'capital': u'Κ',
            'name': u'καππα',
            'segment': 'consonant',
            'subsegment': 'mute',
            'roman': 'k',
            'value': 20}
# lambda:http://en.wiktionary.org/wiki/λάμβδα
data[30] = {'greek': u'λ',
            'capital': u'Λ',
            'name': u'λαμβδα',
            'segment': 'consonant',
            'subsegment': 'semivowel',
            'roman': 'l',
            'value': 30}
# mu:http://en.wiktionary.org/wiki/mu
data[40] = {'greek': u'μ',
            'capital': u'Μ',
            'name': u'μυ',
            'segment': 'consonant',
            'subsegment': 'semivowel',
            'roman': 'm',
            'value': 40}
# nu:http://en.wiktionary.org/wiki/νῦ
data[50] = {'greek': u'ν',
            'capital': u'Ν',
            'name': u'νυ',
            'segment': 'consonant',
            'subsegment': 'semivowel',
            'roman': 'n',
            'value': 50}
# xi:http://en.wiktionary.org/wiki/ξεῖ
data[60] = {'greek': u'ξ',
            'capital': u'Ξ',
            'name': u'ξει',
            'segment': 'consonant',
            'subsegment': 'double',
            'roman': 'c',
            'value': 60}
# omicron:http://en.wiktionary.org/wiki/omicron
data[70] = {'greek': u'ο',
            'capital': u'Ο',
            'name': u'ο μικρον',
            'segment': 'vowel',
            'subsegment': 'short',
            'roman': 'o',
            'value': 70}
# pi:http://en.wiktionary.org/wiki/πεῖ
data[80] = {'greek': u'π',
            'capital': u'Π',
            'name': u'πει',
            'segment': 'consonant',
            'subsegment': 'mute',
            'roman': 'p',
            'value': 80}
# koppa:http://en.wikipedia.org/wiki/Koppa_(letter)
# http://www.webtopos.gr/eng/languages/greek/alphabet/earlyletters.htm
data[90] = {'greek': u'ϙ', 'small2': u'ϟ',
            'capital': u'Ϙ', 'capital2': u'Ϟ',
            'name': u'κοππα',
            'segment': 'numeral',
            #'subsegment': '',
            'roman': '90',
            'value': 90}

# letters from ρ to ϡ (100 to 900)
# rho:http://en.wiktionary.org/wiki/ῥῶ
data[100] = {'greek': u'ρ',
             'capital': u'Ρ',
             'name': u'ρω',
             'segment': 'consonant',
             'subsegment': 'semivowel',
             'roman': 'r',
             'value': 100}
# sigma:http://en.wiktionary.org/wiki/σίγμα
data[200] = {'greek': u'σ', 'small2': u'ϲ', 'small3': u'ς',
             'capital': u'Σ', 'capital2': u'Ϲ', 'capital3': u'Σ',
             'name': u'σιγμα',
             'segment': 'consonant',
             'subsegment': 'semivowel',
             'roman': 's',
             'value': 200}
# tau:http://en.wiktionary.org/wiki/tau
data[300] = {'greek': u'τ',
             'capital': u'Τ',
             'name': u'ταυ',
             'segment': 'consonant',
             'subsegment': 'mute',
             'roman': 't',
             'value': 300}
# upsilon:http://en.wiktionary.org/wiki/upsilon
data[400] = {'greek': u'υ',
             'capital': u'ϒ', 'capital2': u'Y',
             'name': u'υ ψιλον',
             'segment': 'vowel',
             'subsegment': 'short',
             'roman': 'u',
             'value': 400}
# phi:http://en.wiktionary.org/wiki/phi
data[500] = {'greek': u'φ',
             'capital': u'Φ',
             'name': u'φει',
             'segment': 'consonant',
             'subsegment': 'mute',
             'roman': 'f',
             'value': 500}
# khi, chi:http://en.wiktionary.org/wiki/chi
data[600] = {'greek': u'χ',
             'capital': u'Χ',
             'name': u'χει',
             'segment': 'consonant',
             'subsegment': 'mute',
             'roman': 'x',
             'value': 600}
# psi:http://en.wiktionary.org/wiki/psi
data[700] = {'greek': u'ψ',
             'capital': u'Ψ',
             'name': u'ψει',
             'segment': 'consonant',
             'subsegment': 'double',
             'roman': 'y',
             'value': 700}
# omega:http://en.wiktionary.org/wiki/omega
data[800] = {'greek': u'ω',
             'capital': u'Ω',
             'name': u'ω μεγα',
             'segment': 'vowel',
             'subsegment': 'long',
             'roman': 'w',
             'value': 800}
# sampi/disigma
# http://en.wikipedia.org/wiki/Sampi
# http://www.tlg.uci.edu/~opoudjis/unicode/other_nonattic.html#sampi
# http://www.parthia.com/fonts/sampi.htm
# http://www.jstor.org/stable/636031
data[900] = {'greek': u'ϡ', 'small2': u'ͳ',
             'capital': u'Ϡ', 'capital2': u'Ͳ',
             'name': u'σαμπι', 'name2': u'δισιγμα',
             'segment': 'numeral',
             #'subsegment': '',
             'roman': '900',
             'value': 900}

greek_roman_values = {}
greek_roman_letters = {}
roman_greek_letters = {}

keys = ['roman', 'greek', 'capital', 'capital2', 'small2', 'small3', 'small4']
for num, d in data.items():
    for k in keys:
        if k in d:
            greek_roman_values[d[k]] = num
            if k == 'roman':
                if d['segment'] != 'numeral':
                    greek_roman_letters[d[k]] = d['greek']
                    greek_roman_letters[d[k].upper()] = d['capital']
                greek_roman_values[d[k].upper()] = num
            else:
                if 'roman' in d:
                    if k == 'capital' or k == 'capital2':
                        roman_greek_letters[d[k]] = d['roman'].upper()
                    else:
                        roman_greek_letters[d[k]] = d['roman']

greek_letters = ''
keys = ['greek', 'capital', 'capital2', 'small2', 'small3', 'small4']
for num, d in data.items():
    for k in keys:
        if k in d:
            #αΑβΒγΓδΔεΕϛϚϜϝζΖηΗθΘιΙυΥκΚϡϠͲͳλΛωΩμΜτΤνΝξΞοΟσΣϹϲςπΠχΧϙϘϞϟρΡψΨφΦ
            greek_letters += d[k]

regex_greek_roman_values = re.compile('|'.join(greek_roman_values.keys()))
regex_greek_to_roman_letters = re.compile('|'.join(roman_greek_letters.keys()))
regex_roman_to_greek_letters = re.compile('|'.join(greek_roman_letters.keys()))
regex_has_numbers = re.compile('\d')
isopsephy_error_msg = "String '%s' contains unsupported characters for isopsephy calculation"

class IsopsephyException(Exception):
    pass

def isopsephy(string):
    """
    String is a greek letter, word or sentence OR roman letter representation (transliteration) 
    of the greek letter, word or sentence that will be converted to the numerical value letter by letter
    Main function will convert input to unicode format for easier frontend, but on module logic
    more straightforward function unicode_isopsephy is used.
    """
    return unicode_isopsephy(string)

def unicode_isopsephy(string):
    """
    String argument must be in unicode format.
    """
    result = 0
    # don't accept strings that contain numbers
    if regex_has_numbers.search(string):
        raise IsopsephyException(isopsephy_error_msg % string)
    else:
        num_str = regex_greek_roman_values.sub(lambda x: '%s ' % greek_roman_values[x.group()],
                                               string)
        # don't accept strings, that contains letters which haven't been be converted to numbers
        try:
            result = sum([int(i) for i in num_str.split()])
        except Exception as e:
            raise IsopsephyException(isopsephy_error_msg % string)
    return result

def to_roman(word):
    """
    Create a roman letter version of the greek word.
    This will change all greek (primary), capital, capital2, small2, small3, and small4
    letters to roman letter. Capital letters are honored.
    """
    return regex_greek_to_roman_letters.sub(lambda x: roman_greek_letters[x.group()],
                                            word).encode('utf-8')

def to_greek(word):
    """
    Create a greek version of the roman letter word.
    This will change a-zA-Z except j, J, v & V to the corresponding greek letters
    Capital letters are honored.
    """
    return regex_roman_to_greek_letters.sub(lambda x: greek_roman_letters[x.group()],
                                            word).encode('utf-8')

names = {'name': 'name_value', 'name2': 'name_value2', 'name3': 'name_value3', 'name4': 'name_value4'}
for num, d in data.items():
    for k, v in names.items():
        if k in d:
            d[v] = unicode_isopsephy(d[k])

# accents / diacritics for simplified greek letters

_accents_ = {}

_accents_[u'Α'] = u"Ἀ Ἄ Ἂ Ἆ ᾏ ᾈ ᾌ ᾊ ᾎ Ά Ἁ Ἅ Ἃ Ἇ Ὰ ᾼ ᾉ ᾍ ᾋ Ἀ"
_accents_[u'α'] = u"ἀ ά ἄ ᾶ ᾳ ὰ ά ἀ ἁ ἂ ἃ ἄ ἅ ἆ ἇ ᾀ ᾁ ᾂ ᾃ ᾄ ᾅ ᾆ ᾇ ᾲ ᾳ ᾴ ᾶ ᾷ"

_accents_[u'Ε'] = u"Έ Ἑ Ἕ Ἓ Ὲ Ἐ Ἔ Ἒ"
_accents_[u'ε'] = u"έ ἔ ἐ ὲ έ ἐ ἑ ἒ ἓ ἔ ἕ"

_accents_[u'Η'] = u" ᾚ ᾞ Ἠ Ἤ Ἢ Ἦ Ή Ἡ Ἥ Ἣ Ἧ Ὴ ῌ ᾙ ᾝ ᾛ ᾟ ᾘ ᾜ"
_accents_[u'η'] = u"ή ἡ ῆ ἤ ἦ ὴ ῃ ὴ ή ᾐ ᾑ ᾒ ᾓ ᾔ ᾕ ᾖ ᾗ ῂ ῃ ῄ ῆ ῇ ἠ ἡ ἢ ἣ ἤ ἥ ἦ ἧ"

_accents_[u'Ι'] = u"Ί Ἱ Ἵ Ἳ Ἷ Ὶ Ἰ Ἴ Ἲ Ἶ Ἱ"
_accents_[u'ι'] = u"ἱ ἰ ἴ ί ῖ ἷ î ì ἶ ὶ ί ῒ ΐ ῖ ῗ ἰ ἱ ἲ ἳ ἴ ἵ ἶ ἷ ϊ"

_accents_[u'Ο'] = u"Ό Ὁ Ὅ Ὃ Ὸ Ὀ Ὄ Ὂ"
_accents_[u'ο'] = u"ὁ ò ó ô ὄ ὅ ὸ ό ὀ ὁ ὂ ὃ ὄ ὅ"

_accents_[u'Ρ'] = u"Ῥ"
_accents_[u'ρ'] = u"ῥ ῤ"

_accents_[u'ϒ'] = u"Ύ Ὑ Ὕ Ὓ Ὗ Ὺ Ῡ"
_accents_[u'υ'] = u"ῦ ύ ϋ ὐ ὕ ὖ ù ὑ ὺ ύ ὐ ὑ ὒ ὓ ὔ ὕ ὖ ὗ ῠ ῡ ῢ ΰ ῦ ῧ"

_accents_[u'Ω'] = u"ᾪ ᾮ Ὠ Ὤ Ὢ Ὦ Ώ Ὡ Ὥ Ὣ Ὧ Ὼ ῼ ᾩ ᾭ ᾫ ᾯ ᾨ ᾬ"
_accents_[u'ω'] = u"ὥ ῶ ὧ ώ ὠ ῳ ᾧ ὼ ώ ὠ ὡ ὢ ὣ ὤ ὥ ὦ ὧ ᾠ ᾡ ᾢ ᾣ ᾤ ᾥ ᾦ ᾧ ῲ ῳ ῴ ῶ ῷ"

accents = {}

for letter, values in _accents_.items():
    for value in values.split():
        accents[value] = letter

regex_roman = re.compile(r'[^abcdefghiklmnopqrstuwxyz ]+', re.IGNORECASE)
def preprocess_roman(string):
    # regex to remove all special characters leaving only a-z and empty scape
    # for example: a)a/atos tau1 -> aaatos tau
    return regex_roman.sub('', string)

regex_greek = re.compile('|'.join(accents.keys()))
regex_greek2 = re.compile('[^%s ]+' % u"αΑβΒγΓδΔεΕϛϚϜϝζΖηΗθΘιΙυϒYκΚϡϠͲͳλΛωΩμΜτΤνΝξΞοΟσΣϹϲςπΠχΧϙϘϞϟρΡψΨφΦ")
def preprocess_greek(string):
    # convert diacritics to simpler forms
    #string = unicode(string, encoding="utf-8")
    string = regex_greek.sub(lambda x: accents[x.group()], string)
    # remove all other characters
    return regex_greek2.sub('', string).encode('utf-8')

def find(text, num, cumulative = False):
    words = text.split()
    numbers = list(map(isopsephy, words))
    if cumulative:
        result = []
        for incides in find_cumulative_indices(numbers, num):
            result.append(' '.join([words[idx] for idx in incides]))
        return result
    else:
        return [words[idx] for idx in map(numbers.index, numbers) if numbers[idx] == num]
