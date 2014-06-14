#!/usr/bin/env python
'''
Copyright (C) 2014 Nicola Romano', romano.nicola@gmail.com

version 0.1
	0.1: first version. Functions for drawing lines and text

Known bugs
	When creating a vertical axis the title is inconsistently positioned in the x direction

------------------------------------------------------------------------
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
------------------------------------------------------------------------

'''

import inkex, simpletransform, simplestyle

def draw_SVG_line(x1, y1, x2, y2, name, parent):
	style = {
		'fill' : 'none',
		'stroke' : '#000000',
		'stroke-width' : '1px',
		'stroke-linecap' : 'round',
		'stroke-opacity' : '1'
		}
	attribs = {
		'style' : simplestyle.formatStyle(style),
		inkex.addNS('label','inkscape') : name,
		'd' : 'M'+str(x1)+' '+str(y1)+'L'+str(x2)+' '+str(y2)
		}
	
	line = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), attribs)
	return line

def draw_SVG_text(x, y, text, parent, style, angle=0):
	attribs = {
		'style' : simplestyle.formatStyle(style),
		'x' : str(x),
		'y' : str(y)
		}

	# Generate text
	txt = inkex.etree.SubElement(parent, inkex.addNS('text'), attribs)
	txt.text = text
	# Rotate (if needed)
	# We need to rotate around the text center.
	# To achieve this we move it to the origin, rotate it and then translate it back
	rotmatrix = simpletransform.parseTransform('translate('+str(x)+','+str(y)+')'+
										' rotate('+str(angle)+')'+
										' translate('+str(-x)+','+str(-y)+')')
	simpletransform.applyTransformToNode(rotmatrix, txt)
	return txt


