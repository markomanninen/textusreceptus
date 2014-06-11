#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

import re
import pandas as pd
from os.path import isfile
from remarkuple import helper as h, table
from isopsephy import preprocess_greek, to_roman, isopsephy
from IPython.display import HTML

dictionary = pd.DataFrame()

def load_dataframe(csv = "nt-strongs.csv"):
    global dictionary
    if isfile(csv):
        print "Retrieving data from local csv copy..."
        dictionary = pd.read_csv(csv, sep = "\t")
        # greek sords are pre processed for simpler forms without accents
        dictionary['word'] = dictionary['word'].map(lambda x: preprocess_greek(x))
        # adding transliteration of the words to the dataframe
        dictionary['transliteration'] = dictionary['word'].map(lambda x: to_roman(x))
        # adding word isopsephy value to the dataframe
        dictionary['isopsephy'] = dictionary['word'].map(lambda x: isopsephy(x))
    else:
        print "Cannot read csv file: %s! Please check path/filename and reload dictionary with load_dataframe(csv = \"your_filename\") function" % csv

def find(query, column):
    global dictionary
    # if culumn is "isopsephy" use == compare
    return dictionary[dictionary[column] == query] if column == 'isopsephy' else dictionary[dictionary[column].str.contains(query)]

def search_strongs_dictionary_table(query, field):
    # initialize tagpy table object
    tbl = table(Class='data')
    # add head row columns
    tbl.addHeadRow(h.tr(h.th('Lemma'), h.th('Word'), h.th('Transliteration'), h.th('Translation'), h.th('Isopsephy')))
    # make search. if field is isopsephy, force search item to int type
    rows = find(int(query) if field == 'isopsephy' else re.compile(query, re.IGNORECASE), field)
    for i, item in rows.iterrows():
        tbl.addBodyRow(h.tr(h.td(item.lemma), h.td(item.word), h.td(item.transliteration), h.td(item.translation), h.td(item.isopsephy)))
    return tbl

def search_strongs_dictionary_html(query, field):
    # using print data stream instead of returning data makes 
    # less hassle with unicodes and character encodings
    print str(search_strongs_dictionary_table(query, field))

#
def print_search_form_html():
    form = """
<h3>Search</h3>

<div class="search-input"><span>Greek</span> <input type="text" id="word" value="Αρμαγεδδων" /> <button onclick="search_strongs_dictionary('word')">Retrieve</button></div>
<div class="search-input"><span>Roman</span> <input type="text" id="transliteration" value="aarwn" /> <button onclick="search_strongs_dictionary('transliteration')">Retrieve</button></div>
<div class="search-input"><span>Lemma</span> <input type="text" id="lemma" value="G2424" /> <button onclick="search_strongs_dictionary('lemma')">Retrieve</button></div>
<div class="search-input"><span>Isopsephy</span> <input type="text" id="isopsephy" value="777" /> <button onclick="search_strongs_dictionary('isopsephy')">Retrieve</button></div>
<div class="search-input"><span>Translation</span> <input type="text" id="translation" value="flute" /> <button onclick="search_strongs_dictionary('translation')">Retrieve</button></div>

<h3>Results</h3>

<div id="result">

<table class="data"><thead><tr><th>Lemma</th><th>Word</th><th>Transliteration</th><th>Translation</th><th>Isopsephy</th></tr></thead><tbody><tr><td>G717</td><td>Αρμαγεδδων</td><td>Armageddwn</td><td>Armageddon (or Har-Meggiddon), a symbolic name</td><td>1008</td></tr></tbody></table>

</div>

<style>
div.search-input span {height: 16px; width: 80px; display: block; float: left;}
div.search-input input {height: 16px;}
div.search-input button {margin-top: -9px;}
</style>
"""
    return HTML(form)

def print_search_form_js():
    js = """
<script>

function handle_output(out_type, out) {
    var res = null
    if (out_type == "stream") {
        res = out.data
    } else if (out_type == "pyout") {
        res = out.data["text/plain"]
    } else if (out_type == "pyerr") {
        res = out.ename + ": " + out.evalue
    } else {
        res = "[output type: "+out_type+" is not implemented]";
    }
    document.getElementById("result").innerHTML = res
}

var callbacks = {'output' : handle_output}

function search_strongs_dictionary(field) {
    var kernel = IPython.notebook.kernel
    kernel.execute("search_strongs_dictionary_html('"+document.getElementById(field).value+"', '"+field+"')", callbacks, {silent:false})
}

</script>
"""
    return HTML(js)