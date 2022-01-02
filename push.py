import os
from deploy import get_now
if __name__ == "__main__":    
    f = open("newfile.txt",'w')
    f.write(f"test{get_now()}")
    f.close()
    os.system(f"git --global config user.name farrar142")
    os.system(f"git --global config user.email gksdjf1690@gmail.com")
    os.system(f"git add . && git commit -m \"test\" && git push origin master")
else:
    for i in range(20):
        print(i)
        f = open("newfile.txt",'w')
        f.write(f"test{str(i)}")
        f.close()
        os.system(f"git add . && git commit -m \"test{str(i)}\" && git push origin master")