#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import requests
import hashlib
import random
import base64
import glob
import mimetypes
import xml.etree.ElementTree as ET
from logging import getLogger
from datetime import datetime
from util import Util
from exception import RequestExceededError

logger = getLogger(__name__)

class Hatena:

	media_url = 'https://f.hatena.ne.jp/atom/post'
	media_dir_name = 'Twitter Photos'
	default_category = ['twitter']
	
	def __init__(self, user_id, blog_id):
		self.user_id = user_id
		self.root_endpoint = 'https://blog.hatena.ne.jp/' + user_id + '/' + blog_id + '/atom'
		self.wsse = None
	
	def auth(self):
		ut = Util()
		created = ut.datetime_to_iso8601(datetime.now())
		nonce = hashlib.sha1(str(random.random()).encode()).digest()
		digest = hashlib.sha1(nonce + created.encode() + os.environ['HT_KEY'].encode()).digest()
		s = 'UsernameToken Username="{0}", PasswordDigest="{1}", Nonce="{2}", Created="{3}"'
		self.wsse = s.format(self.user_id, base64.b64encode(digest).decode(), base64.b64encode(nonce).decode(), created)
		return
	
	def create_media_payload(self, mimetype, data, name):
		entry = ET.Element('entry',{'xmlns':'http://purl.org/atom/ns#'})
		title = ET.SubElement(entry, 'title')
		title.text = name
		content = ET.SubElement(entry, 'content')
		content.text = data
		content.set('mode', 'base64')
		content.set('type', mimetype)
		dir = ET.SubElement(entry, 'dc:subject')
		dir.text = Hatena.media_dir_name
		return ET.tostring(entry, encoding='utf8', method='xml')
	
	def upload_media(self, filepath, media_key):
		path = filepath + os.sep + media_key
		try:
			filename = glob.glob(path + '.*')[0]
		except:
			logger.info('[INFO] no media for ' + media_key)
			return None
		with open(filename, 'rb') as f:
			image_data = f.read()
		content = base64.b64encode(image_data).decode('utf-8')
		mimetype = mimetypes.guess_type(filename)[0]
		
		media_entry = self.create_media_payload(mimetype, content, media_key)
		res = requests.post(Hatena.media_url, data=media_entry, headers={'X-WSSE': self.wsse})
		return ET.fromstring(res.text)
	
	def parse_media_syntax_from_xml(self, root):
		for child in root:
			if 'syntax' in child.tag:
				return child.text
				
	def parse_hashtag(self, text):
		return [w[1:] for w in text.split() if w.startswith("#") ]
	
	def escape_hashtag(self, text):
		return text.replace('#', '\#')
	
	def create_entry_content(self, tweets, medias):
		ut = Util()
		body = ''
		tags = []
		for tweet in tweets:
			tags += self.parse_hashtag(tweet['text'])
			text = self.escape_hashtag(tweet['text'])
			utc_time = tweet['created_at']
			local_time = ut.utc_str_to_local(utc_time)			
			
			body += text + '\n'
			if 'attachments' in tweet.keys() and 'media_keys' in tweet['attachments'].keys():
				for media_key in tweet['attachments']['media_keys']:
					if media_key in medias:
						body += '\n[' + medias[media_key]  +  ']\n'
			body += '\n <font size="1" color="#c0c0c0">' + local_time.strftime("%d %B %Y %H:%M") + '</font>\n\n'
		return body, tags
				
	def create_entry_payload(self, date, tweets, medias):
		ut = Util()
		body, tags = self.create_entry_content(tweets, medias)
		tags = tags + Hatena.default_category
		tags = list(set(tags))
	
		entry = ET.Element('entry',{'xmlns':'http://www.w3.org/2005/Atom', 'xmlns:app':'http://www.w3.org/2007/app'})
		title = ET.SubElement(entry, 'title')
		title.text = date
		author = ET.SubElement(entry, 'author')
		name = ET.SubElement(author, 'name')
		name.text = self.user_id
		content = ET.SubElement(entry, 'content')
		content.text = body
		content.set('type', 'text/plain')
		updated = ET.SubElement(entry, 'updated')
		updated.text = ut.date_to_iso_format(date)
		for tag in tags:
			category = ET.SubElement(entry, 'category')
			category.set('term', tag)
		control = ET.SubElement(entry, 'app:control')
		draft = ET.SubElement(control, 'app:draft')
		draft.text = "no"
		return ET.tostring(entry, encoding='utf8', method='xml')

	def create_entry(self, date, tweets, media_path):
		medias = {}
		for tweet in tweets:
			if 'attachments' in tweet.keys() and 'media_keys' in tweet['attachments'].keys():
				for media_key in tweet['attachments']['media_keys']:
					filepath = media_path
					media_entry = self.upload_media(filepath, media_key)
					if media_entry != None:
						media_syntax = self.parse_media_syntax_from_xml(media_entry)
						medias[media_key] = media_syntax
		return self.create_entry_payload(date, tweets, medias)		
	
	def post_entry(self, entry):
		url = self.root_endpoint + '/entry'
		res = requests.post(url, data=entry, headers={'X-WSSE': self.wsse})
		if res.status_code != requests.codes.created:
			logger.info('-------------[entry post response]---------------')
			logger.info(res.status_code)
			logger.info(res.text)
		if res.status_code == requests.codes.bad_request and 'Entry limit was exceeded' in res.text:
			raise RequestExceededError('Hatena Entry limit was exceeded.')
		return
