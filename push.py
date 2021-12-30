import os

if __name__ == "__main__":    
    os.system(f"git add . && git commit -m \"test\" && git push origin master")
else:
    for i in range(20):
        print(i)
        f = open("newfile.txt",'w')
        f.write(f"test{str(i)}")
        f.close()
        os.system(f"git add . && git commit -m \"test{str(i)}\" && git push origin master")