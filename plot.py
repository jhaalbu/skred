from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, LabelSet
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.layouts import gridplot
from bokeh.palettes import viridis, Category20
from bokeh.transform import factor_cmap

def plot_steinmaaned(df, vegref):
    skred = df.query('Skredtype == "Stein"')
    gruppe = skred.groupby('Maaned')
    count = gruppe.count()
    values = (count['Dag'].tolist())
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
    p = figure(x_range=maaneder, plot_height=500, plot_width=800, title="Steinskred per månad for " + vegref,
               toolbar_location="above", tools="save")
    labels = LabelSet(x='x', y='y', text='y', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    p.vbar(x='x', top='y', width=0.9, source=source)
    p.xaxis.major_label_orientation = 1.2
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Måned"
    p.y_range.start = 0
    p.add_layout(labels)
    #p.add_tools(HoverTool(tooltips=[("Antall", '@y')]))
    return p

def plot_snomaaned(df, vegref):
    skred = df.query('Skredtype == "Snø"')
    gruppe = skred.groupby('Maaned')
    count = gruppe.count()
    values = (count['Dag'].tolist())
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
    p = figure(x_range=maaneder, plot_height=500, plot_width=800, title="Snøskred per månad for " + vegref,
               toolbar_location="above", tools="save")
    labels = LabelSet(x='x', y='y', text='y', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    p.vbar(x='x', top='y', width=0.9, source=source)
    p.xaxis.major_label_orientation = 1.2
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Måned"
    p.y_range.start = 0
    p.add_layout(labels)
    p.add_tools(HoverTool(tooltips=[("Antall", '@y')]))
    return p

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
    p = figure(x_range=maaneder, plot_height=500, plot_width=800, title="Skred per månad for strekning " + vegref,
               toolbar_location="above", tools="save")
    labels = LabelSet(x='x', y='y', text='y', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    
    p.vbar(x='x', top='y', width=0.9, source=source)
    p.xaxis.major_label_orientation = 1.2
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Maaned"
    p.y_range.start = 0
    p.add_layout(labels)
    p.add_tools(HoverTool(tooltips=[("Antall", '@y')]))
    return p

def plot_skredtype(df, vegref):
    gruppe = df.groupby('Skredtype')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=500, plot_width=800, x_range=gruppe, title="Antall skred per skredtype for " + vegref,
           toolbar_location="above", tools="save")

    p.vbar(x='Skredtype', top='SkredID_count', width=0.9, source=source)
    labels = LabelSet(x='Skredtype', y='SkredID_count', text='SkredID_count', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    p.add_layout(labels)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Type skred"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def plot_aar(df, vegref):
    gruppe = df.groupby('År')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=500, plot_width=800, x_range=gruppe, title="Antall skred per år for " + vegref,
           toolbar_location="above", tools="save")

    p.vbar(x='År', top='SkredID_count', width=0.9, source=source)
    labels = LabelSet(x='År', y='SkredID_count', text='SkredID_count', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    p.add_layout(labels)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Årstall"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def plot_losneomrade(df, vegref):
    gruppe = df.groupby('Løsneområde')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=500, plot_width=800, x_range=gruppe, title="Antall skred per løsneområde for " + vegref,
           toolbar_location="above", tools="save")

    p.vbar(x='Løsneområde', top='SkredID_count', width=0.9, source=source)
    labels = LabelSet(x='Løsneområde', y='SkredID_count', text='SkredID_count', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    p.add_layout(labels)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Løsneområde"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def plot_steinlosneomrade(df, vegref):
    skred = df.query('Skredtype == "Stein"')
    gruppe = skred.groupby('Løsneområde')
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=500, plot_width=800, x_range=gruppe, title="Antall steinskred per løsneområde for " + vegref,
           toolbar_location="above", tools="save")

    p.vbar(x='Løsneområde', top='SkredID_count', width=0.9, source=source)
    labels = LabelSet(x='Løsneområde', y='SkredID_count', text='SkredID_count', level='glyph',
        x_offset=-8, y_offset=0, source=source, render_mode='canvas')
    p.add_layout(labels)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Løsneområde"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p

def plot_volumomraade(df, vegref):
    gruppe = df.groupby(('Løsneområde', 'Volum'))
    source = ColumnDataSource(gruppe)
    p = figure(plot_height=500, plot_width=800, x_range=gruppe, title="Antall skred per volum, sortert på løsneområde for " + vegref,
           toolbar_location="above", tools="save")

    p.vbar(x='Løsneområde_Volum', top='SkredID_count', width=0.9, source=source)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = "Antall skred"
    p.xaxis.axis_label = "Type skred"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None

    return p





