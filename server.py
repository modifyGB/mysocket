import socket
import threading

serveraddr = ('0.0.0.0', 8080)#定义server的ip和地址

class Server:#server类
    def __init__(self):
        self.user={}
        self.addr={}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(serveraddr)
        self.server.listen(128)

    def add_user(self,name,addr):
        self.user[name]=addr
        self.addr[addr[0]+str(addr[1])]=name

    def get_user(self,name):
        return self.user[name]

def main_thread(server,client,address):#主线程函数
    datalist = client.recv(1024).decode('utf-8').split(' ', 3)
    if datalist[1] == 'login':#登录
        server.add_user(datalist[2],address)
        client.send(str(address[1]).encode('utf-8'))
        print('用户'+datalist[2]+'已录入',server.user[datalist[2]])
    elif (datalist[1] == 'send' and len(datalist) == 4):#发送
        if(datalist[2] in server.user.keys()):
            target = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            target.connect(server.get_user(datalist[2]))
            target.send(('用户'+datalist[0]+'发来一条信息:'+datalist[3]).encode('utf-8'))
            client.send('success'.encode('utf-8'))
            print('用户'+datalist[0]+'给用户'+datalist[2]+'发送了一条信息:'+datalist[3])
            target.close()
        else:
            client.send(('用户'+datalist[2]+'不存在').encode('utf-8'))
            print('用户'+datalist[2]+'不存在')
    elif datalist[1] == 'close':#退出
        print('已删除用户'+datalist[0])
        client.send('success'.encode('utf-8'))
        del server.user[datalist[0]]
    else:#其他
        client.send('格式有误'.encode('utf-8'))
    client.close()

def server_thread(server):#服务端
    print('服务器已开启')
    while(True):
        client, address = server.server.accept()
        threading.Thread(target=main_thread, args=(server,client,address)).start()

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server_thread, args=(server,)).start()
    while(True):
        put = input()
        if(put=='close'):
            server.close()
            break
        else:
            print('无效指令')