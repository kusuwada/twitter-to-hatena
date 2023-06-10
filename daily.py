#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import argparse
import glob
from logging import basicConfig, getLogger, INFO
from twitter import Twitter
from hatena import Hatena
from util import Util

basicConfig(level=INFO)
logger = getLogger(__name__)

def daily(date, tw_id, ht_id, ht_host, work_dir, tz='Etc/UTC'):

	## set timezone
	Util.tz_str = tz
	## set tmp media filepath
	media_path = work_dir
	
	logger.info('[START]' + date)
	
	## get tweets from twitter
	tw = Twitter()
	tw.auth()
	tw.get_user_id(tw_id)
	logger.info(tw_data)
	tw_data = tw.list_daily(date)
	if tw_data['meta']['result_count'] == 0:
		logger.info('[NO POST]' + date)
		return
	if 'includes' in tw_data.keys() and 'media' in tw_data['includes'].keys():
		tw.download_medias(tw_data['includes']['media'], media_path)
	logger.info('[INFO] finish twitter data fetch.')
	
	## post to hatena
	tw_list_sorted = sorted(tw_data['data'], key=lambda x: x['id'])
	ht = Hatena(ht_id, ht_host)
	ht.auth()
	entry = ht.create_entry(date, tw_list_sorted, media_path)
	try:
		ht.post_entry(entry)
	except Exception as e:
		raise(e)
	logger.info('[EXPORTED]' + date)

if __name__ == "__main__":	
	parser = argparse.ArgumentParser(description='export tweet to hatena.')
	parser.add_argument('date', help='date to export. [YYYY-MM-DD]')
	parser.add_argument('tw_id', help='Twitter name')
	parser.add_argument('ht_id', help='Hatena ID')
	parser.add_argument('ht_host', help='Hatena domain. e.g. example.hatenadiary.com')
	parser.add_argument('work_dir', help='working directory path')
	parser.add_argument('--tz', help='timezone')
	args = parser.parse_args()
	
	try:
		daily(args.date, args.tw_id, args.ht_id, args.ht_host, args.work_dir, args.tz)
	except Exception as e:
		logger.error(e)
		sys.exit(1)
