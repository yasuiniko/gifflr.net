import pytumblr
from flask import Flask, request, redirect, render_template
from itertools import permutations
#from wtforms import Form, TextAreaField, fields, validators, widgets

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')

@app.route('/gifs', methods = ['POST'])
def findGif():
	tumurl = ''
	tumclient = pytumblr.TumblrRestClient(
	  'Kjr56gcuNUtyRDZfhy6rsmmv5cUatTzcVlGg2MsDh67Wq23MxM',)
	gifstring = request.values.get('string')

	punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	no_punct = ""
	for char in gifstring:
	   if char not in punctuation:
	       no_punct = no_punct + char

	words = no_punct.split()
	finalists = []

	for e in words:

		tumresp = tumclient.tagged(e+' gif', limit = 5000)
		notecount = []
		index = 0

		for x in xrange(0,len(tumresp)):
			if 'photos' in tumresp[x]:
				notecount.append(tumresp[x]['note_count'])
		
		if notecount:
			notecount.sort()
			notecount.reverse()

			for i in xrange(0,len(tumresp)):
				if(tumresp[i]['note_count'] == notecount[0]):
					finalists.append(tumresp[i])

	if len(words) > 1:
		for e in permutations(words, 2):
			d = ' '.join(elem for elem in e)
			tumresp = tumclient.tagged(d+' gif', limit = 5000)
			notecount = []
			index = 0

			for x in xrange(0,len(tumresp)):
				if 'photos' in tumresp[x]:
					notecount.append(tumresp[x]['note_count'])
			
			if notecount:
				notecount.sort()
				notecount.reverse()

				for i in xrange(0,len(tumresp)):
					if(tumresp[i]['note_count'] == notecount[0]):
						finalists.append(tumresp[i])
			
	if finalists:
		notecount = []
		for x in xrange(0,len(finalists)):
			notecount.append(finalists[x]['note_count'])

		notecount.sort()
		notecount.reverse()

		for i in xrange(0,len(finalists)):
			if(finalists[i]['note_count'] == notecount[0]):
				index = i
	try:
		tumurl = finalists[index]['photos'][0]['original_size']['url']
	except IndexError:
		tumurl = '/'
	except KeyError:
		tumurl = '/'

	return tumurl

if __name__ == '__main__':
	app.run(debug = True)