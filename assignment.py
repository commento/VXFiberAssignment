
import sys

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

import requests
import json

url = sys.argv[1]
apikey = sys.argv[2]


r1 = requests.get(url + "/order?q=activated_date.lt:2019-03-01T00:00:00,terminated_date.gte:2019-03-01T00:00:00,,terminated_date:null,object.created:/%5Cd{4}-%5Cd{2}-%5Cd{2}/&api_key=" + apikey + "&per_page=100&page=1")
d1 = json.loads(r1.text)

r2 = requests.get(url + "/order?q=activated_date.lt:2019-03-31T23:59:59,terminated_date.gte:2019-03-31T23:59:59,,terminated_date:null,object.created:/%5Cd{4}-%5Cd{2}-%5Cd{2}/&api_key=" + apikey + "&per_page=100&page=1")
d2 = json.loads(r2.text)


order1 = {}
order2 = {}

for elem in d1["data"]:
	if not elem["object"] in order1:
		order1[elem["object"]] = {"activated_date":elem["activated_date"], "terminated_date":elem["terminated_date"], "service_provider":elem["service_provider"]}
	elif order1[elem["object"]]["service_provider"] != elem["service_provider"]:
		del order1[elem["object"]]

for elem in d2["data"]:
	if not elem["object"] in order2:
		order2[elem["object"]] = {"activated_date":elem["activated_date"], "terminated_date":elem["terminated_date"], "service_provider":elem["service_provider"]}
	elif order2[elem["object"]]["service_provider"] != elem["service_provider"]:
		del order2[elem["object"]]



rcr = len(order1) / len(order2) * 100

print("RCR is: ", rcr, "%")
