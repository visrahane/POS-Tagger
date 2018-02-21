correct=0;
incorrect=0;
line=1;
with open("hmmoutput.txt",encoding="utf8") as textfile1, open("en_dev_tagged.txt",encoding="utf8") as textfile2:
    for x, y in zip(textfile1, textfile2):
        #print (x);
        myLine = x.rstrip().split(" ");
        expectedLine = y.rstrip().split(" ");
        wordNo=1;
        for myWord,expectedWord in zip(myLine,expectedLine):
            myTags = myWord.split("/");
            myTags[0:-1] = ["/".join(myTags[0:-1])];

            expectedTags = expectedWord.split("/");
            expectedTags[0:-1] = ["/".join(expectedTags[0:-1])];

            if(expectedTags[1]!=myTags[1]):
                incorrect+=1;
                print("line-",line,"wordNo-",wordNo,"word:",expectedTags[0],myTags[0],"myTag:",myTags[1],"expectedTag:",expectedTags[1]);
            else:
                correct+=1;
                #print("good");
            wordNo+=1;
        line+=1;
print("Correct:",correct);
print("InCorrect:",incorrect);
print("Total:",correct+incorrect);
print("Accuracy:",correct/(correct+incorrect));