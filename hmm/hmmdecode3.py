import json;
import sys;
from collections import defaultdict;

stateDiagram={};
wordTagMap={};
initProbOfTag={};

def readFile(fileName):
    inputFileObj=open(fileName,encoding="utf8");
    return inputFileObj;

def readProbFromFile():
    f = open('hmmmodel.txt', 'r');
    lines=f.readlines();
    stateDiagram=json.loads(lines[0]);
    wordTagMap=json.loads(lines[1]);
    initProbOfTag=json.loads(lines[2]);
    return stateDiagram,wordTagMap,initProbOfTag;

def tagData(inputFileObj):
    outputFileObj=open('hmmoutput.txt', 'w');
    for line in inputFileObj:
        obs=line.rstrip().split(" ");
        for i in range(len(obs)):
            obs[i]=obs[i].lower();
        backpointer=runViterbi(obs);
        state=backpointer["qf"][obs.__len__()-1];
        for t in range(obs.__len__()-1,-1,-1):
            obs[t] += '/' + state;
            state=backpointer[state][t];
        print(" ".join(obs),file=outputFileObj);
    outputFileObj.close();

def writeToFile():
    f = open("hmmmodel.txt", "a");
    f.write(json.dumps(stateDiagram));
    f.write("\n");

def runViterbi(obs):
    #print(obs);
    n = len((stateDiagram)) + 1;
    viterbi, backpointer =initForViterbi(obs);
    for obsIndex in range(1,len(obs)):
        for state in stateDiagram:
            #calculate max (prev state max value*transtion cost*emission at current state)
            max,maxState=getMax(state,obsIndex,viterbi,obs);
            viterbi[state][obsIndex] = max;
            backpointer[state][obsIndex] = maxState;

    max,maxState=getFinalMax(len(obs)-1,viterbi);
    viterbi["qf"][len(obs)-1]=max;
    backpointer["qf"][len(obs)-1]=maxState;
    print("viterbi-", viterbi);
    print("backPtr-", backpointer);
    return backpointer;


def getFinalMax(finalT,viterbi):
    max = float("-inf");
    maxState = 0;
    for state in stateDiagram:
        currentValue=viterbi[state][finalT];
        if (max < currentValue):
            max = currentValue;
            maxState = state;
    return max,maxState;

def getMax(currentState,obsIndex,viterbi,obs):
    max=float("-inf");
    maxState=0;
    for state in stateDiagram:
        currentValue=viterbi[state][obsIndex-1]*wordTagMap.get(obs[obsIndex]).get(currentState, 0)*stateDiagram[state].get(currentState,0);
        if(max<currentValue):
            max=currentValue;
            maxState=state;
    return max,maxState;

def initForViterbi(obs):
    viterbi = defaultdict(list);
    backpointer = defaultdict(list);
    t = len(obs)
    for state in stateDiagram:
        myList = [0] * t;
        newList = [0] * t;
        viterbi[state] = myList;
        backpointer[state] = newList;
        viterbi[state][0] = initProbOfTag.get(state, 0) * wordTagMap[obs[0]].get(state, 0);
        backpointer[state][0] = 0;
    myList = [0] * t;
    newList = [0] * t;
    viterbi["qf"] = myList;
    backpointer["qf"] = newList;
    return viterbi,backpointer;

stateDiagram,wordTagMap,initProbOfTag=readProbFromFile();
inputFileObj=readFile(sys.argv[1]);
tagData(inputFileObj);
inputFileObj.close();
#print(stateDiagram);
#print(wordTagMap);
#print(initProbOfTag);

