#!/usr/bin/env python

import re
import httplib, urllib
import xml.etree.ElementTree as ET

bpid = 356464
# === get sra ids ===
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?db=sra&dbfrom=bioproject&id=356464&term=all[filter]
#	https://dataguide.nlm.nih.gov/eutilities/utilities.html#elink
params = urllib.urlencode({'db': 'sra', 'dbfrom': 'bioproject', 'id': bpid, 'term': 'all[filter]'})
conn = httplib.HTTPSConnection("eutils.ncbi.nlm.nih.gov")
conn.request("POST", "/entrez/eutils/elink.fcgi", params)

response = conn.getresponse()
# # response.status and response.reason can be used to check for 200 (response.status) OK (response.reason)
data = response.read()

# parse xml response: get SRA IDs
#       assumes XML is like 2_list_sra_ids_1.pdf
ids = []
root = ET.fromstring(data)
for id in root.findall("./LinkSet/LinkSetDb"):
	if (id.find("LinkName").text == "bioproject_sra_all"):
		for sra in id.findall("./Link/Id"):
        		ids.append(sra.text)
if (len(root.findall("./LinkSet/LinkSetDb"))):
	# === get summaries for these SRAs ===
	# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=sra&id=3543186,3543185,3543183
	#       https://dataguide.nlm.nih.gov/eutilities/utilities.html#esummary
	params = urllib.urlencode({'db': 'sra', 'id': ','.join (ids)})
	conn.request("POST", "/entrez/eutils/esummary.fcgi", params)

	response = conn.getresponse()
	# response.status and response.reason can be used to check for 200 (response.status) OK (response.reason)
	data = response.read()

	# parse xml response: get summaries for these SRAs
	#       assumes XML is like 2_list_sra_ids_2.pdf
	srr = []
	root = ET.fromstring(data)
	for item in root.findall("./DocSum/Item"):
		if (item.attrib['Name'] == 'Runs' and re.match ("<Run acc=", item.text)):
	        	srr.append(item.text.split()[1].replace ('"', '').split('=')[1])
	print srr

conn.close()
