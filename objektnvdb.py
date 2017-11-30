# -*- coding: utf-8 -*-
"""Fetching a bunch of objects of a specifid type from Norwegian National
road database (NVDB). See https://www.vegvesen.no/nvdb/apidokumentasjon/
Here, we set up a geographic filter for a certain road number (fv30) and county (16),
and a property filter (skiltnummer = Fartsgrense 70 km/t).
"""

import requests
import json
from collections import Counter
import pandas as pd
import numpy as np
from flask import Flask, request, render_template
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.layouts import gridplot
from wtforms import Form, IntegerField, StringField, validators


app = Flask(__name__)

class InputForm(Form):
    veg = StringField(label='Veg (f.eks fv60)', validators=[validators.InputRequired()])
    #fylke = IntegerField(label='Fylke (f.eks 14)')
    hpfra = IntegerField(label='HP fra (f.eks 1)')
    mfra = IntegerField(label='meter fra (f.eks 1200)')
    hptil = IntegerField(label='HP til (f.eks 8)')
    mtil = IntegerField(label='meter til (f.eks 5000)')

vegref = 'fv241'
egenskap = '2326=4198'


@app.route('/', methods=['GET', 'POST'])
def index():

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        veg, hpfra, hptil, mfra, mtil = form.veg.data, form.hpfra.data, form.hptil.data, form.mfra.data, form.mtil.data
    else:
        veg = 'rv5'
        fylke = 14
        hpfra = 1
        hptil = 10
        mfra = 0
        mtil = 30000

    if hpfra == hptil:
        vegref = veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + str(mtil)
    else:
        vegref = veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + 'hp' + str(hptil) + 'm' + str(mtil)

    plotdict = alle_skred_maaneder(vegref)

    stein, steinmaaned = zip(*plotdict[4198].items())
    jord, jordmaaned = zip(*plotdict[4199].items())
    isstein, issteinmaaned = zip(*plotdict[5351].items())
    isnr, ismaaned = zip(*plotdict[4201].items())
    sno, snomaaned = zip(*plotdict[4200].items())
    flom, flomaaned = zip(*plotdict[4202].items())
    sorpe, sorpemaaned = zip(*plotdict[4203].items())
    utgliding, utglidingmaaned = zip(*plotdict[13103].items())

    print(stein)
    print(steinmaaned)
    fig_stein = figure(title="Antall steinskred per månad for " + vegref)
    fig_stein.vbar(x=stein, width=0.5, bottom=0, top=steinmaaned, color='green')

    fig_jord = figure(title="Antall Jord/løsmasse per månad for " + vegref)
    fig_jord.vbar(x=jord, width=0.5, bottom=0, top=jordmaaned, color='green')

    fig_isstein = figure(title="Antall Is/stein per månad for " + vegref)
    fig_isstein.vbar(x=isstein, width=0.5, bottom=0, top=ismaaned, color='green')

    fig_is = figure(title="Antall isnedfall per månad for " + vegref)
    fig_is.vbar(x=isnr, width=0.5, bottom=0, top=ismaaned, color='green')

    fig_sno = figure(title="Antall snøskred per månad for " + vegref)
    fig_sno.vbar(x=sno, width=0.5, bottom=0, top=snomaaned, color='green')

    fig_flom = figure(title="Antall flomskred per månad for " + vegref)
    fig_flom.vbar(x=flom, width=0.5, bottom=0, top=flomaaned, color='green')

    fig_sorpe = figure(title="Antall sørpeskred per månad for " + vegref)
    fig_sorpe.vbar(x=sorpe, width=0.5, bottom=0, top=sorpemaaned, color='green')

    fig_utgliding = figure(title="Antall utgliding per månad for " + vegref)
    fig_utgliding.vbar(x=utgliding, width=0.5, bottom=0, top=utglidingmaaned, color='green')

    grid = gridplot([fig_stein, fig_jord, fig_isstein, fig_is, fig_sno, fig_flom, fig_sorpe], ncols=2, plot_width=500, plot_height=500)

    #plots = {'blue' : fig_maaned, 'green' : fig_aar}

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(grid)
    #script2, div2 = components(fig_aar)
    html = render_template(
        'hoved.html',
        plot_script=script,
        #plot_script2=script2,
        plot_div=div,
        #plot_div2=div2,
        js_resources=js_resources,
        css_resources=css_resources,
        form=form
    )
    return encode_utf8(html)

def skred(fylke, veg, hpfra, hptil, mfra, mtil):
    api = 'https://www.vegvesen.no/nvdb/api/v2/'
    headers =   { 'accept' : 'application/vnd.vegvesen.nvdb-v2+json',
							'X-Client' : 'nvdbskred.py',
							'X-Kontaktperson' : 'jan.aalbu@vegvesen.no'}

    objType = 445 #Skred
    url = api + 'vegobjekter/' + str(objType)
    skredtypenr = [4198, 4199, 5351, 4200, 4201, 4202, 4203, 13103]
    skredtype = {4198 : 'Stein', 4199: 'Jord/løsmasse', 5351: 'Is/stein', 4200: 'Snø', 4201: 'Is', 4202: 'Flomskred (vann+stein+jord)', 4203: 'Sørpeskred (vann+snø+stein)', 13103: 'Utglidning av veg'}
    if hpfra == hptil:
        vegref = veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + 'm' + str(mtil)
    else:
        vegref = veg + 'hp' + str(hpfra) + 'm' + str(mfra) + '-' + 'hp' + str(hptil) + 'm' + str(mtil)
    sNum = 0
    data = []
    for i in skredtypenr:
        filtre = {'egenskap': '2326=' + str(skredtypenr[sNum]), 'vegreferanse' : vegref , 'segmentering' : 'false'}
        rstat = requests.get(url + '/statistikk', headers=headers, params=filtre)
        obj = rstat.json()
        data.append([skredtype[i], obj['antall']])
        sNum = sNum + 1
    return data

