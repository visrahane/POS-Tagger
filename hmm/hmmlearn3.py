import sys;
from collections import defaultdict;
import json;


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
    f = open("hmmmodel.txt", "w");
    f.write(json.dumps(stateDiagram));
    f.write("\n");
    f.write(json.dumps(wordTagMap))
    f.write("\n");
    f.write(json.dumps(initCountOfTagMap));
    f.close()

def calculateTransProbability():
    #iterate over stateDiagram and update edges to have transition prob
    """
    for vertex1,vertices in stateDiagram.items():
        totalEdgeCount=sum(vertices.values());
        for vertex2,edgeCount in vertices.items():
            edgeCount=(edgeCount)/totalEdgeCount;
            vertices[vertex2]=edgeCount;

    """
    for key1 in stateDiagram:
        totalEdgeCount = sum(stateDiagram[key1].values());
        for key2 in stateDiagram:
            if(stateDiagram[key1].__contains__(key2)):
                stateDiagram[key1][key2]= ((stateDiagram[key1][key2] + 0.5) / (totalEdgeCount+len(stateDiagram)/2));
            else:
                stateDiagram[key1][key2]=0.5/(totalEdgeCount+len(stateDiagram)/2);

def calculateEmissionProbability():
    """
    for word,innerTagMap in wordTagMap.items():
        for tag,tagCnt in innerTagMap.items():
            tagCnt=tagCnt/tagMap[tag];
            innerTagMap[tag]=tagCnt;
    """
    for word, innerTagMap in wordTagMap.items():
        for tag, tagCnt in innerTagMap.items():
            tagCnt = tagCnt/tagMap[tag];
            innerTagMap[tag] = tagCnt;

    for tag in stateDiagram:
        wordTagMap["unknown"][tag]=(tagMap[tag]/sum(tagMap.values()));

def calculateInitialProbability():
    totalCount=sum(initCountOfTagMap.values());
    totalKnownTags=len(initCountOfTagMap);
    totalKnowTagCnt=0;
    for node in initCountOfTagMap:
        initCountOfTagMap[node]=(initCountOfTagMap[node]+0.5)/(totalCount+len(stateDiagram)/2);
        totalKnowTagCnt+=tagMap[node];

    totalUnknowTagCnt=sum(tagMap.values())-totalKnowTagCnt;
    #print("shit",totalUnknowTagCnt);
    for node in stateDiagram:
        if(node not in initCountOfTagMap):
            initCountOfTagMap[node]=(tagMap[node]/totalUnknowTagCnt * (len(stateDiagram)-totalKnownTags)/2)/(totalCount+len(stateDiagram)/2);

def constructMaps(inputFileObj):
    for line in inputFileObj:
        words=(line.rstrip().split(" "));
        prev=""; # to keep track of prev node
        for word in words:
            tagWordArray=word.split("/");
            #if slash in words
            tagWordArray[0:-1]= ["/".join(tagWordArray[0:-1])];
            tagWordArray[0]= tagWordArray[0].lower();
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

print("tagMap-", tagMap);
saveToFile();

