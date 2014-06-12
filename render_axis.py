#!/usr/bin/env python
'''
Copyright (C) 2014 Nicola Romano', romano.nicola@gmail.com

version 0.1
 0.1: first working version - produces horizontal and vertical axes

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
'''

import inkex, simplestyle, simpletransform
import sys

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
	
	inkex.etree.SubElement(parent, inkex.addNS('path','svg'), attribs)

def draw_SVG_text(x, y, text, size, parent, style, angle=0):
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


def draw_axis(x_pos, y_pos, width, height, axis_from, axis_to, num_ticks, sub_ticks, decimals, text, direction, grp):
	# Length of ticks
	ticklength = 5
	subticklength = 3

	# Text styles (TODO: make them user-defined)
	font_axis_ticks = {
		'font-size' : '10px',
		'fill' : '#000000',
		'font-family' : 'Arial',
		'text-align' : "center",
		'text-anchor' : "middle"
		}
		
	font_axis_title = {
		'font-size' : "15px",
		'fill' : '#000000',
		'font-family' : "Arial",
		'text-align' : "center",
		'text-anchor' : "middle"
		}
	
	if direction == "vertical":
		font_axis_ticks['text-align'] = "end"
		font_axis_ticks['text-anchor'] = "end"

	# The relative amount per tick
	# e.g. we're going from 0 to 8 and have 5 ticks
	# each tick will be 2, so we have 0, 2, 4, 6, 8
	tickamount = (axis_to - axis_from)/(num_ticks-1)

	if direction=="horizontal":
		# TODO: add offset option
		# TODO: allow axis position on other sides of the bbox
		# Align to bounding box
		x1 = x_pos
		x2 = x_pos + width
		y1 = y2 = y_pos

		draw_SVG_line(x1, y1, x2, y2, "myaxis", grp)
		i = 0
		tickspace = float(x2-x1)/float(num_ticks-1)
		subtickspace = tickspace/float(sub_ticks+1)
		# Draw the ticks
		for i in range(num_ticks):
			ticktxt = ('%0.'+str(decimals)+'f') % (i*tickamount + axis_from)
			# Draw main ticks
			draw_SVG_line(i*tickspace+x1, y1, i*tickspace+x1, y1+ticklength, 
				"myaxis_tick"+str(i), grp)
			# Draw minor ticks
			if i<(num_ticks-1): # Do not put minor ticks after the last major one!
				for j in range(1, sub_ticks+1):
					draw_SVG_line(i*tickspace+x1+j*subtickspace, y1, i*tickspace+x1+j*subtickspace, 
						y1+subticklength, "myaxis_subtick"+str(i), grp)
			# Draw text associated to main ticks
			draw_SVG_text(i*tickspace+x1, y1+ticklength+10, ticktxt, "10px", grp, font_axis_ticks)
			
		# Draw the title
		draw_SVG_text((x1+x2)/2, y1+ticklength+30, text, "12px", grp, font_axis_title)
	else: # Vertical axis
			# Align to bounding box
		y1 = y_pos
		y2 = y_pos - height
		x1 = x2 = x_pos

		draw_SVG_line(x1, y1, x2, y2, "myaxis", grp)
		i = 0
		tickspace = float(y2-y1)/float(num_ticks-1)

		for i in range(num_ticks):
			ticktxt = ('%0.'+str(decimals)+'f') % (i*tickamount + axis_from)
			draw_SVG_line(x1, i*tickspace+y1, x1-ticklength, i*tickspace+y1, 
				"myaxis_tick"+str(i), grp)
			# Draw text associated to main ticks
			draw_SVG_text(x1-ticklength-5, i*tickspace+y1+2.5, ticktxt, "10px", grp, font_axis_ticks)

		# Draw the title
		draw_SVG_text(x1-ticklength-30, (y1+y2)/2, text, "12px", grp, font_axis_title, -90)

class RenderAxis(inkex.Effect):
	""" Constructor.
	Defines "--what" option of a script."""
	def __init__(self):
		# Call base class construtor.
		inkex.Effect.__init__(self)
		# Option parser:
		# -f, --axis_from
		# -t, --axis_to
		# -N, --num_ticks
		# -n, --sub_ticks
		# -p, --decimals (precision)
		# -T, --axis_title
		# -d, --direction
		# -b, --tab
		self.OptionParser.add_option("-f", "--axis_from",
						action="store", type="float",
						dest="axis_from", default=0,
						help="Axis starting value")
		self.OptionParser.add_option("-t", "--axis_to",
						action="store", type="float",
						dest="axis_to", default=10,
						help="Axis ending value")
		self.OptionParser.add_option("-n", "--num_ticks",
						action="store", type="int",
						dest="num_ticks", default=5,
						help="Number of ticks")
		self.OptionParser.add_option("-N", "--sub_ticks",
						action="store", type="int",
						dest="sub_ticks", default=0,
						help="Number of sub-ticks")
		self.OptionParser.add_option("-p", "--decimals",
						action="store", type="int",
						dest="decimals", default=1,
						help="Number of ticks")
		self.OptionParser.add_option("-T", "--axis_title",
						action="store", type="string",
						dest="text", default='',
						help="Title of the axis")
		self.OptionParser.add_option("-d", "--direction",
						action="store", type="string",
						dest="direction", default='',
						help="Direction of the axis")
		self.OptionParser.add_option("-b", "--tab",
						action="store", type="string",
						dest="tab", default='',
						help="The tab of the interface")

	def effect(self):
		if len(self.options.ids) == 0:
			inkex.errormsg("Please select an object.")
			exit()
			
		# Collect document ids
		doc_ids = {}
		docIdNodes = self.document.xpath('//@id')
		for m in docIdNodes:
			doc_ids[m] = 1

		grpname = 'axis'
		# Make sure that the id/name is inique
		index = 0
		while (doc_ids.has_key(grpname)):
			grpname = 'axis' + str(index)
			index = index + 1

		grp_name = grpname
		grp_attribs = {inkex.addNS('label','inkscape'):grp_name}
		# The group to put everything in
		grp = inkex.etree.SubElement(self.current_layer, 'g', grp_attribs)
		
		# Get the bounding box
		bbox = simpletransform.computeBBox(self.selected.values())
		width = int(bbox[1] - bbox[0])
		height = int(bbox[3] - bbox[2])
		x_pos = bbox[0]
		y_pos = bbox[3]

		draw_axis(x_pos, y_pos, width, height, 
				self.options.axis_from, self.options.axis_to, 
				self.options.num_ticks, self.options.sub_ticks, 
				self.options.decimals, self.options.text, 
				self.options.direction, grp)

e = RenderAxis()
e.affect()
