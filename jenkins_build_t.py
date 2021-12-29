import os
for i in range(100):
    print(i)
    f = open("newfile.txt",'w')
    f.write(f"test{str(i)}")
    f.close()
    os.system(f"git add . && git commit -m \"test{str(i)}\" && git push origin master")