# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:15:22 2017

@author: JanHelge
"""
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, LabelSet
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.layouts import gridplot
from bokeh.palettes import viridis, Category20
from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.io import show, output_file


def plot_maaned(df, vegref):
    gruppe = df.groupby('Maaned')
    count = gruppe.count()
    values = (count['SkredID'].tolist())
    keys = (count.index.tolist())
    madict = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, 'Ingen data': 0}
    ma = dict(zip(keys, values))
    print(ma)

    z = {**madict, **ma}

    maaneder = list(z.keys())
    antall_maaned = list(z.values())
    source = ColumnDataSource(data=dict(
    x=maaneder,
    y=antall_maaned,
    ))
    p = figure(x_range=maaneder, plot_height=500, title="Skred per månad for strekning " + vegref,
               toolbar_location="above", tools="save")
    labels = LabelSet(x='Maaned', y='SkredID_count', text='SkredID_count', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    
    p.vbar(x='x', top='y', width=0.9, source=source)
    p.xaxis.major_label_orientation = 1.2
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.add_layout(labels)
    p.add_tools(HoverTool(tooltips=[("Antall", '@y')]))
    return p

show(plot_maaned())