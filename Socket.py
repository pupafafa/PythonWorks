import socket
def server_program():
    host = '192.168.1.141'
    port = 5000  #  1024 이상으로 해야함.
    print('IP / PORT: ', host,port)
    BUFFER=4096
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    # IPv4,TCP PROTOCOL 사용
    server_socket.bind((host, port))    # bind host address and port together

    server_socket.listen(0) 
    while True: #서버는 항상 열려있어야 함.
        client_sock, client_addr = server_socket.accept()  # connection 받기
        print('%s:%s connected' %client_addr)
        while True:
            recv = client_sock.recv(BUFFER).decode() # client 로부터 메시지 받기
            if not recv:
                client_sock.close()
                break   
            print('[client %s:%s said]:%s' %(client_addr[0], client_addr[1],recv))
            #addr[0]에는 host, addr[1]에는 무슨 값이 잇는지는 모르겠음.
            server_message = 'server has received client message'
            client_sock.send(server_message.encode())
    server_socket.close()
if __name__ == '__main__':
    server_program()
