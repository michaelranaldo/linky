#!/usr/bin/python3
from lib import logger,user_enum, banner
import argparse, os.path, json
from time import sleep

'''

Linky is a LinkedIn Enumerator.

Inspired by @vysecurity.

'''

# The most important part...
banner.banner()

parser = argparse.ArgumentParser(description="Yet another LinkedIn scraper.")
parser.add_argument("-c", "--cookie", required=True, metavar="", help="Cookie to authenticate to LinkedIn with [li_at]")
parser.add_argument("-i", "--company-id", metavar="", help="Company ID number")
parser.add_argument("-k", "--keyword", metavar="", help="Keyword for searches")
parser.add_argument("-d", "--domain", metavar="", help="Company domain name")
parser.add_argument("-o", "--output", metavar="", help="File to output to: Writes CSV, JSON and HTML.")
parser.add_argument("-f", "--format", metavar="", help="Format for email addresses")
args = parser.parse_args()

if os.path.isfile(args.cookie):
	try:
		with open(args.cookie,'r') as f:
			cookie=f.readline()
			logger.green('Got cookie: [%s]' % logger.GREEN(cookie))
	except:
		logger.red('Could not open'+args.cookie)
		quit()
else:
	cookie=args.cookie

company_id=args.company_id

domain=args.domain

if args.output:
	filename = args.output
else:
	filename=None

if args.keyword == None:
	keyword = None
else:
	keyword = args.keyword

if args.format:
	email_schemes=['firstname.surname','firstnamesurname','f.surname','fsurname','surname.firstname','surnamefirstname','s.firstname','sfirstname']
	email_format=args.format.lower()
	if email_format not in email_schemes:
		logger.red('Unknown email scheme specified, please see the available below:')
		for i in email_schemes:
			logger.blue(i)
		quit()	
else:
	email_format='firstname.surname'

if args.company_id == None:
	logger.red('Please specify a company id with the %s flag' % logger.RED('-id'))
	quit()
if args.domain == None:
	logger.red('Please specify a domain with the %s flag' % logger.RED('-d'))
	quit()
connection_data=[cookie,company_id,email_format]
try:
	sleep(2)
	users=user_enum.run(connection_data,domain,filename,keyword)
except KeyboardInterrupt:
	logger.yellow('Keyboard interrupt detected!')
	quit()

logger.green('Done!')