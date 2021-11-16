import ssl
import socket
from configparser import ConfigParser
from threading import Thread

host = ''
port = 53


config = ConfigParser()
config.sections()
config.read('conf.ini')

server = config['SERVER']
dnsaddr = (server['ipaddr'], int(server['port']))

# Handle thread connections 
def handleTcpConnections(conn):
    while 1:
        print("Processing TCP request")
        data, addr = conn.recvfrom(1024) # Receive request data from remote connection
        if not data: 
            break
        result = sendRequest(data,host,dnsaddr)
        conn.sendall(result)
    print("connection closed for {}".format(addr))
    conn.close()
  
# def handleUdpConnections(data):
#     while 1:
#         print("Processing UDP request")
#         print("udp data: {}".format(data))
#         if not data: 
#             break
#         result = sendRequest(data,host,dnsaddr)
#         print("results from UDP query: {}".format(result))
#         #conn.sendall(result)
#     print("UDP connection closed")
    conn.close()


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
    # sockudp  =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # sockudp.bind((host,port))
    

    print("Listening for connections on port {}".format(port))
    while 1:
      try:
        #   udpdata, udpaddr = sockudp.recvfrom(1024) # Listening on UDP port 53
          conn, address = sockclient.accept()       # Listening on TCP port 53
        #   if udpdata:
        #       t = Thread(target=handleUdpConnections, args=(udpdata,))
        #       t.start()
          
          if conn:
              t = Thread(target=handleTcpConnections, args=(conn, ))
              t.start()

        
      except Exception as e: print(e)
    sockclient.close()
 