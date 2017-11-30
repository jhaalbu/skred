from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.layouts import gridplot


def plotSkredtype(df):
    gruppe = df.groupby('Skredtype')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=350, x_range=gruppe, title="Antall skred per skredtype",
           toolbar_location="above", tools="save")

    p.vbar(x='Skredtype', top='SkredID_count', width=0.9, source=source)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Type skred"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def plotMaaned(df):
    gruppe = df.groupby('Maaned')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=350, x_range=gruppe, title="Antall skred per måned",
           toolbar_location="above", tools="")

    p.vbar(x='Maaned', top='SkredID_count', width=0.9, source=source)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Måned"
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def plotLosneOmrade(df):
    gruppe = df.groupby('Løsneområde')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=350, x_range=gruppe, title="Antall skred per løsneområde",
           toolbar_location="above", tools="save")

    p.vbar(x='Løsneområde', top='SkredID_count', width=0.9, source=source)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Løsneområde"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p


def steinMaaned(df):
    seg_df = df.query('Skredtype == "Stein"')
    seg_gruppe = seg_df.groupby('Maaned')
    source = ColumnDataSource(seg_gruppe)

    p = figure(plot_height=350, x_range=seg_gruppe, title="Antall steinskred per måned",
               toolbar_location='above', tools="save")

    p.vbar(x='Maaned', top='SkredID_count', width=0.9, source=source)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Måned"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def snoMaaned(df):
    seg_df = df.query('Skredtype == "Snø"')
    seg_gruppe = seg_df.groupby('Maaned')
    source = ColumnDataSource(seg_gruppe)

    p = figure(plot_height=350, x_range=seg_gruppe, title="Antall snøskred per måned",
               toolbar_location='above', tools="save")

    p.vbar(x='Maaned', top='SkredID_count', width=0.9, source=source)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Måned"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def flomMaaned(df):
    seg_df = df.query('Skredtype == "Flomskred (vann+stein+jord)"')
    seg_gruppe = seg_df.groupby('Maaned')
    source = ColumnDataSource(seg_gruppe)

    p = figure(plot_height=350, x_range=seg_gruppe, title="Antall flomskred per måned",
               toolbar_location='above', tools="save")

    p.vbar(x='Maaned', top='SkredID_count', width=0.9, source=source)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Måned"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p



'''
df = pd.DataFrame(liste)
gruppe = df.groupby('Skredtype')
gruppemaaned = df.groupby('Maaned')
gruppetype = df.groupby('Løsneområde')

source = ColumnDataSource(gruppe)
source_maaned = ColumnDataSource(gruppemaaned)
source_type = ColumnDataSource(gruppetype)

p = figure(plot_height=350, x_range=gruppe, title="Skred",
           toolbar_location=None, tools="")

p.vbar(x='Skredtype', top='SkredID_count', width=1, source=source)

p.y_range.start = 0
p.xgrid.grid_line_color = None
p.xaxis.axis_label = "Type skred"
p.xaxis.major_label_orientation = 1.2
p.outline_line_color = None

show(p)

pm = figure(plot_height=350, x_range=gruppemaaned, title="Skred",
           toolbar_location=None, tools="")

pm.vbar(x='Maaned', top='SkredID_count', width=1, source=source_maaned)

pm.y_range.start = 0
pm.xgrid.grid_line_color = None
pm.xaxis.axis_label = "Måned"
pm.xaxis.major_label_orientation = 1.2
pm.x_range.range_padding = 0.1
pm.outline_line_color = None

show(pm)

ptype = figure(plot_height=350, x_range=gruppetype, title="Skred",
           toolbar_location=None, tools="")

ptype.vbar(x='Løsneområde', top='SkredID_count', width=1, source=source_type)

ptype.y_range.start = 0
ptype.xgrid.grid_line_color = None
ptype.xaxis.axis_label = "Type løsneområde"
ptype.yaxis.axis_label = "Antall skred"
ptype.xaxis.major_label_orientation = 1.2
ptype.outline_line_color = None

show(ptype)

print(gruppe.describe())
print(gruppemaaned.describe())
'''