#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

from copy import deepcopy

class TAG(object):
    """ Simple html tag generator """
    def __init__(self, *args, **kw):
        self._name = self.__class__.__name__.lower()
        self._attributes = dict([k.lower(), str(w)] for k, w in kw.iteritems())
        self._in = []
        self._left = []
        self._right = []
        map(self.__lshift__, args)

    def getName(self):
        return self._name
    def setName(self, name):
        self._name = name
        return self

    def getAttribute(self, key):
        return self._attributes[key] if self._attributes.has_key(key) else None
    def setAttribute(self, key, value):
        self._attributes[key] = value
        return self

    def rcontent(self, item):
        return self.__rshift__(item)
    def __rshift__(self, item):
        self._in = [item] + self._in
        return self

    def content(self, item):
        return self.__lshift__(item)
    def __lshift__(self, item):
        self._in.append(item)
        return self

    def prepend(self, item):
        return self.__radd__(item)
    def __radd__(self, item):
        self._left.append(item)
        return self

    def append(self, item):
        return self.__add__(item)
    def __add__(self, item):
        self._right.append(item)
        return self

    def renderAttributes(self):
        attr = ''
        if self._attributes:
            attr = ''.join([' %s="%s"' % (k, v) for k, v in self._attributes.iteritems()])
        return attr

    def __str__(self):

        left = ''
        right = ''
        element = ''

        if self._in:
            in_elements = ''.join([str(item() if callable(item) else item) for item in self._in])
            element = '<%s%s>%s</%s>' % (self._name, self.renderAttributes(), in_elements, self._name)
        else:
            element = '<%s%s/>' % (self._name, self.renderAttributes())

        if self._left:
            left = ''.join(map(lambda item: str(item() if callable(item) else item), self._left))

        if self._right:
            right = ''.join(map(lambda item: str(item() if callable(item) else item), self._right))

        return  left + element + right

class htmlHelper(object):
    """ Tag generation factory """
    def __getattr__(self, tag):
        """ This method only gets called for attributes (ie. tags in this application) that don't exist yet. """
        if not self.__dict__.has_key(tag):
            self.__dict__[tag] = type(tag, (TAG,), {})
        return deepcopy(self.__dict__[tag])

def table(*args, **kw):
    global helper
    """ 
    This function presents the idea of extending tags for simpler generation of some
    html element groups. Table has several group of tags in well defined structure. Caption
    header should be right after table and before thead. Colgroup, tfoot, tbody, tr, td and th 
    elements has certain order which are handled by extended table class returned by this function.
    
    Same idea could be used to create unordered lists and menu or other custom html widgets.
    
    Use in this way:
    from tagpy import helper as h, table
    """
    class table(type(helper.table())):
        """ Extend base table tag class """
        def __init__(self, *args, **kw):
            super(self.__class__, self).__init__(*args, **kw)
        
        def addCaption(self, caption, **kw):
            if not self.__dict__.has_key('caption'):
                self.caption = helper.caption(**kw)
            self.caption.content(caption)
            return self
        
        def addColGroup(self, *cols, **kw):
            """
            http://www.w3.org/TR/CSS2/tables.html#columns
            """
            if not self.__dict__.has_key('colgroup'):
                self.colgroup = helper.colgroup(**kw)
            for col in cols:
                self.colgroup.content(col)
            return self
        
        def addHeadRow(self, *trs, **kw):
            if not self.__dict__.has_key('thead'):
                self.thead = helper.thead(**kw)
            for tr in trs:
                self.thead.content(tr)
            return self
        
        def addFootRow(self, *trs, **kw):
            if not self.__dict__.has_key('tfoot'):
                self.tfoot = helper.tfoot(**kw)
            for tr in trs:
                self.tfoot.content(tr)
            return self
        
        def addBodyRow(self, *trs, **kw):
            if not self.__dict__.has_key('tbody'):
                self.tbody = helper.tbody(**kw)
            for tr in trs:
                self.tbody.content(tr)
            return self
        
        def addBodyRows(self, *trs, **kw):
            if not self.__dict__.has_key('tbodys'):
                self.tbodys = []
            self.tbodys.append(helper.tbody(*trs, **kw))
            return self
        
        def __str__(self):
            self._in = []
            if self.__dict__.has_key('caption'):
                self.content(self.caption)
            if self.__dict__.has_key('colgroup'):
                self.content(self.colgroup)
            if self.__dict__.has_key('thead'):
                self.content(self.thead)
            if self.__dict__.has_key('tfoot'):
                self.content(self.tfoot)
            if self.__dict__.has_key('tbody'):
                self.content(self.tbody)
            if self.__dict__.has_key('tbodys'):
                map(self.content, self.tbodys)
            return super(self.__class__, self).__str__()
    
    return table(*args, **kw)

#
"""
All tag elements are accessible via readily constructed factory variable. This helper
should be imported from the module in this wise: from tagpy import helper
OR from tagpy import helper as h if shorter variable name is preferred
"""
helper = htmlHelper()