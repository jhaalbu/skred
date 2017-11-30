import pandas as pd
import matplotlib as plt
import numpy as np
import requests

def hentData(vegref):

    api = 'https://www.vegvesen.no/nvdb/api/v2/'
    headers =   { 'accept' : 'application/vnd.vegvesen.nvdb-v2+json', 'X-Client' : 'nvdbskred.py','X-Kontaktperson' : 'jan.aalbu@vegvesen.no'}

    #vegref = 'fv241'


    objType = 445 #Skred
    url = api + 'vegobjekter/' + str(objType)
    filtre = {'vegreferanse': vegref, 'segmentering' : 'false', 'srid' : 4326}
    rstat = requests.get(url + '/statistikk', headers=headers, params=filtre)
    skredstat = rstat.json()
    filtre['inkluder'] = 'egenskaper,lokasjon'
    r = requests.get(url, headers=headers, params=filtre)
    skred = r.json()

    #print(skredstat)
    antall = skredstat['antall']

    liste = []

    for i in range(1,antall):
        ettskred = skred['objekter'][i]
        if 'egenskaper' in ettskred:
            skredid = ettskred['id']
            if next((item for item in ettskred['egenskaper'] if item['id'] == 2324), None) == None:
                maaned = 'Ingen data'
            else:
                maaned = next((item for item in ettskred['egenskaper'] if item['id'] == 2324), None)['verdi'][5:7]

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2324), None) == None:
                aar = 'Ingen data'
            else:
                aar = next((item for item in ettskred['egenskaper'] if item['id'] == 2324), None)['verdi'][0:4]

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2324), None) == None:
                dag = 'Ingen data'
            else:
                dag = next((item for item in ettskred['egenskaper'] if item['id'] == 2324), None)['verdi'][8:10]

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2326), None) == None:
                skredtype = 'Ingen data'
            else:
                skredtype = next((item for item in ettskred['egenskaper'] if item['id'] == 2326), None)['verdi']


            if next((item for item in ettskred['egenskaper'] if item['id'] == 2328), None) == None:
                losneomraade = 'Ingen data'
            else:
                losneomraade = next((item for item in ettskred['egenskaper'] if item['id'] == 2328), None)['verdi']

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2330), None) == None:
                hoyde = 'Ingen data'
            else:
                hoyde = next((item for item in ettskred['egenskaper'] if item['id'] == 2330), None)['verdi']

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2325), None) == None:
                klokke = 'Ingen data'
            else:
                klokke = next((item for item in ettskred['egenskaper'] if item['id'] == 2325), None)['verdi']

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2339), None) == None:
                vaer = 'Ingen data'
            else:
                vaer = next((item for item in ettskred['egenskaper'] if item['id'] == 2339), None)['verdi']

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2341), None) == None:
                blokkert_veglengde = 'Ingen data'
            else:
                blokkert_veglengde = next((item for item in ettskred['egenskaper'] if item['id'] == 2341), None)['verdi']

            if next((item for item in ettskred['egenskaper'] if item['id'] == 2344), None) == None:
                stenging = 'Ingen data'
            else:
                stenging = next((item for item in ettskred['egenskaper'] if item['id'] == 2344), None)['verdi']

            vegreferanse = ettskred['lokasjon']['vegreferanser'][0]['kortform']
            geometri = ettskred['lokasjon']['geometri']['wkt']

            skreddict = {'SkredID' : skredid,
                         'Skredtype' : skredtype,
                         'Maaned' : maaned,
                         'År' : aar,
                         'Dag' : dag,
                         'Klokke' : klokke,
                         'Løsneområde' : losneomraade,
                         'Høgde' : hoyde,
                         'Vær' : vaer,
                         'Blokkert veglengde' : blokkert_veglengde,
                         'Stenging' : stenging,
                         'Vegreferanse' : vegreferanse,
                         'Geometri' : geometri}
            liste.append(skreddict)

    df = pd.DataFrame(liste)

    return(df)


