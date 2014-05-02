#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: search.py

def find_cumulative_indices(list_of_numbers, search_sum):
    """ 
    find_cumulative_indices([70, 58, 81, 909, 70, 215, 70, 1022, 580, 930, 898], 285) ->
    [[4, 5],[5, 6]]
    """
    u = 0
    y = 0
    result = []
    for idx, val in enumerate(list_of_numbers):
        y += list_of_numbers[idx]
        while y >= search_sum:
            if y == search_sum:
                result.append(range(u, idx+1))
            y -= list_of_numbers[u]
            u += 1
    # if matches are not found, empty string is returned
    # for easier cell data handling on pandas dataframe
    return result or ''

# http://stackoverflow.com/questions/21380268/matching-the-sum-of-values-on-string

def search_by_num(text, num):
    return list2string(find_number(string2list(text), num))

def list2string(alist):
    return " ".join(map(str, alist))

def string2list(slist):
    return list(map(int, slist.split()))

def find_number(alist, total):
    u = 0
    y = 0 # the current sum of the interval (u .. v)
    res = []
    for v in range(0, len(alist)):
        # at this point the interval sum y is smaller than the requested total,
        # so we move the right end of the interval forward
        y += alist[v]
        while y >= total:
            if y == total:
                res.append(list2string(alist[ u : v+1 ]))
            # if the current sum is too large, move the left end of the interval forward
            y -= alist[u]
            u += 1
    return res