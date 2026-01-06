import os
p="/home/yuvaganesh/StegoScope/tmpdir"
for roots,dirs,files in os.walk(p):
    for filename in files:
        print(filename)