def alle_skred_maaneder(vegref):
    skredtypenr = [4198, 4199, 5351, 4200, 4201, 4202, 4203, 13103]
    skredtype = {4198 : 'Stein', 4199: 'Jord/løsmasse', 5351: 'Is/stein', 4200: 'Snø', 4201: 'Is', 4202: 'Flomskred (vann+stein+jord)', 4203: 'Sørpeskred (vann+snø+stein)', 13103: 'Utglidning av veg'}
    sdict = {}
    for i in skredtypenr:
        egenskap = '2326=' + str(i)
        sdict[i] = skredMaaneder(egenskap, vegref)
    return sdict

def hentStatistikk(egenskap, vegref):
    api = 'https://www.vegvesen.no/nvdb/api/v2/'
    headers =   { 'accept' : 'application/vnd.vegvesen.nvdb-v2+json',
                        'X-Client' : 'NVDB Skred',
                        'X-Kontaktperson' : 'jan.aalbu@vegvesen.no'}
    objType = 445
    url = api + 'vegobjekter/' + str( objType )
    filtre = {'egenskap': egenskap, 'vegreferanse': vegref, 'segmentering' : 'false'}
    rstat = requests.get( url + '/statistikk', headers=headers, params=filtre )
    stat = rstat.json()
    print(stat)
    return stat

def antallSkred(egenskap, vegref):
    stat = hentStatistikk(egenskap, vegref)['antall']
    return stat

def hentMangeskred(egenskap, vegref):
    api = 'https://www.vegvesen.no/nvdb/api/v2/'
    headers =   { 'accept' : 'application/vnd.vegvesen.nvdb-v2+json',
                        'X-Client' : 'NVDB Skred',
                        'X-Kontaktperson' : 'jan.aalbu@vegvesen.no'}
    objType = 445
    url = api + 'vegobjekter/' + str( objType )
    filtre = {'egenskap': egenskap, 'vegreferanse': vegref, 'segmentering' : 'false'}

    # Hva skal vi ha med av egenskaper og lokasjonsdata?
    # Ref https://www.vegvesen.no/nvdb/apidokumentasjon/#/get/vegobjekter
    #      Under "Velg respons"
    filtre['inkluder'] = 'alle'
    r = requests.get( url, headers = headers, params = filtre)
    mangeskred = r.json()
    return mangeskred

def hentEttskred(mangeskred,  nr):
    ettskred = mangeskred['objekter'][nr]
    return ettskred

def finnDato(ettskred): #Tar eit skredobjekt som input, gir ut dato for skredet
    egenskap = ettskred['egenskaper']
    if next((item for item in egenskap if item['id'] == 2324), None) == None:
        return '0'
    else:
        datodict = next((item for item in egenskap if item['id'] == 2324), None)
        dato = datodict['verdi']
        return dato


def finnMaaned(ettskred): #Tar eit skredobjekt som input, gir ut måned for skredet
    dato = finnDato(ettskred)
    maaned = dato[5:7]
    print(maaned)
    print(type(maaned))
    if maaned == '':
        return 0
    else:
        mint = int(maaned)
    print(type(mint))
    print(mint)
    return mint

def finnAar(ettskred):
    dato = finnDato(ettskred)
    aar = dato[0:4]
    return aar

def finnDag(ettskred):
    dato = finnDato(ettskred)
    dag = dato[8:10]
    return dag

def skredMaaneder(egenskap, vegref):
    maaneder = []
    mangeskred = hentMangeskred(egenskap, vegref)
    for i in range(0, antallSkred(egenskap, vegref)):
        ettskred = mangeskred['objekter'][i]
        maaned = finnMaaned(ettskred)
        maaneder.append(maaned)

    mdict = dict(Counter(maaneder))
    return mdict

def skredAar(egenskap, vegref):
    aar = []
    mangeskred = hentMangeskred(egenskap, vegref)
    for i in range(0, antallSkred(egenskap, vegref)):
        ettskred = mangeskred['objekter'][i]
        etaar = finnAar(ettskred)
        aar.append(etaar)

    mdict = dict(Counter(aar))
    return mdict



#dict_med_skred = alle_skred_maaneder(vegref)
#print(dict_med_skred)
#print(dict_med_skred[4199])
#print(hentStatistikk(egenskap, vegref))
#print(finnMaaned(hentEttskred(hentMangeskred(egenskap, vegref), 1)))
#print(antallSkred(egenskap, vegref))
#print(skredMaaneder(egenskap, vegref))
#print(skredAar(egenskap, vegref))

#group = dfm.groupby('0')
#print(group)
#print(dfm)
#print(Counter(maaneder))
#mdict = dict(Counter(maaneder))
#print(mdict)
#df = pd.DataFrame(mdict, index=['Antall'])
#print(df)
#source = ColumnDataSource(df)

#mliste = map(list, mdict.items())
#print(mliste)


#print(json.dumps(mangeskred, indent=4))
#ettskred = mangeskred['objekter'][1]
#print(json.dumps(ettskred, indent=4))

#print(ettskred['geometri']['wkt'])


#print(ettskred['egenskaper'])
#egenskap = ettskred['egenskaper']
#print(json.dumps(egenskap, indent=4))
#datodict = next((item for item in egenskap if item['id'] == 2324), None)
#print(datodict)
#print(datodict['verdi'])


if __name__ == '__main__':
    app.run(debug=True)
