import os
import locale
import subprocess
import time
import socket
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
                # 실행중이면 ports값도 얻어내옴
                _result.append(get_ports_from_strings(_result, words))
                # 인스턴스 ip 주소값도 알아내옴.
                _result.append(get_logs(
                    "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+words[0]).strip("'"))
            except:
                pass
            result.append(_result)
    else:
        print("No Containers")
    return result
def get_specfic_container(cmd):
    a = get_docker_containers()
    for i in a:
        if i[0] == cmd:
            return i
    return []
def connection_checker(sock,server_address):
    for i in range(10):
        time.sleep(1)
        if sock.connect(server_address):
            sock.close()
            return print("success")
if __name__ == "__main__":
    prev_con = get_specfic_container("web")
    # os.system("docker pull python:3")
    # os.system("docker build -t python:test .")
    # os.system("docker run -d -p 8001:8000 python:test gunicorn --bind 0:8001 base.wsgi")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f"{prev_con[-1]}, {prev_con[-2]}")
    server_address = ("localhost",int(prev_con[-2]))
    connection_checker(sock,server_address)