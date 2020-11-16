import json
def processRaw():
    with open('./performance/groundTruth2.json', encoding='utf-8') as f:
        data = json.load(f)
    
    #print(data)
    print(type(data))
    queries = list(data.keys())
    print(queries)
    URLs = {}
    #print(data)

    for ele in queries:
        retVal = data[ele]["result"]
        URLs[ele] = []
        for i in retVal:
            URLs[ele].append(i["_source"]["ï»¿URL"])
    #print(URLs)
    
    with open("./performance/expectedList1.json", "w") as fp:
        json.dump(URLs, fp)
