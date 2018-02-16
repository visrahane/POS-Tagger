import sys;
from collections import defaultdict;
import json;
import numpy as np;

stateDiagram=defaultdict(dict);
wordTagMap=defaultdict(dict);
tagMap={};
tagMap=defaultdict(lambda:0, tagMap);
initCountOfTagMap=defaultdict(dict);

def readFile(fileName):
    print("in func"+fileName);
    inputFileObj=open(fileName,encoding="utf8");
    return inputFileObj;
    """ for line in inputFileObj:
        print(line.split(" ")); """

def saveToFile():
    f = open("hmmmodel.txt", "a");
    f.write(json.dumps(stateDiagram));
    f.close()

def calculateTransProbability():
    #iterate over stateDiagram and update edges to have transition prob
    for vertex1,vertices in stateDiagram.items():
        totalCount=sum(vertices.values());
        for vertex2,edgeCount in vertices.items():
            edgeCount=edgeCount/totalCount;
            vertices[vertex2]=edgeCount;

def calculateEmissionProbability():
    for word,innerTagMap in wordTagMap.items():
        for tag,tagCnt in innerTagMap.items():
            tagCnt=tagCnt/tagMap[tag];
            innerTagMap[tag]=tagCnt;

def calculateInitialProbability():
    totalCount=sum(initCountOfTagMap.values());
    for node in initCountOfTagMap:
        initCountOfTagMap[node]=initCountOfTagMap[node]/totalCount;

def constructMaps(inputFileObj):
    for line in inputFileObj:
        words=(line.split(" "));
        prev=""; # to keep track of prev node
        for word in words:
            tagWordArray=word.split("/");
            tagWordArray[0]=tagWordArray[0].lower();
            tagMap[tagWordArray[1]]+=1;
            if ( (tagWordArray[1]) not in stateDiagram):
                #add the entry for tag
                stateDiagram[tagWordArray[1]]={};
                #handle word and its mapping
            if(tagWordArray[0] in wordTagMap):
                if (tagWordArray[1] in wordTagMap[tagWordArray[0]]):
                    wordTagMap[tagWordArray[0]][tagWordArray[1]] +=1 ;
                else:
                    wordTagMap[tagWordArray[0]][tagWordArray[1]] = 1;
            else:
                # add the entry for word
                wordTagMap[tagWordArray[0]][tagWordArray[1]]=1;
            if(prev==""): # first tag of the line
                if ((tagWordArray[1]) in initCountOfTagMap):
                    # get the key and increment its count;
                    initCountOfTagMap[tagWordArray[1]]=initCountOfTagMap[tagWordArray[1]]+1;
                else:
                    #create new entry with count=1
                    initCountOfTagMap[tagWordArray[1]]=1;
            else:
                #create an edge going from prev to this tag and increase the count of edge if already an edge
                #or create an edge with count 1;
                # if found add1 to the value
                if ((tagWordArray[1]) in stateDiagram[prev]):
                    stateDiagram[prev][tagWordArray[1]]+=1;
                else:
                    stateDiagram[prev][tagWordArray[1]]=1;
            prev=tagWordArray[1];


        prev="";



inputFileObj=readFile(sys.argv[1]);
constructMaps(inputFileObj);
calculateTransProbability();
#calculateEmissionProbability();

print("stateDiagram-", stateDiagram);
#print("wordTagMap-", wordTagMap);
calculateEmissionProbability();
calculateInitialProbability();
print("probWordTagMap-", wordTagMap);
print("initCountOfTagMap-",initCountOfTagMap);
#print("tagMap-", tagMap);
saveToFile();
