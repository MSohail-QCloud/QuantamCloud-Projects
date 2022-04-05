

fil="orderfile.txt"

f = open(fil, "r")
for l in f:
    if len(l)>2:
        lst=l.split(':')
        print(lst[0])
        print(lst[2])