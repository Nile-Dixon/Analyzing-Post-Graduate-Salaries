import pandas as pd

#READ IN STEM DESIGNATED DEGREES FOR CIP CODES NOT IN THE FAMILY OF 14, 26, 27, AND 40
stem_designated_cip_codes = []
stem_degrees = open("data/stem_designated.txt")
for degree in stem_degrees:
	string_parts = degree.split(" ")
	stem_designated_cip_codes.append(int(string_parts[1].replace(".","")[0:4]))

#LOAD DATA 
colleges = pd.read_csv("data/colleges.csv", 
	usecols = ['UNITID','CONTROL','REGION','LOCALE'])
salaries = pd.read_csv("data/salaries.csv",
	usecols = ['UNITID','CIPCODE','CIPDESC','CREDLEV','MD_EARN_WNE'])

#ADD DERIVATIVE VARIABLES
salaries['STEM_DESIGNATION'] =  [0 for x in range(len(salaries))]
salaries['GEOGRAPHY_TYPE'] = ['UNKNOWN' for x in range(len(salaries))]
salaries['GEOGRAPHY_SIZE'] = ['UNKNOWN' for x in range(len(salaries))]

#SUBSET SALARY DATA 
salaries = salaries[salaries['CREDLEV'].isin(['2','3','5','6'])]
salaries = salaries[salaries['MD_EARN_WNE'] != "PrivacySuppressed"]
salaries = salaries[salaries['UNITID'].notnull()]

#LEFT JOIN COLLEGES ON SALARIES
salaries = pd.merge(salaries, colleges, how = 'left', on = 'UNITID', suffixes = ('_x','_y'))

#ADD STEM DESIGNATION TO EACH POST-SECONDARY SALARY 
for index, row in salaries.iterrows():
	
	#FIND STEM_DESIGNATION DERIVATIVE VARIABLE
	cip_code = row['CIPCODE']
	if cip_code >= 1400 and cip_code < 1500:
		salaries.loc[index, 'STEM_DESIGNATION'] = 1
	elif cip_code >= 2600 and cip_code < 2800:
		salaries.loc[index, 'STEM_DESIGNATION'] = 1
	elif cip_code in stem_designated_cip_codes:
		salaries.loc[index, 'STEM_DESIGNATION'] = 1

	#FIND GEOGRAPHY_TYPE DERIVATIVE VARIABLE
	locale_value = row['LOCALE']
	if locale_value in [11,12,13]:
		salaries.loc[index, 'GEOGRAPHY_TYPE'] = 'CITY'
	elif locale_value in [21,22,23]:
		salaries.loc[index, 'GEOGRAPHY_TYPE'] = 'SUBURB'
	elif locale_value in [31,32,33]:
		salaries.loc[index, 'GEOGRAPHY_TYPE'] = 'TOWN'
	elif locale_value in [41,42,43]:
		salaries.loc[index, 'GEOGRAPHY_TYPE'] = 'RURAL'

	#FIND GEOGRAPHY_SIZE DERIVATIVE VARIABLE
	if locale_value in [11,21,31,41]:
		salaries.loc[index, 'GEOGRAPHY_SIZE'] = 'LARGE'
	elif locale_value in [12,22,32,42]:
		salaries.loc[index, 'GEOGRAPHY_SIZE'] = 'MEDIUM'
	elif locale_value in [13,23,33,43]:
		salaries.loc[index, 'GEOGRAPHY_SIZE'] = 'SMALL'

