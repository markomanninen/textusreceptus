#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: html.py

from IPython.display import HTML
import pandas as pd
from remarkuple import helper as h, table
from . math import digital_root, digital_sum
from . main import to_roman, to_greek, isopsephy, unicode_isopsephy

def _init_text(text, capitalize = None):
    return text.decode('utf-8')

def char_table_data(text, modulo = 9):
    # initialize data dictionary, split text to columns: #, letter, translit, num, sum, mod, word
    data = dict([key, []] for key in ['letter', 'transliteration', 'isopsephy', 'word'])
    # character chart
    # split words
    for word in _init_text(text).split():
        # split letters
        for idx, letter in enumerate(word):
            #data['index'].append(idx)
            data['letter'].append(letter)
            data['transliteration'].append(to_roman(letter.encode('utf-8')))
            data['isopsephy'].append(isopsephy(letter.encode('utf-8')))
            data['word'].append(word)

    data = pd.DataFrame(data)
    # word summary from character chart
    gb = data.groupby('word')
    data2 = gb.sum()
    data2['characters'] = gb['word'].apply(len)
    data2['digital_sum'] = data2['isopsephy'].apply(digital_sum)
    data2['digital_root'] = data2['isopsephy'].apply(digital_root)
    # phrase summary from word summary
    s = data2.sum()
    data3 = pd.DataFrame({'digital_root': [digital_root(s.isopsephy)],
                          'characters': [s.characters], 
                          'digital_sum': [digital_sum(s.isopsephy)],
                          'isopsephy': [s.isopsephy],
                          'phrase': text})

    return (data, data2, data3)


def char_table(text, modulo = 9):
    # initialize html table
    tbl = table(Class="char-table")
    # add caption / table title
    tbl.addCaption(text)
    # add data rows
    tr1 = h.tr() # greek letters
    tr2 = h.tr() # roman letters
    tr3 = h.tr() # isopsephy number
    tr4 = h.tr() # summary
    i = 0
    text = unicode(text, encoding="utf-8")
    for word in text.split():
        if i > 0:
            # add empty cells for word separation
            tr1 += h.th("&nbsp;")
            tr1 += h.th("&nbsp;")
            tr2 += h.td()
            tr2 += h.td(Class="empty-cell")
            tr3 += h.td()
            tr3 += h.td(Class="empty-cell")
            tr4 += h.td()
            tr4 += h.td()
        num = unicode_isopsephy(word)
        tr4 += h.td("%s %s" % (num, h.sub(digital_root(num))), colspan=len(word))
        i = i+1
        # add each letter on own cell
        for letter in word:
            tr1 += h.th(letter.encode('utf-8'))
            tr2 += h.td(to_roman(letter.encode('utf-8')))
            tr3 += h.td(unicode_isopsephy(letter))
    # add rows to table
    tbl.addHeadRow(tr1)
    tbl.addBodyRow(tr2)
    tbl.addBodyRow(tr3)
    tbl.addFootRow(tr4)
    # add summary footer for table
    num = unicode_isopsephy(text)
    tbl.addFootRow(h.tr(h.td("%s %s" % (num, h.sub(digital_sum(num), " / ", digital_root(num, modulo))), 
                             colspan=len(text)+len(text.split()), 
                             style="border-top: solid 1px #ddd")))
    return tbl