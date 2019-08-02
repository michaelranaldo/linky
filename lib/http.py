from lib import logger
import requests

def connect(url,cookie):
	cookies={'li_at': cookie, 'JSESSIONID': 'ajax:0397788525211216808'}
	headers={'Csrf-Token': 'ajax:0397788525211216808', 'X-RestLi-Protocol-Version': '2.0.0'}

	try:
		r=requests.get(url, headers=headers,cookies=cookies)
		data=r.text
		if 'CSRF check failed.' in data:
			logger.red('Failed to authenticate to LinkedIn')
			return None
		return r
	except Exception as e:
		error=str(e)
		logger.red(error)
		logger.red('Check the cookie and make sure its correct!')
		return None