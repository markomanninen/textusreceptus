#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: svg.py

from . main import helper
from math import pi, sin, cos

def svg(*args, **kw):
    """
    Use in this way:
    
    ´from remarkuple import helper as h, svg´
    
    """
    class svg(type(helper.svg())):
        
        def __init__(self, *args, **kw):
            super(self.__class__, self).__init__(*args, **kw)
            # cartesian grid on/off
            self.__dict__['grid'] = False
            # axes on/off
            self.__dict__['axes'] = False
            # show origin
            self.__dict__['origin'] = False
            # grid aspects
            self.__dict__['grid_aspects'] = (4, 8)
            # x
            self.__dict__['x'] = 200
            # y
            self.__dict__['y'] = 200
            # elements
            self.__dict__['elements'] = []
            # size of the svg canvas, width and height
            self.__dict__['size'] = (100, 100)
            # grid id
            self.__dict__['grid_id'] = "gid%s" % id(self)
            # grid item id
            self.__dict__['grid_item_id'] = "gitem%s" % id(self)
            # grid width
            width = kw['width'] if kw.has_key('width') else self.__dict__['x']*2
            # grid height
            height = kw['height'] if kw.has_key('height') else self.__dict__['y']*2
            self.set_size(width, height)
        
        def set_grid(self, grid = True):
            self.__dict__['grid'] = grid
            return self
        
        def set_axes(self, axes = True):
            self.__dict__['axes'] = axes
            return self
        
        def set_origin(self, origin = True):
            self.__dict__['origin'] = origin
            return self
        
        def set_size(self, width, height):
            self.__dict__['x'] = width/2
            self.__dict__['y'] = height/2
            self.__dict__['size'] = (width, height)
            self.width = width
            self.height = height
            self.viewbox = "0 0 %s %s" % (width+1, height+1)
            return self
        
        def set_text(self, *args, **kw):
            kw['x'] = self.__dict__['x']+kw['x'] if kw.has_key('x') else self.__dict__['x'] 
            kw['y'] = self.__dict__['y']-kw['y'] if kw.has_key('y') else self.__dict__['y']
            self.__dict__['elements'].append(helper.text(*args, **kw))
            return self
        
        def set_rectangle(self, *args, **kw):
            kw['x'] = self.__dict__['x']+kw['x'] if kw.has_key('x') else self.__dict__['x']
            kw['y'] = self.__dict__['y']-kw['y'] if kw.has_key('y') else self.__dict__['y']
            self.__dict__['elements'].append(helper.rect(*args, **kw))
            return self
        
        def set_group(self, *args, **kw):
            self.__dict__['elements'].append(helper.g(*args, **kw))
            return self
        
        def set_defs(self, *args, **kw):
            self.__dict__['elements'].append(helper.defs(*args, **kw))
            return self
        
        def set_line(self, *args, **kw):
            kw['x1'] = self.__dict__['x']+kw['x1'] if kw.has_key('x1') else self.__dict__['x']
            kw['y1'] = self.__dict__['y']-kw['y1'] if kw.has_key('y1') else self.__dict__['y']
            kw['x2'] = self.__dict__['x']+kw['x2'] if kw.has_key('x2') else self.__dict__['x'] + 10
            kw['y2'] = self.__dict__['y']-kw['y2'] if kw.has_key('y2') else self.__dict__['y'] + 10
            self.__dict__['elements'].append(helper.line(*args, **kw))
            return self
        
        def set_circle(self, *args, **kw):
            kw['cx'] = self.__dict__['x']+kw['cx'] if kw.has_key('cx') else self.__dict__['x']
            kw['cy'] = self.__dict__['y']-kw['cy'] if kw.has_key('cy') else self.__dict__['y']
            self.__dict__['elements'].append(helper.circle(*args, **kw))
            return self
        
        def set_triangle(self, *args, **kw):
            kw['sides'] = 3
            return self.set_regular_polygon(*args, **kw)
        
        def set_square(self, *args, **kw):
            kw['sides'] = 4
            return self.set_regular_polygon(*args, **kw)
        
        def set_pentagon(self, *args, **kw):
            kw['sides'] = 5
            return self.set_regular_polygon(*args, **kw)
        
        def set_hexagon(self, *args, **kw):
            kw['sides'] = 6
            return self.set_regular_polygon(*args, **kw)
        
        def set_regular_polygon(self, *args, **kw):
            # set default properties for vertex
            kw['cx'] = kw['cx']+self.__dict__['x'] if kw.has_key('cx') else self.__dict__['x']
            kw['cy'] = kw['cy']-self.__dict__['y'] if kw.has_key('cy') else self.__dict__['y']
            kw['radius'] = kw['radius'] if kw.has_key('radius') else 1
            kw['sides'] = kw['sides'] if kw.has_key('sides') else 4
            kw['degrees'] = kw['degrees'] if kw.has_key('degrees') else 0
            # set generate polygon points
            points = self.polygon_points(self.vertex(cx=kw['cx'],
                                                     cy=kw['cy'],
                                                     radius=kw['radius'],
                                                     sides=kw['sides'],
                                                     degrees=kw['degrees']))
            # delete default properties
            del kw['cx']
            del kw['cy']
            del kw['radius']
            del kw['sides']
            del kw['degrees']
            # create polygon with given points and keywords
            self.__dict__['elements'].append(helper.polygon(points=points, *args, **kw))
            return self
        
        def polygon_points(self, vertex):
            return ' '.join(['%s,%s' % (point[0], point[1]) for point in vertex])
        
        def vertex(self, cx = 0, cy = 0, sides = 4, radius = 1, degrees = 0):
            centerAng = 2*pi/sides
            startAng = pi*degrees/180
            points = []
            for i in range(0, sides):
                ang = startAng + (i*centerAng);
                x = round(cx + radius*cos(ang), 2)
                y = round(cy - radius*sin(ang), 2)
                points.append([x,y])
            return points
        
        def _set_grid(self):
            """ Set up background grid for drawing canvas """
            grid_sizex = self.__dict__['size'][0]/self.__dict__['grid_aspects'][0]
            grid_sizey = self.__dict__['size'][1]/self.__dict__['grid_aspects'][0]
            
            sizex = grid_sizex*(1.0/self.__dict__['grid_aspects'][1])
            sizey = grid_sizey*(1.0/self.__dict__['grid_aspects'][1])
            
            defs = helper.defs()
            defs += helper.pattern(helper.path(**{'d': 'M %s 0 L 0 0 0 %s' % (sizex, sizey), 'fill': 'none', 'stroke': 'gray', 'stroke-width': 0.5}),
                                   **{'id': self.__dict__['grid_item_id'], 'width': sizex, 'height': sizey, 'patternUnits': 'userSpaceOnUse'})
            defs += helper.pattern(helper.path(**{'d': 'M %s 0 L 0 0 0 %s' % (grid_sizex, grid_sizey), 'fill': 'none', 'stroke': 'gray', 'stroke-width': 1}),
                                   helper.rect(width=grid_sizex, height=grid_sizey, fill="url(#%s)" % self.__dict__['grid_item_id']),
                                   **{'id': self.__dict__['grid_id'], 'width': grid_sizex, 'height': grid_sizey, 'patternUnits': 'userSpaceOnUse'})
            self += defs
            self += helper.rect(fill="white", height=self.__dict__['size'][0]+1, width=self.__dict__['size'][1]+1)
            self += helper.rect(fill="url(#%s)" % self.__dict__['grid_id'], height=self.__dict__['size'][0]+1, width=self.__dict__['size'][1]+1)
            
        def _set_axes(self):
            """ Set up x and y axis for drawing canvas """
            self += helper.line(stroke="black", x1=self.__dict__['x'], x2=self.__dict__['x'], y1=0, y2=self.__dict__['y']*2)
            self += helper.line(stroke="black", x1=0, x2=self.__dict__['x']*2, y1=self.__dict__['y'], y2=self.__dict__['y'])
        
        def _set_origin(self):
            """ Set up origin dot and x/y coordinates for drawing canvas """
            self += helper.circle(cx=self.__dict__['x'], cy=self.__dict__['y'], r=2, fill="black", stroke="black", style="fill-opacity: 50%")
            self += helper.text("(0,0)", x=self.__dict__['x']+5, y=self.__dict__['y']-5, style="fill-opacity: 50%")
        
        def __str__(self):
            if self.__dict__['grid']:
                self._set_grid()
            if self.__dict__['axes']:
                self._set_axes()
            if self.__dict__['origin']:
                self._set_origin()
            if self.__dict__['elements']:
                for element in self.__dict__['elements']:
                    self += element
            return super(self.__class__, self).__str__()
    
    return svg(*args, **kw)