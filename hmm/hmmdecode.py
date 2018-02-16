import json;

def readProbFromFile():
    f = open('hmmmodel.txt', 'r');
    stateDiagram=json.loads(f.read());
    print(stateDiagram);

readProbFromFile();