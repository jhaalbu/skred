import data
import plot
from flask import Flask, request, render_template
from wtforms import Form, IntegerField, StringField, validators
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8



app = Flask(__name__)

class InputForm(Form):
    veg = StringField(label='Veg (f.eks fv60)', validators=[validators.InputRequired()])
    fylke = IntegerField(label='Fylke (f.eks 14)')
    hpfra = IntegerField(label='HP fra (f.eks 1)', default=1)
    mfra = IntegerField(label='meter fra (f.eks 0)', default=0)
    hptil = IntegerField(label='HP til (f.eks 20)', default=20)
    mtil = IntegerField(label='meter til (f.eks 50000)', default=50000)

@app.route('/', methods=['GET', 'POST'])
def index():

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        veg, fylke, hpfra, hptil, mfra, mtil = form.veg.data, form.fylke.data, form.hpfra.data, form.hptil.data, form.mfra.data, form.mtil.data
        viseside = True
    else:
        viseside = False
        veg = 'fv241'
        fylke = '14'
        hpfra = 1
        hptil = 10
        mfra = 0
        mtil = 10000

    if hpfra == hptil:
        vegref = str(fylke) + '00' + veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + str(mtil)
    else:
        vegref = str(fylke) + '00' + veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + 'hp' + str(hptil) + 'm' + str(mtil)

    df = data.hentData(vegref)
    fig_skredtype = plot.plot_skredtype(df, vegref)
    fig_maaned = plot.plot_maaned(df, vegref)
    fig_losneområde = plot.plot_losneomrade(df, vegref)
    fig_steinmaaned = plot.plot_steinmaaned(df, vegref)
    fig_snomaaned = plot.plot_snomaaned(df, vegref)
    #fig_steinm = plot.plot_steinmaaned(df, vegref)
    fig_aar = plot.plot_aar(df, vegref)
    fig_volumomraade = plot.plot_volumomraade(df, vegref)
    fig_steinlosneomrade = plot.plot_steinlosneomrade(df, vegref)

    #grid_oversikt = gridplot([fig_skredtype, fig_maaned, fig_losneområde, fig_aar], ncols=1, plot_width=500)
    #grid_skredtype = gridplot([fig_steinmaaned, fig_snomaaned], ncols=1, plot_width=500)
    #gird_samlaplot = gridplot([], ncols=1, plot_width=500, plot_height=500)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script_skredtype, div_skredtype = components(fig_skredtype)
    script_maaned, div_maaned = components(fig_maaned)
    script_aar, div_aar = components(fig_aar)
    script_steinmaaned, div_steinmaaned = components(fig_steinmaaned)
    script_snomaaned, div_snomaaned = components(fig_snomaaned)
    script_losneområde, div_losneområde = components(fig_losneområde)
    script_volumomraade, div_volumomraade = components(fig_volumomraade)
    script_steinlosneområde, div_steinlosneområde = components(fig_steinlosneomrade)
    
    html = render_template(
        'index.html',
        script_skredtype=script_skredtype,
        div_skredtype=div_skredtype,
        script_maaned=script_maaned,
        div_maaned=div_maaned,
        script_aar=script_aar,
        div_aar=div_aar,
        script_losneområde=script_losneområde,
        div_losneområde=div_losneområde,
        script_steinmaaned=script_steinmaaned,
        div_steinmaaned=div_steinmaaned,
        script_steinlosneområde=script_steinlosneområde,
        div_steinlosneområde=div_steinlosneområde,
        script_snomaaned=script_snomaaned,
        div_snomaaned=div_snomaaned,
        script_volumomraade=script_volumomraade,
        div_volumomraade=div_volumomraade,
        js_resources=js_resources,
        css_resources=css_resources,
        form=form,
        vegref=vegref,
        viseside=viseside
    )


    return encode_utf8(html)


if __name__ == '__main__':
    app.run(debug=True)


