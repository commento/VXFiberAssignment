
import sys
import requests
import json

url = sys.argv[1]
apikey = sys.argv[2]


r1 = requests.get(url + "/order?q=activated_date.lt:2019-03-01T00:00:00,terminated_date.gte:2019-03-01T00:00:00,,terminated_date:null,object.created:/%5Cd{4}-%5Cd{2}-%5Cd{2}/&api_key=" + apikey + "&per_page=100&page=1")
d1 = json.loads(r1.text)

r2 = requests.get(url + "/order?q=activated_date.lt:2019-03-31T23:59:59,terminated_date.gte:2019-03-31T23:59:59,,terminated_date:null,object.created:/%5Cd{4}-%5Cd{2}-%5Cd{2}/&api_key=" + apikey + "&per_page=100&page=1")
d2 = json.loads(r2.text)


orders1 = {}
orders2 = {}

missingObjs = 0

for elem in d1["data"]:
	if elem["object"] not in orders1:
		orders1[elem["object"]] = {"activated_date":elem["activated_date"], "terminated_date":elem["terminated_date"], "service_provider":elem["service_provider"]}

for elem in d2["data"]:
	if elem["object"] not in orders2:
		orders2[elem["object"]] = {"activated_date":elem["activated_date"], "terminated_date":elem["terminated_date"], "service_provider":elem["service_provider"]}
	elif orders2[elem["object"]]["service_provider"] != elem["service_provider"]:
		del orders2[elem["object"]]


for obj in orders1.keys():
	if obj not in orders2.keys():
		missingObjs += 1


rcr = missingObjs / len(orders1) * 100

print("RCR is: ", rcr, "%")
