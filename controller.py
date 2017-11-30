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
    #fylke = IntegerField(label='Fylke (f.eks 14)')
    hpfra = IntegerField(label='HP fra (f.eks 1)', default=1)
    mfra = IntegerField(label='meter fra (f.eks 0)', default=0)
    hptil = IntegerField(label='HP til (f.eks 20)', default=20)
    mtil = IntegerField(label='meter til (f.eks 50000)', default=50000)

@app.route('/', methods=['GET', 'POST'])
def index():

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        veg, hpfra, hptil, mfra, mtil = form.veg.data, form.hpfra.data, form.hptil.data, form.mfra.data, form.mtil.data
        viseside = True
    else:
        viseside = False
        veg = 'fv241'
        fylke = 14
        hpfra = 1
        hptil = 10
        mfra = 0
        mtil = 10000

    if hpfra == hptil:
        vegref = veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + str(mtil)
    else:
        vegref = veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + 'hp' + str(hptil) + 'm' + str(mtil)

    df = data.hentData(vegref)
    fig_skredtype = plot.plotSkredtype(df)
    fig_maaned = plot.plotMaaned(df)
    fig_løsneområde = plot.plotLosneOmrade(df)
    fig_steinmaaned = plot.steinMaaned(df)
    fig_flommaaned = plot.flomMaaned(df)
    fig_snomaaned = plot.snoMaaned(df)

    grid = gridplot([fig_skredtype, fig_maaned, fig_løsneområde, fig_steinmaaned, fig_flommaaned, fig_snomaaned], ncols=1, plot_width=500, plot_height=500)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(grid)
    html = render_template(
        'hoved.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        form=form,
        vegref=vegref,
        viseside=viseside
    )


    return encode_utf8(html)


if __name__ == '__main__':
    app.run(debug=True)


