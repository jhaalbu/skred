# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:09:56 2017

@author: JanHelge
"""

import bokeh.plotting as bk
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import brewer
from numpy import pi

# define starts/ends for wedges from percentages of a circle
percents = [0, 0.14, 0.22, 0.40, 0.83, 0.99, 1.0]
category = ['Extreme ', 'High ', 'Light ', 'Medium ', 'Not Classified', 'Very Light ']
starts = [p*2*pi for p in percents[:-1]]
ends = [p*2*pi for p in percents[1:]]

# a color for each pie piece
colors = brewer['Spectral'][len(percents)]

# create source
source = ColumnDataSource(
    data=dict(
        x=[0 for x in percents],
        y=[0 for x in percents],
        ymin = [0.5 for x in percents],
        ymax = [1 for x in percents],
        percents=percents,
        category= category,
        starts=starts,
        colors=colors,
        ends=ends,
    )
)

# create chart
TOOLS = "hover"
p = bk.figure(title='Chronic',title_text_font ='Roboto', title_text_font_size ='14pt', title_text_alpha =0.7,
              x_range=(-1.1,1.1), y_range=(-1.1,1.1), width=250, height=250, tools=TOOLS)

p.annular_wedge(x='x', y='y',  inner_radius='ymin', outer_radius='ymax', direction="anticlock",
                start_angle='starts', end_angle='ends', color='colors', source=source)

hover = p.select(dict(type=HoverTool))
hover.tooltips = [
    ('category', '@category'),
    ('percents','@percents')
]

# displays
bk.show(p)

