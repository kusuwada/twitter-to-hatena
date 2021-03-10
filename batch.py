#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import daily
from util import Util

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='export tweet to hatena.')
	parser.add_argument('start', help='start date to export. [YYYY-MM-DD]')
	parser.add_argument('end', help='end date to export. [YYYY-MM-DD]')
	parser.add_argument('tw_id', help='Twitter name')
	parser.add_argument('ht_id', help='Hatena ID')
	parser.add_argument('ht_host', help='Hatena domain. e.g. example.hatenadiary.com')
	parser.add_argument('work_dir', help='working directory path')
	parser.add_argument('--tz', help='timezone')
	args = parser.parse_args()
	
	ut = Util()
	for date in ut.daterange_to_list(args.start, args.end):
		daily.daily(date, args.tw_id, args.ht_id, args.ht_host, args.work_dir, args.tz)