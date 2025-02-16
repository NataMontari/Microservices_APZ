# Microservices_APZ
Code for all tasks from apz, featuring a simple microservice

Additional tasks: retry, dublication, gRPC protocol

facade_service.py - facade service for client-server communication. Receives get or post requests from the client and manages them (runs on localhost: 8080)

logging_service.py - stores all messages that are snt by facade_service via grpc protocol, sends back all the messages when receives a GET request (runs on localhost: 8081)

messages_service - currently not implemented, sends back "not implemented" message when receives a GET request (runs on localhost: 8082)


logging.proto defines the gRPC service interface for the logging system.

It specifies the available RPC methods and message formats using Protocol Buffers (protobuf).

This file allows automatic generation of client and server code.

the rest of the files - logging_pb2.py and logging_pb2_grc.py where generated using this command:

`python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/messages.proto`

test_requests_get.sh - test file with bash code for sending a GET request

test_requests_post.sh - test file with bash code for sending POST request

Usage:

run all 3 microservices in separate terminals

facade:
![image](https://github.com/user-attachments/assets/d6562ec2-bc79-4ceb-a8fe-5e2b4d9ec16e)

logging:
![image](https://github.com/user-attachments/assets/fcbdc264-bc5e-479c-9b60-9758dfb66754)

messages:
![image](https://github.com/user-attachments/assets/1cddd363-d516-4bff-8f1f-70a5bc10856a)

than run the bash scripts:

first GET request, when logging hash map is empty:
![image](https://github.com/user-attachments/assets/3273f713-b97f-4089-a6a5-c2b0e7d65b4c)

facade service prints:
![image](https://github.com/user-attachments/assets/f1586354-ca70-4c67-af2c-eefd3144e9ab)

messages service prints:
![image](https://github.com/user-attachments/assets/5e427f65-5569-4bd4-a921-be5269eca70a)

A POST request:
![image](https://github.com/user-attachments/assets/5d958e7b-2c87-4ed5-8e3d-fcd9bb843939)

facade service prints:
![image](https://github.com/user-attachments/assets/49c958b8-a16a-4efc-8580-fd07a8cc94fd)

Now we'll do another GET request:
![image](https://github.com/user-attachments/assets/327e4a1f-4197-4890-b1f3-0e5f1a02e6f4)

facade service:
![image](https://github.com/user-attachments/assets/515c0b75-afc6-4994-8a31-37f2f00f648d)

messages service:
![image](https://github.com/user-attachments/assets/716419df-44ca-4a82-a3b8-fc68dd8c4a62)

Now, let's try to send the same message, without changing anything:
![image](https://github.com/user-attachments/assets/58057c7c-6b0b-4083-b6e9-e3fc3b3fef07)

facade service:
![image](https://github.com/user-attachments/assets/43d6a09d-ad1d-474c-8862-e16107f5444f)

Now, a POST service with a different message:
![image](https://github.com/user-attachments/assets/1e91f567-09f8-4ed0-9dec-5e69f07c705c)

facade service:

![image](https://github.com/user-attachments/assets/38b425eb-d32d-4085-897e-c545a0564db5)

Now, let's check with GET:
![image](https://github.com/user-attachments/assets/e36447a3-dffa-45d5-8749-18d31c892c16)


To show that retry mechanism works, we'll shut down the logging server and try and post something there:
![image](https://github.com/user-attachments/assets/4e505d06-bbcf-4bff-80db-ced989b1e25d)

facade service:
![image](https://github.com/user-attachments/assets/f3401a8c-3e90-4342-87f1-defce79bc1d1)

as you can see, facade_service tried to send the message three times, but encountered a 

gRPC UNAVAILABLE error, only then did it state that the POST request failed and returned code 500:

![image](https://github.com/user-attachments/assets/b9b58435-441c-4aec-8863-b41c9972ac84)







