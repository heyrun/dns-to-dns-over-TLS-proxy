import ssl
import socket
from configparser import ConfigParser
host = ''
port = 53


config = ConfigParser()
config.sections()
config.read('conf.ini')

server = config['SERVER']
dnsaddr = (server['ipaddr'], int(server['port']))


# Send Request to CloudFlare
def sendRequest(data, addr, server):
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    
    with socket.create_connection(server) as sock:
        with context.wrap_socket(sock, server_hostname=server[0]) as ssock:

            print("TLS connection established with remote server. TLS version: ",ssock.version())
            print("server is: ",server)
            ssock.sendall(data)
            result = ssock.recv(1024)
            print("result in bytes: ",result)

            print("restults n quest",result.decode('utf-8', 'ignore'))
            return (result)

if __name__ == '__main__':
    sockclient  =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockclient.bind((host,port))
    sockclient.listen(1)
    while 1:
    
      try:

          conn, address = sockclient.accept()
        
          with conn:
            print('Local connection established on {}'.format(address))
            data, addr = conn.recvfrom(1024)
            result = sendRequest(data,host,dnsaddr)
            conn.sendall(result)
            conn.shutdown(1)
            conn.close()
      except Exception as e: print(e)
 