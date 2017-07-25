import sys, os
headline_list=[]
print("[=] Beginning conversion...")
f=open('data/Combined_News_DJIA.csv','r')
for line in f.readlines()[1:]:
    try:
        pieces=line.split(',')
        label=pieces[1]
        headlines=pieces[2:]
        for headline in headlines:
            headline_list.append([headline[2:],label])
    except:
        pass
f.close()
f=open('data/train/headlines.csv','w')
for headline, label in headline_list:
    f.write(headline+","+label+"\n")
f.close()

print("[+] Finished converting")