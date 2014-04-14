import io
cntlin = 0
ofile = open('train.tsv', 'r')
fln = ofile.readlines()
f1 = open('train_0.tsv', 'w')
f2 = open('train_1.tsv', 'w')
f3 = open('train_2.tsv', 'w')
f4 = open('train_3.tsv', 'w')
f5 = open('train_4.tsv', 'w')
prev = -1
j = 0
while cntlin < len(fln):
    ln = fln[cntlin].split("\t")
    j = int(ln[1].strip("'"))
    if j != prev:
        i = int(ln[3].strip("'"))
        if i == 0:
            f1.write(ln[2]+"\n")
        elif i == 1:
            f2.write(ln[2]+"\n")
        elif i == 2:
            f3.write(ln[2]+"\n")
        elif i == 3:
            f4.write(ln[2]+"\n")
        elif i == 4:
            f5.write(ln[2]+"\n")
        prev = j
    cntlin += 1
