import json;


def readProbFromFile():
    f = open('hmmmodel.txt', 'r');
    lines=f.readlines();
    stateDiagram=json.loads(lines[0]);
    wordTagMap=json.loads(lines[1]);
    initProbOfTag=json.loads(lines[2]);
    print(stateDiagram);
    print(wordTagMap);
    print(initProbOfTag);

readProbFromFile();