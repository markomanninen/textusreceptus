#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: table.py

from . main import helper

def table(*args, **kw):
    """
    Table function presents the idea of extending tags for simpler generation of some
    html element groups. Table has several group of tags in well defined structure. Caption
    header should be right after table and before thead for example. Colgroup, tfoot, tbody, tr, td and
    th elements has certain order which are handled by extended table class.
    
    Same idea could be used to create unordered lists and menu or other custom html widgets.
    
    Use in this way:
    
    ´from remarkuple import helper as h, table´
    
    """
    class table(type(helper.table())):
        """ Extend base table tag class """
        def __init__(self, *args, **kw):
            super(self.__class__, self).__init__(*args, **kw)
        
        def addCaption(self, caption, **kw):
            if not self.__dict__.has_key('caption'):
                self.__dict__['caption'] = helper.caption(**kw)
            self.__dict__['caption'].addContent(caption)
            return self
        
        def addColGroup(self, *cols, **kw):
            """
            http://www.w3.org/TR/CSS2/tables.html#columns
            """
            if not self.__dict__.has_key('colgroup'):
                self.__dict__['colgroup'] = helper.colgroup(**kw)
            for col in cols:
                self.__dict__['colgroup'].addContent(col)
            return self
        
        def addHeadRow(self, *trs, **kw):
            if not self.__dict__.has_key('thead'):
                self.__dict__['thead'] = helper.thead(**kw)
            for tr in trs:
                self.__dict__['thead'].addContent(tr)
            return self
        
        def addFootRow(self, *trs, **kw):
            if not self.__dict__.has_key('tfoot'):
                self.__dict__['tfoot'] = helper.tfoot(**kw)
            for tr in trs:
                self.__dict__['tfoot'].addContent(tr)
            return self
        
        def addBodyRow(self, *trs, **kw):
            """ Body rows can be collected under same element, or under separate body tags via addBodyRows """
            if not self.__dict__.has_key('tbody'):
                self.__dict__['tbody'] = helper.tbody(**kw)
            for tr in trs:
                self.__dict__['tbody'].addContent(tr)
            return self
        
        def addBodyRows(self, *trs, **kw):
            """ See above """
            if not self.__dict__.has_key('tbodys'):
                self.__dict__['tbodys'] = []
            self.__dict__['tbodys'].append(helper.tbody(*trs, **kw))
            return self
        
        def __str__(self):
            if self.__dict__.has_key('caption'):
                self.addContent(self.__dict__['caption'])
            if self.__dict__.has_key('colgroup'):
                self.addContent(self.__dict__['colgroup'])
            if self.__dict__.has_key('thead'):
                self.addContent(self.__dict__['thead'])
            if self.__dict__.has_key('tfoot'):
                self.addContent(self.__dict__['tfoot'])
            if self.__dict__.has_key('tbody'):
                self.addContent(self.__dict__['tbody'])
            if self.__dict__.has_key('tbodys'):
                map(self.addContent, self.__dict__['tbodys'])
            return super(self.__class__, self).__str__()
    
    return table(*args, **kw)