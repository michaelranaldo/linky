from collections import Counter

def count(data):
	counts = {}
	role_data = {}
	for d in data:
		for k,v in d.items():
			current_role=v[6]
			current_company=v[7]
			if current_role in counts:
				counts[current_role] += 1
			else:
				counts[current_role] = 1
	
	coll_obj = Counter(counts)

	try:
		most_common_5 = coll_obj.most_common(5)

		for role in most_common_5:
			role_name=role[0]
			role_count=role[1]
			role_data[role_name]=role_count
	except:
		logger.red('Couldnt identify common role types')

	return role_data