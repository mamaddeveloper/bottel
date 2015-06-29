import StringIO
import json
import logging
import random
import urllib
import urllib2

import random

#for importing countdown
import datetime

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '122588379:AAEepyctVILJi-V2gHA4olBzwkByPC4RUWs'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
	# key name: str(chat_id)
	enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
	es = EnableStatus.get_or_insert(str(chat_id))
	es.enabled = yes
	es.put()

def getEnabled(chat_id):
	es = EnableStatus.get_by_id(str(chat_id))
	if es:
		return es.enabled
	return False


# ================================

class MeHandler(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(60)
		self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(60)
		self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
	def get(self):
		urlfetch.set_default_fetch_deadline(60)
		url = self.request.get('url')
		if url:
			self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
	def post(self):
		urlfetch.set_default_fetch_deadline(60)
		body = json.loads(self.request.body)
		logging.info('request body:')
		logging.info(body)
		self.response.write(json.dumps(body))

		update_id = body['update_id']
		message = body['message']
		message_id = message.get('message_id')
		date = message.get('date')
		text = message.get('text')
		fr = message.get('from')
		chat = message['chat']
		chat_id = chat['id']

		if not text:
			logging.info('no text')
			return

		def reply(msg=None, img=None):
			if msg:
				resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
					'chat_id': str(chat_id),
					'text': msg.encode('utf-8'),
					'disable_web_page_preview': 'true',
					'reply_to_message_id': str(message_id),
				})).read()
			elif img:
				resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
					('chat_id', str(chat_id)),
					('reply_to_message_id', str(message_id)),
				], [
					('photo', 'image.jpg', img),
				])
			else:
				logging.error('no msg or img specified')
				resp = None

			logging.info('send response:')
			logging.info(resp)

		if text.startswith('/'):
			if text == '/start':
				reply('Bot enabled')
				setEnabled(chat_id, True)
			#elif text == '/stop':
			#    reply('Bot disabled')
			#    setEnabled(chat_id, False)

			elif text == '/command1':
				reply("Prueba a decir: \n/tiempo para la cuenta atras.\n/cartel para ver el cartel del AS\n/iker para frase mitica aleatoria de Iker.\n/lefuck para frase mitica aleatoria de LeFuck\n/acorde para frase mitica de este.\n/alfonso para saber que se comeria.\n/michel para la frase de la sandia.\n/jess para sus orales\n/shurtiz para parar el endiose.\n/aaaa para saltos de linea.\n\n Bot creado por @ShurKevin")

			elif text == '/tiempo':
				limit = datetime.datetime(2015, 07, 28, 8, 0, 0)
				now = datetime.datetime.now()
				diff = limit - now
				def convert_timedelta(diff):
					days, seconds = diff.days, diff.seconds
					hours = seconds // 3600
					minutes = (seconds % 3600) // 60
					seconds = (seconds % 60)
					return days, hours, minutes, seconds
				diff = convert_timedelta(diff)
				if diff[0] == 1:
					text1="Queda %d dia" % (diff[0])
				else:
					text1="Quedan %d dias" % (diff[0])

				if diff[1] == 1:
					text2=", %d hora" % (diff[1])
				else:
					text2=", %d horas" % (diff[1])
				
				if diff[2] == 1:
					text3=", %d minuto" % (diff[2])
				else:
					text3=", %d minutos" % (diff[2])
				
				if diff[3] == 1:
					text4="y %d segundo para el Arenal Sound 2015!" % (diff[3])
				else:
					text4="y %d segundos para el Arenal Sound 2015!" % (diff[3])
				text="%s %s %s %s" % (text1, text2, text3, text4)
				text = str(text)
				reply(text)

			elif text == '/cartel':
				reply('http://www.arenalsound.com/wp-content/uploads/2015/06/as_cartel5.jpg')

			elif text == '/grupointeresante':
				aleatorio = random.choice(['Sunset Sons', 'Don Broco', 'La Pegatina', 'Rayden\n(no troll)\n(no homo)', 'DJs From Mars', 'Rudimental', 'Carlos Sadness', 'The Kooks', 'Zedd', 'We Are Scientists', 'Twin Atlantic', 'The Subways', 'Supersubmarina', 'Nero', 'Mystery Skulls', 'Holy Bouncer', 'Monarchy', 'Varry Brava', 'South Central', 'Dinero'])
				reply(aleatorio)

			elif text == '/acorde':
				aleatorio = random.choice(['TRANQUI SI SOMOS GENTE NORMAL, SOLO QUEREMOS QUE NOS GUIES\nGUIAMEEEEE', 'tracatracapumplasplastracatracaplasplasquetequetepantuquesumumtanquetequetetan (beatbox)'])
				reply(aleatorio)

			elif text == '/iker':
				aleatorio = random.choice(['Con este floodito me voy a ir del grupito ahora mismito', 'hahahahaha', 'Soy el Iker, un sofisticado robot sexual enviado a traves del tiempo para cambiarle el futuro a una mujer afortunada. jejejejeje'])
				reply(aleatorio)

			elif text == '/lefuck':
				aleatorio = random.choice(['Ub kalcetin \n Y sela metemo por el kulo', 'Compranos calientaburras \n y nos cojemos a dos putas'])
				reply(aleatorio)

			elif text == '/alfonso':
				aleatorio = random.choice(['Sabeis lo que me comeria yo ahora mismo?', 'Ahora mismo me comeria un pussy.'])
				reply(aleatorio)

			elif text == '/michel':
				reply('En este grupo de mierda solo se puede hablar tranquilamente a partir de las 2 de la manyana. Putos flooders si supierais el asco que me dais no me diriais ni donde sera la quedada. este flood es un insulto a mi inteligencia y a la profesion de cocinero. Hace tanto calor que entre comerme un conyo y una sandia bien fresquita me comeria un conyo, pa que os voy a enganyar. Estais arruinando mi puta experiencia en telegram.')

			elif text == '/jess':
				aleatorio = random.choice(['Mis orales son 10 minutos.', 'Fer... tu polla esta un poco deforme\njijiji\nEs un poco fea eh...'])
				reply(aleatorio)

			elif text == '/shurtiz':
				reply('No endioses.')

			elif text == '/aaaa':
				reply('Ups...\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\nMenos mal.')

app = webapp2.WSGIApplication([
	('/me', MeHandler),
	('/updates', GetUpdatesHandler),
	('/set_webhook', SetWebhookHandler),
	('/webhook', WebhookHandler),
], debug=True)
