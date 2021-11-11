# N26 SRE Challenge
## DNS to DNS-over-TLS proxy SRE

Regular DNS requests are sent unencrypted. This means that a potential hacker can see the resources you/your applications are trying to access. This can definitely pose a potential risk to the business. 

Some DNS providers (such as Cloudflare) offer a ​DNS-over-TLS feature that could enhance privacy by encrypting our DNS queries on the transport layer by adding TLS encryption over the packets being sent.

For applications that do not handle DNS-over-TLS by default, this application is created to serve as a proxy that receives DNS requests via TCP port 53 as plaintext connection and forward the request to a DNS resolver that supports DNS-over_TLS DoT over an encrypted channel. 

This application currently send the requests to CloudFlare (1.1.1.1) on port 853

## Installation
### As a Container
-  Create a docker image from the DockerFile included in this folder by running ``` docker build --tag dns_proxy . ```
-  Create a bridge network by running ``` docker network create  ntest ```
-  Run the docker image by running the following command: ``` docker run --publish 53:53  --net ntest dns_proxy ```
-  you can test the service by running  `dig @127.0.0.1 yahoo.com +tcp`

### Run locally
-  Change directory to the root folder on the terminal
-  Run sudo python3 index.py  # The sudo is required to use port 53
-  Launch another terminal and run a test `dig @127.0.0.1 yahoo.com +tcp`

## POSSIBLE SECURITY CONCERNS 
- The system's trusted CA certificate was used to establish the connection with the remote server, hence, no certificate was provided for the connection. 
- TLS v1.3 is established during the test, which is convinient for optimal security.  The application is restricted to use a minimum version of TLSv1.3 .
- This application currently listen on TCP port 53. zone transfer is usually done via TCP port 53
-  Applications and any internal firewall have to allow TCP port 53 to enable communication.
-  

## INTEGRATION
- The application currently runs as a docker container, to integrate it into a microservice environment running on kubernetes, for example, there will be a need to expose the container via a service resource. All applications that requirements the need of the Dns_proxy service and send requests to the service IP address. 
-  Services that needs to reach the same network as the dns_proxy. 

## POSSIBLE IMPROVEMENTS
- The app can be improved to used mulithreading processes to handle concurrent requests from multiple clients at a time. 
- Have all new requests cached, saved and loaded to memory for fast response to requests. 
- Have the application send requests to more than one resolver that supports DoT. 
- Enable app to listen on both TCP and UDP port 53 
