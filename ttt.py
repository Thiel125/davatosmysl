import urllib2
import os
import csv
import json
import random
import urllib
import dicttoxml
import requests
import pandas as pd
from flask import render_template, Flask,jsonify,make_response, Response
'''https://github.com/newnewcorder/flask-chartjs-demo'''
os.environ['no_proxy']='*'

app = Flask(__name__)

def wpjson():
    r=urllib2.urlopen('https://blog.iservery.com/wp-json/wp/v2/posts')
    data=json.load(r)
    pole=[]
    for radek in data:
        inradek=dict(nadpis=radek['title']['rendered'],text=radek['content']['rendered'])
        #inradek{'nadpis':'data','text':'data'}
        pole.append(inradek)
    return pole

@app.route('/json')
def jsex():
    return jsonify(list=wpjson())

@app.route('/xml')
def xmlex():
    list = wpjson()
    xml = dicttoxml.dicttoxml(list)
    response= make_response(xml,200)
    response.headers['Content-Type']='application/xml'
    return response

@app.route('/html')
def htmllex():
    url = "http://192.168.10.1/test.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for prvek in data['data']:
        print prvek
        return prvek
    print data
    return data

@app.route('/csv')
def csfout():
    def generate():
            my_list_of_dicts = wpjson()
            for row in my_list_of_dicts:
                yield row['nadpis']+';\n'

    return Response(generate(), mimetype='text/csv')

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port = port)