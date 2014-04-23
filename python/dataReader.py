import random

with open("data/trainML.tsv",'r') as ofile:
    cntlin = 0
    i = 0
    prev = -1

    trainLn = []
    testLn = []
    uni = []
    trainScore = [0, 0, 0, 0, 0]
    testScore = [0, 0, 0, 0, 0]

    train = open('data/train_n.tsv', 'w')
    test = open('data/test_n.tsv', 'w')
    metaData = open('data/metadata_n.txt', 'w')

    rndln = random.sample(range(1, 8544), 6835)
    fln = ofile.readlines()
    while cntlin < len(fln):
        ln = fln[cntlin].split("\t")
        i = int(ln[1].strip("'"))
        uni.append(i)
        if i in rndln:
            train.write(fln[cntlin])
            trainLn.append(i)
            if i != prev:
                trainScore[int(ln[3].strip("'"))] += 1
        else:
            test.write(fln[cntlin])
            testLn.append(i)
            if i != prev:
                testScore[int(ln[3].strip("'"))] += 1
        prev = i
        cntlin += 1


    i = 0
    j = 0
    metaData.write("Training Data\n ")
    trainLn = list(set(trainLn))
    numtrain = len(trainLn)
    trainLn = ",".join([str(i) for i in trainLn])
    metaData.write(trainLn+"\n")
    trainScore = ",".join([str(j) for j in trainScore])
    metaData.write(" Score Distribution [1,2,3,4,5] = ["+trainScore+"]\n")
    metaData.write(" Total "+str(numtrain)+"\n\n")

    i = 0
    j = 0
    metaData.write("Testing Data\n ")
    testLn = list(set(testLn))
    numtest = len(testLn)
    testLn = ",".join([str(i) for i in testLn])
    metaData.write(testLn+"\n")
    testScore = ",".join([str(j) for j in testScore])
    metaData.write(" Score Distribution [1,2,3,4,5] = ["+testScore+"]\n")
    metaData.write(" Total "+str(numtest)+"\n\n")

    metaData.write("Total sentences "+str(len(list(set(uni)))))
    print "Number of unique sentences ",len(list(set(uni)))
    print "----------------------------Data Divided------------------------------------"