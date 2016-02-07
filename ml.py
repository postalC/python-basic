def getClassify(input):
    print("I got " + input);
    data = {
        'input' : input
    }
    return data;


from flask import json
def getClassifies(input):
    print("I got " + input);
    jsonInput= json.loads(input)
    data = {
        'input' : jsonInput['message']
    }
    return data;