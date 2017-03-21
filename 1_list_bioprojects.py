#!/usr/bin/env python

import httplib, urllib
import xml.etree.ElementTree as ET

page_size = 100
page_token = 0
# === get bioproject ids ===
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=bioproject&term=all[filter]&retmax=100&retstart=0
#	https://dataguide.nlm.nih.gov/eutilities/utilities.html#esearch
#	retmax (optional): Total number of unique identifiers (UIDs) from the retrieved set to be shown in the output (default=20). Increasing retmax allows more of the retrieved UIDs to be included in the output, up to a maximum of 100,000 UIDs. If you need to retrieve more than 100,000 UIDs, you can submit multiple ESearch requests, and increase the retstart parameter each time.
#	retstart (optional): Setting this parameter helps limit which of the unique identifiers (UIDs) in the results set will be shown in the output, as it determines whether the output begins at the first retrieved UID, or with a UID that is later in the results set. For example, if retstart is set to 10, the first ten UIDs in the results set will be skipped, and the output will begin with the eleventh UID. The default of this parameter is 0, corresponding to the first record in the entire set.
params = urllib.urlencode({'db': 'bioproject', 'term': 'all[filter]', 'retmax': page_size, 'retstart': page_token * page_size})
conn = httplib.HTTPSConnection("eutils.ncbi.nlm.nih.gov")
conn.request("POST", "/entrez/eutils/esearch.fcgi", params)

response = conn.getresponse()
# response.status and response.reason can be used to check for 200 (response.status) OK (response.reason)
data = response.read()

# parse xml response: get BioProject IDs
#	assumes XML is like 1_list_bioprojects_1.pdf
ids = []
root = ET.fromstring(data)
for id in root.findall("./IdList/Id"):
	ids.append(id.text)

# === get summaries for these bioprojects ===
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=379763,379762
#	https://dataguide.nlm.nih.gov/eutilities/utilities.html#esummary
params = urllib.urlencode({'db': 'bioproject', 'id': ','.join (ids)})
conn.request("POST", "/entrez/eutils/esummary.fcgi", params)

response = conn.getresponse()
# response.status and response.reason can be used to check for 200 (response.status) OK (response.reason)
data = response.read()

# parse xml response: get summaries for these BioProject IDs
#	assumes XML is like 1_list_bioprojects_2.pdf
root = ET.fromstring(data)
for ds in root.findall("./DocumentSummarySet/DocumentSummary"):
	uid = ds.find('Project_Id').text
	bpid = ds.find('Project_Acc').text		# id
	title = ds.find('Project_Title').text		# name
	desc = ds.find('Project_Description').text	# description
	print '%s\t%s\t%s\t%s' % (uid, bpid, title, desc)
	# UnicodeEncodeError: 'ascii' codec can't encode character u'\xe0' in position 583: ordinal not in range(128)

conn.close()
