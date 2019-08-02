from lib import logger
import re

def names(name_data):

	# firstname=name_data[0]
	# surname=name_data[1]

	surname_split = name_data[1].split()

	firstname = name_data[0]
	middlename = ""
	surname = name_data[1]

	if len(surname_split) == 1:
		firstname = name_data[0]
		middlename = ''
		surname = surname_split[0]

	elif len(surname_split) == 2:
		firstname = name_data[0]
		middlename = surname_split[0]
		surname = surname_split[1]

	elif len(surname_split) >= 3:
		firstname = name_data[0]
		surname = surname_split[0]

	else:
		firstname = name_data[0]
		surname = ''


	doctor_regex='^([Dd][Rr][.])|([Dd][Rr]\s)'

	if re.match(doctor_regex,firstname):
		firstname=re.sub(doctor_regex,'',firstname)

	firstname = re.sub('[^A-Za-z]+', '', firstname)
	middlename = re.sub('[^A-Za-z]+', '', middlename)
	surname = re.sub('[^A-Za-z]+', '', surname)

	if middlename == '':
		fullname = firstname+' '+surname
	else:
		fullname = firstname+' '+middlename+' '+surname

	return [firstname,middlename,surname,fullname]

def emails(name_data,email_format,domain):
	firstname=name_data[0]
	middlename=name_data[1]
	surname=name_data[2]

	if middlename and surname == '':
		email=firstname+'@'+domain

	if 'firstname.surname' in email_format:
		email=firstname_dot_surname(firstname,surname,domain)
	elif 'f.surname' in email_format:
		email=f_dot_surname(firstname,surname,domain)
	elif 'firstnamesurname' in email_format:
		email=firstnamesurname(firstname,surname,domain)
	elif 'fsurname' in email_format:
		email=fsurname(firstname,surname,domain)

	elif 'surname.firstname' in email_format:
		email=surname_dot_firstname(firstname,surname,domain)
	elif 's.firstname' in email_format:
		email=s_dot_firstname(firstname,surname,domain)
	elif 'surnamefirstname' in email_format:
		email=surnamefirstname(firstname,surname,domain)
	elif 'sfirstname' in email_format:
		email=sfirstname(firstname,surname,domain)
	else:
		logger.red('Unknown email scheme specified.')
		quit()

	return email

def firstname_dot_surname(firstname,surname,domain):
	email=firstname+'.'+surname+domain
	return email.lower()

def f_dot_surname(firstname,surname,domain):
	firstname = firstname[0][0].strip()
	email = firstname+'.'+surname+domain
	return email.lower()

def firstnamesurname(firstname,surname,domain):
	email = firstname+surname+domain
	return email.lower()

def fsurname(firstname,surname,domain):
	firstname = firstname[0][0]
	email = firstname+surname+domain
	return email.lower()


def surname_dot_firstname(firstname,surname,domain):
	email=surname+'.'+firstname+domain
	return email.lower()

def s_dot_firstname(firstname,surname,domain):
	surname = surname[0][0].strip()
	email = surname+'.'+firstname+domain
	return email.lower()

def surnamefirstname(firstname,surname,domain):
	email = surname+firstname+domain
	return email.lower()

def sfirstname(firstname,surname,domain):
	surname = surname[0][0]
	email = surname+firstname+domain
	return email.lower()

