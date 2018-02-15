import sys;
from collections import defaultdict;

stateDiagram=defaultdict(dict);
wordMap=defaultdict(dict);
initCountOfTagMap=defaultdict(dict);

def readFile(fileName):
    print("in func"+fileName);
    inputFileObj=open(fileName,encoding="utf8");
    return inputFileObj;
    """ for line in inputFileObj:
        print(line.split(" ")); """

def constructMaps(inputFileObj):
    for line in inputFileObj:
        words=(line.split(" "));
        prev=""; # to keep track of prev node
        for word in words:
            tagWordArray=word.split("/");
            if ( (tagWordArray[1]) not in stateDiagram):
                #print("found");
                #add the entry for word
                stateDiagram[tagWordArray[1]]={};
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

    print("initCountOfTagMap-",initCountOfTagMap);

inputFileObj=readFile(sys.argv[1]);
constructMaps(inputFileObj);

