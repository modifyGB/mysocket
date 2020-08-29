import socket
import threading

serveraddr = ('127.0.0.1', 8080)#定义server的ip和地址

def client_thread(client,port):#客户端
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(('127.0.0.1', port))
    client.listen(1)
    while(True):
        clientsocket, address = client.accept()
        print(clientsocket.recv(1024).decode('utf-8'))

if __name__ == "__main__":
    #login指令
    target = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    target.connect(serveraddr)
    id = input('请输入你的用户名: ')
    target.send(('none login '+id).encode('utf-8'))
    port = int(target.recv(1024).decode('utf-8'))
    print('链接成功')
    target.close()
    #启动客户端
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threading.Thread(target=client_thread, args=(client,port)).start()
    #开始发送指令
    while(True):
        put = id+' '+input()
        target = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        target.connect(serveraddr)
        target.send(put.encode('utf-8'))
        callback = target.recv(1024).decode('utf-8')
        if(callback!='success'):
            print(callback)
        target.close()
        if put.split(' ')[1] == 'close':#关闭客户端
            break
    client.close()