from time import gmtime, strftime
from lib import html
import pandas as pd
import csv, json
import os

colour_red = "\033[1;31m"
colour_blue = "\033[1;34m"
colour_green = "\033[1;32m"
colour_yellow = "\033[1;33m"
colour_remove= "\033[0m"
cur_dir=os.path.dirname(os.path.abspath(__file__))

def RED(string):
	string=str(string)
	return (colour_red + string + colour_remove)

def BLUE(string):
	string=str(string)
	return (colour_blue + string + colour_remove)

def GREEN(string):
	string=str(string)
	return (colour_green + string + colour_remove)

def YELLOW(string):
	string=str(string)
	return (colour_yellow + string + colour_remove)

def blue(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+BLUE(' >> ' )+string)

def green(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+GREEN(' >> ' )+string)

def red(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+RED(' >> ' )+string)

def yellow(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+YELLOW(' >> ' )+string)

def write_out(data,domain,word_occurrence,filename):
	if filename == None:
		return
	write_html(data,domain,word_occurrence,filename)
	write_csv(data,domain,word_occurrence,filename)
	write_json(data,domain,word_occurrence,filename)

def write_csv(data,domain,word_occurrence,filename):
	filename=filename+'.csv'
	headers=['picture','fullname','firstname','middlename','surname','email','current role','current company']
	with open(filename,'w') as f:
		writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['fullname','firstname','middlename','surname','email','current role','current company'])
		for d in data:
			for k,v in d.items():
				fullname=k
				profile_url=v[0]
				picture=v[1]
				if picture == None:
					picture=cur_dir+'/html/src/blank.jpg'
				firstname=v[2]
				middlename=v[3]
				surname=v[4]
				email=v[5]
				current_role=v[6]
				current_company=v[7]
				writer.writerow([fullname,firstname,middlename,surname,email,current_role,current_company,profile_url])

def write_json(data,domain,word_occurrence,filename):
	filename=filename+'.json'
	with open(filename,'w') as f:
		json.dump(data,f)

def write_html(data,domain,word_occurrence,filename):
	user_counter=0
	for d in data:
		for k,v in d.items():
			user_counter+=1
	filename=filename+'.html'
	with open(filename,'w') as f:
		title='Linky: % s' % domain
		f.write(html.header(title))
		headers=['picture','fullname','firstname','middlename','surname','email','current role','current company']
		f.write(html.h3_span(['Users',user_counter]))
		f.write(html.p('Click the users image to view their LinkedIn!'))
		f.write(html.table_head(headers))
		for d in data:
			for k,v in d.items():
				fullname=k
				profile_url=v[0]
				picture=v[1]
				if picture == None:
					picture=False
				firstname=v[2]
				middlename=v[3]
				surname=v[4]
				email=v[5]
				current_role=v[6]
				current_company=v[7]
				f.write('<tr>\n')
				f.write(html.table_picture(profile_url,picture))
				f.write(html.table_entry(fullname))
				f.write(html.table_entry(firstname))
				f.write(html.table_entry(middlename))
				f.write(html.table_entry(surname))
				f.write(html.table_entry(email))
				f.write(html.table_entry(current_role))
				f.write(html.table_entry(current_company))
				f.write('</tr>\n')
		f.write('</tbody>\n')
		f.write('</table>\n')
		f.write(html.h3('Top roles'))
		f.write(html.p('The following table shows the most common roles within the designated organisation.\nRunning this tool again with these top 3 results as keywords will result in more specific data as the api data extraction only pulls 1000 results.'))
		f.write(html.table_head(['Role','Count']))
		for role,count in word_occurrence.items():
			f.write('<tr>\n')
			f.write(html.table_entry(role))
			f.write(html.table_entry(count))
			f.write('</tr>\n')
		f.write('</tbody>\n')
		f.write('</table>\n')
		f.write(html.footer())