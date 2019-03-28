from socket import *
import win32api
import os

def on_close(sig):
    try:
        tcpSerSock.close()
    except NameError:
        pass

#获取本机电脑名
myname = gethostname()
#获取本机ip
myaddr = gethostbyname(myname)
print ('myname:',myname)
print ('myaddr:',myaddr)
HOST = myaddr
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)   #创建套接字
win32api.SetConsoleCtrlHandler(on_close, True)
tcpSerSock.bind(ADDR)   #绑定IP和端口
tcpSerSock.listen(3)    #监听端口，最多3人排队

try:
    while True:
        print('等待连接...')
        tcpCliSock, addr = tcpSerSock.accept()    #建立连接
        print('来自'+addr[0]+'的连接，端口号为'+str(addr[1]))
        while True:
            print('等待对方发送文件...')
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                print('连接已断开')
                break
            filename=data.decode('utf-8')
            chooses0=input('对方发送的文件名为：“'+filename+'” 是否接收？(y/n)')
            while True:
                if chooses0=='y'or'n':
                    break
                else:
                    chooses0=input('请输入y(es)/n(o)')
            filepath=input('请输入文件保存位置：> ')
            while True:
                if filepath=='':
                    filepath='.'
                if not os.path.isdir(filepath): #是文件夹 
                    chooses1=input('文件夹不存在，要创建吗？(y/n)')
                    if chooses1=='y':
                        os.makedirs(filepath)
                    elif chooses1=='n':
                        ('请重新输入文件保存位置')
                        filepath=input('> ')
                        continue
                    else:
                        chooses1=input('请输入y(es)/n(o)')
                filepath=filepath.replace('\\','/')
                if not filepath[-1]=='/':
                    filepath=filepath+'/'
                if os.path.isfile(filepath+filename):
                    print('文件“'+filename+'”已存在，您希望？')
                    print('\t1.覆盖')
                    print('\t2.更换保存目录')
                    print('\t3.重命名接收文件')
                    t=input('请输入对应编号：>')
                    while True:
                        if t=='1':
                            flags='break'
                            break
                        elif t=='2':
                            print('请重新输入文件保存位置')
                            filepath=input('> ')
                            flags='continue'
                            break
                        elif t=='3':
                            filename=input('请输入文件名> ')
                            flags='continue'
                            break
                        else:
                            t= input('编号错误，请重新输入')
                    if flags=='break':
                        break
                    elif flags=='continue':
                        continue
            if chooses0=='y':
                tcpCliSock.send('True'.encode("utf-8"))
            elif chooses0=='n':
                tcpCliSock.send('False'.encode("utf-8"))
            print('开始传输')
            with open(filepath+filename,'wb') as f:
                while True:
                    data = tcpCliSock.recv(BUFSIZ)
                    if not data:
                        print('连接已断开')
                        break
                    if data==b'\n\n':
                        print('文件传输完成')
                        break
                    f.write(data)
                    tcpCliSock.send(b'\n\n')
        tcpCliSock.close()
except ConnectionResetError:
    input('远程主机强制下线，按任意键退出')
    exit()

