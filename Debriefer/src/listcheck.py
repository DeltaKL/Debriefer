mylist = [('124', 10), ('second', 20) , ('thirdd', 30), ('last',40)]



ml=list(enumerate(mylist))
revlist=reversed(ml)

print(ml)
print(list(revlist))

mstr="thirdd"
for i,k in list(enumerate(mylist)):
        if mstr in k:
            print(k)
            print(i)
            myFileName = mylist[i-1][0]

            print(myFileName)
