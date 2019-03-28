from socket import *
import os

try:
    HOST = input('>请输入目标host ip：')
    while True:
        PORT = 9999
        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        try:
            tcpCliSock.connect(ADDR)
            print('>已连接')
            while True:
                print('请输入要发送的文件路径，为空则断开连接')
                filepath = input('> ')
                if not filepath:
                    print('断开链接')
                    tcpCliSock.close()
                    break
                if not os.path.isfile(filepath):
                    print('文件不存在')
                    continue
                tcpCliSock.send(os.path.basename(filepath).encode("utf-8"))
                print('等待对方确认传输')
                data = tcpCliSock.recv(BUFSIZ)
                if data=='False':
                    print('对方拒绝了文件传输')
                    continue
                print('开始传输')
                with open(filepath,'rb') as f:
                    while True:
                        data=f.read(BUFSIZ)
                        if data==b'':
                            data=b'\n\n'
                            tcpCliSock.send(data)
                            print('文件传输完成')
                            break
                        tcpCliSock.send(data)
                        rec = tcpCliSock.recv(BUFSIZ)
                        if rec==b'\n\n':
                            continue
        except gaierror:
            print('输入主机ip错误')
        except ConnectionRefusedError:
            print('输入主机ip错误')
        recon=input('>请重新输入目标host ip,输入"q"退出：')
        if recon=="q" :
            break
        else:
            HOST =recon
except ConnectionResetError:
    input('远程主机强制下线，按任意键退出')
    exit()
