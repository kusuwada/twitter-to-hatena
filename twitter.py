#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import requests
import json
import urllib
from logging import getLogger
from datetime import timedelta
from requests_oauthlib import OAuth1
from util import Util

logger = getLogger(__name__)

class Twitter:

	tweet_fields = 'created_at,text'
	media_fields = 'url'
	base_url = 'https://api.twitter.com/2/'
	
	def __init__(self):
		self.user_id = None
		self.access_token = None

	def auth(self):
		self.access_token = OAuth1(os.environ['TW_API_KEY'], os.environ['TW_API_KEY_SECRET'], os.environ['TW_CLIENT_ID'], os.environ['TW_CLIENT_SECRET'])
		return
	
	def get_user_id(self, username):
		uri = 'https://api.twitter.com/2/users/by/username/' + username
		res = requests.get(uri, auth=self.access_token)
		logger.info('Get User ID')
		logger.info(json.loads(res.text))
		self.user_id = json.loads(res.text)['data']['id']
		return self.user_id
	
	def list_daily(self, date):
		ut = Util()
		timeline_path = 'users/' + self.user_id + '/tweets'
		dt = ut.local_date_to_utc_datetime(date)
		start_time = ut.datetime_to_iso8601(dt)
		end_time = ut.datetime_to_iso8601(dt + timedelta(days=1) - timedelta(seconds=1))
		start_time = urllib.parse.quote(start_time)
		end_time = urllib.parse.quote(end_time)
		query = '?start_time=' + start_time + '&end_time=' + end_time
		query += '&exclude=retweets,replies'
		query += '&tweet.fields=' + Twitter.tweet_fields + \
			'&expansions=attachments.media_keys' + \
			'&media.fields=' + Twitter.media_fields
		uri = Twitter.base_url + timeline_path + query
		res = requests.get(uri, auth=self.access_token)
		return json.loads(res.text)
	
	# (only for public account)
	def download_medias(self, medias, media_path):
		ut = Util()
		filepath = media_path
		logger.info(filepath)
		logger.info(medias)
		for media in medias:
			if media['type'] == 'photo':  # only photo
				extension = media['url'].split('.')[-1]
				ut.media_download(media['url'], filepath, media['media_key'] + '.' + extension)
		return
