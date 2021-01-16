import sys
import requests
import json


# function to convert orders to a dictionary of objects
# if an object is present twice it is considered the most recent order
def convertOrdersToObjects(d):
    objects = {}
    for elem in d["data"]:
        if elem["object"] not in objects:
            objects[elem["object"]] = {
                "activated_date": elem["activated_date"], 
                "terminated_date": elem["terminated_date"], 
                "service_provider": elem["service_provider"]
            }
        elif objects[elem["object"]]["service_provider"] != elem["service_provider"]:
            if objects[elem["object"]]["activated_date"] < elem["activated_date"]:
                objects[elem["object"]]["service_provider"] = elem["service_provider"]
                objects[elem["object"]]["activated_date"] = elem["activated_date"]
                objects[elem["object"]]["terminated_date"] = elem["terminated_date"]
    return objects


# first arg is the url, second arg is the apikey
url = sys.argv[1]
apikey = sys.argv[2]


r1 = requests.get(url + "/order?q=activated_date.lt:2019-03-01T00:00:00,terminated_date.gte:2019-03-01T00:00:00,,terminated_date:null,object.created:/%5Cd{4}-%5Cd{2}-%5Cd{2}/&api_key=" + apikey + "&per_page=100&page=1")
d1 = json.loads(r1.text)

r2 = requests.get(url + "/order?q=activated_date.lt:2019-03-31T23:59:59,terminated_date.gte:2019-03-31T23:59:59,,terminated_date:null,object.created:/%5Cd{4}-%5Cd{2}-%5Cd{2}/&api_key=" + apikey + "&per_page=100&page=1")
d2 = json.loads(r2.text)


objectsStart = {}
objectsEnd = {}
missingObjs = 0


objectsStart = convertOrdersToObjects(d1)
objectsEnd = convertOrdersToObjects(d2)


for objectId in objectsStart.keys():
    # At the end of the period, it’s no more part of the “active objects”.
    if objectId not in objectsEnd.keys():
        missingObjs += 1
    # At the end of the period, it’s still active, but has a different service provider.
    elif objectsEnd[objectId]["service_provider"] != objectsStart[objectId]["service_provider"]:
        missingObjs += 1


# The churn rate it’s (missing active objects / total active objects at beginning) * 100
rcr = missingObjs / len(objectsStart) * 100

print("RCR is: ", rcr, "%")
