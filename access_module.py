import socket
import json
import sys

class access_page:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def read(self, page):
        s = socket.socket()
        s.connect((self.ip, self.port))
        message = {}
        message['type'] = "read_page"
        message["page_no"] = page
        message = json.dumps(message)
        s.send(message.encode())
        reply = json.loads(s.recv(2048).decode())
        s.close()
        return reply["data"]
    
    def write(self, data, page):
        s = socket.socket()
        s.connect((self.ip, self.port))
        message = {}
        message['type'] = "write_page"
        message["page_no"] = page
        message["data"] = data
        message = json.dumps(message)
        s.send(message.encode())
        reply = json.loads(s.recv(2048).decode())
        s.close()
        return reply
    
    def refresh(self):
        s = socket.socket()
        s.connect((self.ip, self.port))
        message = {}
        message['type'] = "refresh"
        message = json.dumps(message)
        s.send(message.encode())
        s.close()

    def get_details(self):
        s = socket.socket()
        s.connect((self.ip, self.port))
        message = {}
        message['type'] = "get_details"
        message = json.dumps(message)
        s.send(message.encode())
        reply = json.loads(s.recv(2048).decode())
        s.close()
        return reply
    
if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])
    a = access_page(ip, port)
    while True:
        p = int(input("enter page number"))
        c = input("enter read / write / refresh")
        if c == "read":
            print(a.read(p))
        elif c == "write": 
            data = input("enter page data")
            print(a.write(data, p))
        elif c == "refresh":
            a.refresh()