import json
def addExpected():
    with open("./performance/expectedList1.json") as f:
        data = json.load(f)

    queries = list(data.keys())
    counter = 0
    for i in queries:
        with open("./performance/Expected/"+str(counter)+".json", "w") as f:
            json.dump(data[i], f)
        counter+=1
    
    