with open ("/home/yuvaganesh/StegoScope/new.txt","r") as file:
    for line in f:
        l=line.strip()
        n=int(l)
        n+=1
        print(n)

