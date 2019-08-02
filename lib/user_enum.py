from lib import logger, naming_scheme, word_occurrence, http
import json, math, re, time

def get_company_profile(cookie,company_id,keyword):
	if keyword == None:
		url='https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=0' % company_id
	else:
		url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&keywords=%s&origin=OTHER&q=guided&start=0" % (company_id,keyword)
	data=http.connect(url,cookie)
	return data.text

def extract_data(data,domain,email_format):
	domain='@'+domain
	collected_data={}
	for d in data['elements'][0]['elements']:
		if 'com.linkedin.voyager.search.SearchProfile' in d['hitInfo'] and d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['headless'] == False:
			try:
				industry = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['industry']
			except:
				industry = ""    

			raw_firstname = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['firstName']
			raw_surname = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['lastName']
			
			profile_url = "https://www.linkedin.com/in/%s" % d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']
			occupation = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['occupation']
			location = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['location']
			try:
				role_data=d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['snippets'][0]['heading']['text']
				try:
					current_role=role_data.split(' at ')[0]
					current_company=role_data.split(' at ')[1]
				except:
					current_company=None,'Error'
					current_role=occupation					
			except:
				try:
					current_company=occupation.split(' at ')[1]
					current_role=occupation.split(' at ')[0]
				except:
					current_company=None,'Error'
					current_role=occupation

			name_data=[raw_firstname,raw_surname]

			name_scheme=naming_scheme.names(name_data)
			firstname=name_scheme[0]
			middlename=name_scheme[1]
			surname=name_scheme[2]
			fullname=name_scheme[3]

			name_data=[firstname,middlename,surname]
			email_scheme=naming_scheme.emails(name_data,email_format,domain)

			email = email_scheme

			try:
				datapoint_1=d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl']
				datapoint_2=d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['artifacts'][2]['fileIdentifyingUrlPathSegment']
				picture=datapoint_1+datapoint_2

				if current_company[0] != None:
					logger.green('Successfully obtained image for %s [%s]' % (logger.GREEN(fullname),logger.GREEN(current_company)))
				else:
					logger.green('Successfully obtained image for %s' % (logger.GREEN(fullname)))
			except:
				if current_company[0] != None:
					logger.red('Unable to obtain image for %s [%s]' % (logger.RED(fullname),logger.RED(current_company)))
				else:
					logger.red('Unable to obtain image for %s' % (logger.RED(fullname)))
				picture = None

			if current_company[0] != None:
				logger.green('Found %s [%s] at %s' % (logger.GREEN(fullname),logger.GREEN(email),logger.GREEN(current_company)))
				userinfo=[profile_url,picture,firstname,middlename,surname,email,current_role,current_company]
			else:
				logger.green('Found %s [%s]' % (logger.GREEN(fullname),logger.GREEN(email)))
				userinfo=[profile_url,picture,firstname,middlename,surname,email,current_role,'Error']

			collected_data[fullname]=userinfo
	return collected_data

def user_data(results,pages,cookie,company_id,domain,email_format):
	# Every page returns a dictionary of data, each dictionary is added to this list.

	users_per_page=[]
	for page in range(0,pages+1):

		if page+1 == 25:
			break

		if results < 40:
			# This method pulls 40 results per page. If the available results is less then 40
			# Set results_per_age to whatever the number is
			results_per_page = results
			results_to_fetch = results
		else:
			# However, if the amount of available results is higher than the per page limit, set the per page limit to the max (40)
			results_per_page = 40

		# Every time this is hit, the start point in the api is incremented. First, it gets 0 - 40, then 40 - 80 and so on.
		# This can be dynamically figured out by multiplying the page number (1) by the results_per_page (40).
		results_to_fetch = results_per_page * page

		# In order to stop this loop from requesting more than is available, and then breaking it, this if statement limits that:
		if results_to_fetch >= results:
			break

		url="https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=%s" % (company_id,results_to_fetch)
		logger.blue('Pulling from page %s' % logger.BLUE(page))
		data=http.connect(url,cookie)
		result = data.text.encode('UTF-8')
		
		try:
			result = json.loads(result)
		except Exception as e:
			x=str(e)
			logger.red(e)
			quit()

		users=extract_data(result,domain,email_format)

		users_per_page.append(users)

	return users_per_page

def run(data,domain,filename,keyword):
	cookie=data[0]
	company_id=data[1]
	email_format=data[2]
	profiles = get_company_profile(cookie,company_id,keyword)
	if profiles == None:
		logger.red('Unable to extract data from LinkedIn')
		quit()
	profiles_data=json.loads(profiles)
	results = profiles_data['elements'][0]['total']
	per_page=40
	pages = int(results / per_page)
	if results < per_page:
		pages=1
	logger.blue('Identified %s page(s)' % logger.BLUE(pages))
	logger.blue('Identified %s result(s)' % logger.BLUE(results))
	quit()

	if pages == 0:
		logger.red('Could not identify pages')
		quit()

	if results > 1000:
		logger.red('This method of enumeration can only extract 1000 users')

	users=user_data(results,pages,cookie,company_id,domain,email_format)
	job_role_count=word_occurrence.count(users)
	logger.write_out(users,domain,job_role_count,filename)
	
	return users