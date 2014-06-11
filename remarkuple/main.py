#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

RESERVED_TAG_METHODS = ["setAttribute", "getAttribute", "addContent"]

class TAGAttributeError(Exception):
    pass

class TAG(object):
    """ 
    XML/HTML tag generation factory/helper
    
    Import module:
    
    from remarkuple import helper as h, concat
    
    Create tag by dot notation or create method:
    
    a = h.a()
    b = h.create('b')
    
    Attach attribute by dot notation or setter:
    
    a.href = "#"
    b.setAttribute("class", "extra-bold")
    
    Retrieve attribute by dot notation or getter:
    
    print a.href, b.getAttribute("class") -> # extra-bold
    
    Add content with plus notation or setter:
    
    a += h.span("text")
    b.addContent("text")
    
    Get XML/HTML:
    
    print a, b -> <a href="#"><span>text</span></a> <b class="extra-bold">text</b>
    
    """
    def __init__(self, *args, **kw):
        """ Args as inner html content, kw as tag attributes. Attributes names/keys are all transformed to lower letters! """
        self.__dict__['content'] = []
        self.__dict__['attributes'] = {}
        for arg in args:
            self.__dict__['content'].append(arg)
        for key, val in kw.iteritems():
            self.__dict__['attributes'][key.lower()] = val
    
    def getAttribute(self, key):
        """ Get attribute by key in case-sensitive manner. Returning None if attribute is not found. """
        return self.__dict__['attributes'].get(key, None)
    def __getattr__(self, key):
        """ 
        Get attribute by key by dot notation: tag.attr. This is a short and nice way, but
        drawback is that python has some reserved words, that can't be used this way. Method is also
        not-case-sensitive, because key is transformed to lower letters. Returning None if attribute is not found. 
        """
        return self.__dict__['attributes'].get(key.lower(), None)
    
    def setAttribute(self, key, val):
        """ Set attribute by key and value in case-sensitive manner. Returning self object for chaining methods. """
        self.__dict__['attributes'][key] = val
        return self
    def __setattr__(self, key, val):
        """ 
        Set attribute by key by dot notation: tag.attr = "value". This is a short and nice way, but
        drawback is that python has some reserved words, that can't be used this way. Method is also
        not-case-sensitive, because key is transformed to lower letters. 
        """
        if key not in RESERVED_TAG_METHODS:
            self.__dict__['attributes'][key.lower()] = val
        else:
            raise TAGAttributeError('Cannot use %s.%s="%s" notation due to conflicting attributes with builtin tag method names. Use %s.setAttribute("%s", "%s") instead.' % 
                                    (self.__class__.__name__, key, val, self.__class__.__name__, key, val))
        
    
    def addContent(self, item):
        """ Add content / inner HTML to tag. Item can be anything from other tag objects to string and numerical values. Returning self object."""
        return self.__iadd__(item)
    def __iadd__(self, item):
        """ Plus notation for adding content for tag: tag1 += tag2. """
        self.__dict__['content'].append(item)
        return self
    
    def __getitem__(self, i):
        """ You can iterate thru tag content: for content in tag ... """
        return self.__dict__['content'][i]
    
    def _repr_html_(self):
        """ Makes possible to render html in IPython notebook environment rather than representing tag in string format """
        return self.__str__()
    def __str__(self):
        """ Represent tag in string format """
        if self.__dict__['content']:
            return '<%s%s>%s</%s>' % (self.__class__.__name__, strattr(self.__dict__['attributes']),
                                      concat(*self.__dict__['content']), self.__class__.__name__)
        else:
            return '<%s%s/>' % (self.__class__.__name__, strattr(self.__dict__['attributes']))

class htmlHelper(object):
    def create(self, tag):
        return type(tag, (TAG,), {})()
    def __getattr__(self, tag):
        return type(tag.lower(), (TAG,), {})
    
def concat(*args):
    return ''.join(map(lambda x: str(x()) if callable(x) else str(x), args))

def strattr(attributes):
    return ''.join([' %s="%s"' % (k, v) for k, v in attributes.iteritems()])

helper = htmlHelper()