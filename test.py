import os,sys
import locale
import subprocess
import time
import socket
from datetime import datetime
def get_logs(cmd):
    os_encoding = locale.getpreferredencoding()
    #print("System Encdoing :: ", os_encoding)
    if os_encoding.upper() == 'cp949'.upper():  # Windows
        return subprocess.Popen(
            cmd, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    elif os_encoding.upper() == 'UTF-8'.upper():  # Mac&Linux
        return os.popen(cmd).read()
    else:
        print("None matched")
        exit()
def get_ports_from_strings(_result, words):
    try:
        tcp = words[-2].split("->")
        _tcp = ""
        for strings in tcp:
            if "tcp" in strings:
                _tcp = strings
                break
        return _tcp.split("/")[0]
    except:
        return ""        
def get_docker_containers():
    cmd = "docker ps -a"
    logs = get_logs(cmd).split("\n")
    column = logs.pop(0)
    result = []
    if logs:
        for line in logs:
            words = line.split("  ")

            while '' in words:
                words.remove('')

            for i in range(len(words)):
                words[i] = words[i].strip().strip()
            try:
                status = words[4].strip().split(" ")[0]
                # print(f"C Name :: {words[-1]}, C ID :: {words[0]}, Img Name :: {words[1]} , Status :: {status}")
                _result = [words[-1], words[0], words[1], status]
                # get ports
                _result.append(get_ports_from_strings(_result, words))
                # get ip
                _result.append(get_logs(
                    "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+words[0]).strip("'").strip("\n"))
            except:
                pass
            result.append(_result)
    else:
        print("No Containers")
    return result
def get_specific_container(cmd):
    a = get_docker_containers()
    for i in a:
        if i[0] == cmd:
            return i
    return []
def get_now():
    now=datetime.now()
    nows = [now.year,now.month,now.day,now.hour,now.minute,now.second]
    nowtime = ""
    for i in nows:
        nowtime = nowtime + str(i).zfill(2)
    return nowtime
def connection_checker(test_con):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(0.5)
    myip = socket.gethostbyname(socket.gethostname())
    print(test_con.ip)
    print(test_con.port)
    server_address = (test_con.ip,int(test_con.port))
    # server_address = (myip,8002)
    for i in range(10):
        time.sleep(1)
        try:
            sock.connect(server_address)            
            sock.close()
            print("Connection Succeed")
            return True
        except:
            print(f"{i+1} failed")
    sock.close()
    print("Connection Failed")
    return False
class Container:
    def __init__(self,con):
        self.container_name = con[0]
        self.image_name = con[2]
        self.ip = con[-1]
        self.port = con[-2]
#
if __name__ == "__main__":
    now = get_now()
    init = False
    try:
        now_con = Container(get_specific_container("now_con"))
    except:
        print("No Current Container.")
        init = True
    os.system("docker pull python:3")
    os.system(f"docker build -t python:{now} .")
    os.system(f"docker run -d -p 8001:8001 --name test_con python:{now} gunicorn --bind 0:8001 base.wsgi")
    con_info = get_specific_container("test_con")
    print(con_info)
    test_con = Container(con_info)
    if connection_checker(test_con) == False:
        os.system(f"docker rm -f test_con")
        os.system(f"docker rmi -f python:{now}")
        print("failed")
        sys.stderr.write("Build Failed")
        exit()
    else:
        os.system(f"docker rm -f test_con")
        if init == False:
            os.system(f"docker rm -f now_con")
        os.system(f"docker run -d -p 8000:8000 --name now_con python:{now} gunicorn --bind 0:8000 base.wsgi")
        if init == False:
            os.system(f"docker rmi -f {now_con.image_name}")
        #messagr success#