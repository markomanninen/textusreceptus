#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: __init__.py

from . main import load_dataframe, find, preprocess_greek, \
                   search_strongs_dictionary_html, \
                   print_search_form_html, print_search_form_js

load_dataframe(csv = "strongs/nt-strongs.csv")
