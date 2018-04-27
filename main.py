from flask import Flask, render_template, request
import json

page_size=20
w=json.load(open("worldl.json"))
alp = sorted(list(set([c['name'][0] for c in w])))

print (alp)

for c in w:
    c['tld']=c['tld'][1:]
page_size=20

app=Flask(__name__)
# for c in w:
# 	c['tld']=c['tld'][1:]

@app.route('/')
def index():
   	return render_template('index.html',
   		w=w[0:page_size],
   		page_number=0,
        page_size=page_size,
        alp=alp)

@app.route('/alpha/<a>')
def alpha(a):
    c1=[c for c in w if c['name'][0]==a]
    return render_template (
        'continentpage.html',
        length_of_c1=len(c1),
        c1 = c1,
        a = a,
        alp=alp)


@app.route('/country/<i>')
def country(i):
    return render_template('countrypage.html', c = w[int(i)])

@app.route('/countryByName/<n>')
def countryByName(n):
	c=None
	for x in w:
		if x['name'] == n:
			c=x
	return render_template('countrypage.html',c=c)

@app.route('/continent/<a>')
def continent(a):
    c1=[c for c in w if c['continent']==a]
    return render_template (
    	'continentpage.html',
    	length_of_c1=len(c1),
    	c1 = c1,
    	a = a)

@app.route('/begin/<b>')
def beginPage(b):
    bn = int(b)
    return render_template('index.html',
        w = w[bn:bn+page_size],
        page_number = bn,
        page_size = page_size,
        alp=alp
        )

@app.route('/delete/<n>')
def deleteCountry(n):
    i=0
    for c in w:
        if c['name']==n:
            break
        i=i+1
    del w[i]
    return render_template('index.html',
        page_number=0,
        page_size=page_size,
        w=w[0:page_size])

@app.route('/editcountryByName/<n>')
def editcountryByName(n):
    c=None
    for x in w:
        if x['name'] == n:
            c=x
    return render_template('countryedit.html'
        ,c=c)

@app.route('/create')
def create():
    return render_template('createCountry.html',
     c=c)

@app.route('/createCountry')
def createCountry(): 
    c={}
    c['name'] =request.args.get('name')
    c['capital'] =request.args.get('capital')
    c['continent'] =request.args.get('continent')
    c['area'] =int(request.args.get('area'))
    c['population'] =int(request.args.get('population'))
    c['gdp'] =float(request.args.get('gdp'))
    c['tld'] =request.args.get('tld')
    c['flag'] =request.args.get('flag')
    w.append(c)
    w.sort(key=lambda c: c['name'])
    return render_template('countrypage.html',c=c)

@app.route('/updateCountryByName')
def updateCountryByName():
    n=request.args.get('name')
    c=None
    for x in w:
        if x['name'] == n:
            c=x
    c['capital'] =request.args.get('capital')
    c['continent'] =request.args.get('continent')
    c['area'] =int(request.args.get('area'))
    c['population'] =int(request.args.get('population'))
    c['gdp'] =float(request.args.get('gdp'))
    c['tld'] =request.args.get('tld')
    w.append(c)
    return render_template(
            'countrypage.html',
            c=c)

app.run(host='0.0.0.0', port=8080, debug=True)
print(w[182]['continent'])