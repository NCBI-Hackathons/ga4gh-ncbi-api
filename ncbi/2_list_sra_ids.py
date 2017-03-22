#!/usr/bin/env python

import re
import httplib, urllib
import xml.etree.ElementTree as ET

bpid = 356464	#bpid = 262923
sras_per_fetch = 100
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
# === get all data for these SRAs ===
sras = {}
while (len(ids)):
	# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id=3543186,3543185,3543183
	#       https://dataguide.nlm.nih.gov/eutilities/utilities.html#efetch
	sra_ids = ids[:sras_per_fetch]
	ids = ids[sras_per_fetch:]
	params = urllib.urlencode({'db': 'sra', 'id': ','.join (sra_ids)})
	conn.request("POST", "/entrez/eutils/efetch.fcgi", params)

	response = conn.getresponse()
	# response.status and response.reason can be used to check for 200 (response.status) OK (response.reason)
	data = response.read()

	# parse xml response: get relevant data for these SRAs
	#       assumes XML is like 2_list_sra_ids_2_with_reference.pdf or 2_list_sra_ids_2_without_reference.pdf
	for child in ET.fromstring(data):
		sra, srr, biosample, assembly = '', '', '', ''
		for pid in child.findall("./SUBMISSION/IDENTIFIERS/PRIMARY_ID"):
			sra = pid.text
		for pid in child.findall("./RUN_SET/RUN/IDENTIFIERS/PRIMARY_ID"):
			srr = pid.text
		for eid in child.findall("./RUN_SET/RUN/Pool/Member/IDENTIFIERS/EXTERNAL_ID"):
			biosample = eid.text
		for node in child.findall("./RUN_SET/RUN"):
			assembly = node.attrib['assembly']
		sras[srr] = [sra, biosample, assembly]

conn.close()
