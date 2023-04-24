import socket
import json
import sys
class memory_manager:
    
    #printing all the config details for a memory manager
    def print_self(self):
        print("......................................")
        print("id : ", self.id)
        print("ip : ", self.ip)
        print("port : ", self.port)
        print("totlal nodes : ", self.total_nodes)
        print("my pages : ", self.my_pages)
        print("total_pages : ", self.total_pages)
        print("page addresses")
        """ for i, j  in self.page_addresses.items():
            print(i, j) """
        print(self.page_addresses)
        print("page content")
        """  for i, j  in self.pages.items():
            print(i, j) """
        print(self.pages)
        print("node addresses")
        """ for i, j  in self.node_addresses.items():
            print(i, j) """
        print(self.node_addresses)
        print("cache copies")
        print(self.cache_copies)
        print("lru : ")
        print(self.lru)
        
    # initiates memory manager when it is the first process
    def standalone_init(self, n_pages, port, ip):
        self.ip = ip
        self.port = port
        self.pages = {}
        self.page_addresses = {}
        self.lru = []
        self.id = 0
        self.cache_copies = {}
        self.node_addresses = {} #node id then node ip and port
        self.node_addresses[self.id] = [self.ip, self.port]
        for i in range(n_pages):
            self.pages[i] = {"empty":True, "cache":-1,"data":""}
            self.page_addresses[i] = self.id
            self.cache_copies[i] = []
            self.lru.append(i)
        self.total_nodes = self.id + 1 # in total 1 node
        self.total_pages = n_pages
        self.my_pages = n_pages
        print("standalone_init")
        self.print_self()

    #initiates memory manager when a neighbour address is given
    def send_ask_neighbour(self,my_ip, my_port, n_pages,  neighbour_ip, neighbour_port ):
        self.ip = my_ip
        self.port = my_port
        self.my_pages = n_pages
        self.pages = {}
        message = {}
        self.lru = []
        message["type"] = "send_ask_neighbour"
        s = socket.socket()
        s.connect((neighbour_ip, neighbour_port))
        s.send(json.dumps(message).encode())
        reply = json.loads(s.recv(2048).decode())
        self.id = reply["total_nodes"]
        self.total_pages = reply["total_pages"] + self.my_pages
        self.node_addresses = {}
        for i,j in reply["node_addresses"].items():
            self.node_addresses[int(i)] = j
        self.node_addresses[self.id] = [self.ip, self.port]
        self.total_nodes = self.id + 1
        self.page_addresses = {}
        self.cache_copies = {}
        for i,j in reply["page_addresses"].items():
            self.page_addresses[int(i)] = j
        for i,j in reply["cache_copies"].items():
            self.cache_copies[int(i)] = j
        for i in range(reply["total_pages"], self.total_pages):
            self.pages[i] = {"empty":True,"cache":-1, "data":""}
            self.page_addresses[i] = self.id
            self.cache_copies[i] = []
            self.lru.append(i)
        print("send ask neighbour")
        self.print_self()

    #recieves and replies to ask neighbour request
    def recv_ask_neighbour(self, s):
        message = {}
        message["type"] = "recv_ask_neighbour"
        message["page_addresses"] = self.page_addresses
        message["cache_copies"] = self.cache_copies
        message["node_addresses"] = self.node_addresses
        message["total_nodes"] = self.total_nodes
        message["total_pages"] = self.total_pages
        message = json.dumps(message)
        s.send(message.encode())
        print("recv ask neighbour")
        self.print_self()
        
    #new memory mangers config to its neighbours
    def send_advertise(self):
        message = {}
        message["type"] = "send_advertise"
        message["id"] = self.id
        message["ip"] = self.ip
        message["port"] = self.port
        message["pages"] = self.my_pages
        message = json.dumps(message) 
       
        for i, j in self.node_addresses.items():
            if i != self.id:
                s = socket.socket()
                s.connect((j[0], j[1]))
                s.send(message.encode())
                s.close()
        print("send advertise")
        self.print_self()

    #recieving memory mangers config by its neighbours
    def recv_advertise(self, message):
        print("message : ", message)
        self.node_addresses[message["id"]] = [message["ip"], message["port"]]
        for i in range(self.total_pages, message["pages"] + self.total_pages):
            self.page_addresses[i] = message["id"]
            self.cache_copies[i] = []
        self.total_pages += message["pages"]
        self.total_nodes += 1
        print("recv advertise")
        self.print_self()

    
    #sends the new location of a page to all neighbours
    def send_new_page_loc(self, page_no):
        message = {}
        message["type"] = "send_new_page_loc"
        message["page_no"] = page_no
        message["node"] = self.id
        message = json.dumps(message) 
        for i, j in self.node_addresses.items():
            if i != self.id:
                s = socket.socket()
                s.connect((j[0], j[1]))
                s.send(message.encode())
                s.close()

    #recieving the new location of a page
    def recv_new_page_loc(self, message):
        self.page_addresses[message["page_no"]] = message["node"]

    #telling that a new page has a cache copy of source page
    def send_add_cache_info(self, source_page, cache_page):
        self.cache_copies[source_page].append(cache_page)
        message = {}
        message["type"] = "send_add_cache_info"
        message["source_page"] = source_page
        message["cache_page"] = cache_page
        message = json.dumps(message) 
        for i, j in self.node_addresses.items():
            if i != self.id:
                s = socket.socket()
                s.connect((j[0], j[1]))
                s.send(message.encode())
                s.close()

    #recieving information about a new cached page
    def recv_add_cache_info(self, message):
        self.cache_copies[message["source_page"]].append(message["cache_page"])

    #telling that a / multiple  page has removed cache copy of source page
    def send_delete_cache_info(self, source_page, cache_page):
        
        message = {}
        message["type"] = "send_delete_cache_info"
        message["source_page"] = source_page
        message["cache_page"] = cache_page
        message = json.dumps(message) 
        for i, j in self.node_addresses.items():
            if i != self.id:
                s = socket.socket()
                s.connect((j[0], j[1]))
                s.send(message.encode())
                s.close()
        for i in cache_page: 
            self.cache_copies[source_page].remove(i)

    #recieving information about deleted cached page
    def recv_delete_cache_info(self, message):
        #print("recv::::::::::::::::"+message)
        for i in message["cache_page"]: 
            print("removed cache: " + str(i))
            self.cache_copies[message["source_page"]].remove(i)

    #ask a neighbour to swap the requested page with our lru page
    def send_swap_request(self, source_page, destination_page):
        message = {}
        message["type"] = "send_swap_request"
        message["source_page"] = source_page
        message["destination_page"] = destination_page
        message["page"] = self.pages[source_page]
        message = json.dumps(message)
        s = socket.socket()
        dest_id = self.page_addresses[destination_page]
        print(self.node_addresses[dest_id][0],self.node_addresses[dest_id][1])
        s.connect((self.node_addresses[dest_id][0],self.node_addresses[dest_id][1]))
        s.send(message.encode())
        reply = json.loads(s.recv(2048).decode())
        self.pages[destination_page] = reply['page']
        self.page_addresses[destination_page] = self.id
        del self.pages[source_page]
        s.close()
        self.send_new_page_loc(destination_page)
        print("..........................................")
        print("send swap request")
        self.print_self()

    #action after recieving a swap request
    def recv_swap_request(self, s, message):
        print("Debug1: ", message)
        reply = {}
        reply["type"] = "recv_swap_request"
        reply["source_page"] = message["destination_page"]
        reply["destination_page"] = message["source_page"]
        reply["page"] = self.pages[message["destination_page"]]
        reply = json.dumps(reply)
        s.send(reply.encode())
        self.pages[message["source_page"]] = message["page"]
        #print(type(message["source_page"]))
        self.page_addresses[message["source_page"]] = self.id
        del self.pages[message["destination_page"]]
        s.close()
        self.send_new_page_loc(message["source_page"])
        self.lru.remove(message["destination_page"])
        self.lru.append(message["source_page"])
        print("..........................................")
        print("recv swap request")
        self.print_self()

    #ask a neighbour to copy the requested page with our lru page
    def send_copy_request(self, destination_page, cache_page):
        message = {}
        message["type"] = "send_copy_request"
        message["source_page"] = destination_page
        message = json.dumps(message)
        s = socket.socket()
        dest_id = self.page_addresses[destination_page]
        print(self.node_addresses[dest_id][0],self.node_addresses[dest_id][1])
        s.connect((self.node_addresses[dest_id][0],self.node_addresses[dest_id][1]))
        s.send(message.encode())
        reply = json.loads(s.recv(2048).decode())
        self.pages[cache_page] = reply['page']
        self.pages[cache_page]["cache"] = destination_page
        self.pages[cache_page]["empty"] = False
        self.send_add_cache_info( destination_page, cache_page)
        s.close()
        print("..........................................")
        print("send copy request")
        self.print_self()

    #action after recieving a copy request
    def recv_copy_request(self, s, message):
        print("Debug1: ", message)
        reply = {}
        reply["type"] = "recv_copy_request"
        reply["page"] = self.pages[message["source_page"]]
        reply = json.dumps(reply)
        s.send(reply.encode())
        s.close()
        print("..........................................")
        print("recv copy request")
        self.print_self()

    #delete all cache copies of this page
    def send_delete_total_cache(self, page_no):
        message = {}
        message["type"] = "send_delete_total_cache"
        for i in self.cache_copies[page_no]:
            message["page_no"] = i
            message = json.dumps(message)
            s = socket.socket()
            dest_id = self.page_addresses[i]
            s.connect((self.node_addresses[dest_id][0],self.node_addresses[dest_id][1]))
            s.send(message.encode())
            s.close()
        self.send_delete_cache_info(page_no, self.cache_copies[page_no])
    
    #delete the recieved page number
    def recv_delete_total_cache(self, message):
        self.pages[message["page_no"]]["empty"] = True
        self.pages[message["page_no"]]["cache"] = -1
        self.pages[message["page_no"]]["data"] = ""


    def recv_get_details(self,s):
        reply = {}
        reply['total_pages'] = self.total_pages
        reply = json.dumps(reply)
        s.send(reply.encode())

        
    #got request to read a page from client
    def recv_read_page(self,s,page_no):
        reply = {}
        if page_no not in self.page_addresses:
            reply["response"] = "no such page present"
            reply = json.dumps(reply)
            s.send(reply.encode() )
            return
        
        elif self.page_addresses[page_no] == self.id: # have orignal page with us
            s.send( json.dumps(self.pages[page_no]).encode())
            self.lru.remove(page_no)
            self.lru.append(page_no)
            return
        
        for i in self.cache_copies[page_no]:
            if self.page_addresses[i] == self.id: # have a cached copy with us
                s.send( json.dumps(self.pages[i]).encode())
                self.lru.remove(i)
                self.lru.append(i)
                print("recv_write_page")
                self.print_self()
                return

        target = self.lru[0] #least recently used page

        if self.pages[target]["empty"] == True: # lru page is empty get a cache copy in it
            self.lru.remove(target)
            self.send_copy_request(page_no, target)
            s.send( json.dumps(self.pages[target]).encode())
            self.lru.append(target)
            print("recv_write_page")
            self.print_self()
            return

        if self.pages[target]["cache"] != -1: # lru page has a cache copy in it
            self.lru.remove(target)
            self.send_delete_cache_info(self.pages[target]["cache"], [target]) # deletes previous cache data
            self.send_copy_request(page_no, target)
            s.send( json.dumps(self.pages[target]).encode())
            self.lru.append(target)
            print("recv_write_page")
            self.print_self()
            return
        #do not have empty or cached pages in lru
        self.lru.remove(target)
        self.send_swap_request(target, page_no)
        s.send( json.dumps(self.pages[page_no]).encode())
        self.lru.append(page_no)
        print("recv_write_page")
        self.print_self()
        return

    #got request to write a page from client
    def recv_write_page(self,s,page_no, data):
        reply = {}
        if page_no not in self.page_addresses:
            reply["response"] = "no such page present"
            reply = json.dumps(reply)
            s.send(reply.encode() )    
            return
        
        
        if self.page_addresses[page_no] != self.id:
            target = self.lru[0]
            self.lru.remove(target)
            self.send_swap_request(target,page_no)
            self.send_delete_total_cache(page_no) #deleting all the cache copies
            if self.pages[page_no]["cache"] != -1: #  page has a cache copy in it
                self.send_delete_cache_info(self.pages[page_no]["cache"], [page_no]) # deletes previous cache data
            reply["response"] = "page written"
            reply = json.dumps(reply)
            self.pages[page_no]["empty"] = False
            self.pages[page_no]["data"] = data
            self.pages[page_no]["cache"] = -1
            s.send(reply.encode() )
            #self.lru.remove(page_no)
            self.lru.append(page_no)
        else:
            if self.pages[page_no]["cache"] != -1: #  page has a cache copy in it
                self.send_delete_cache_info(self.pages[page_no]["cache"], [page_no]) # deletes previous cache data
            self.send_delete_total_cache(page_no) #deleting all the cache copies
            reply["response"] = "page written"
            reply = json.dumps(reply)
            self.pages[page_no]["empty"] = False
            self.pages[page_no]["data"] = data
            self.pages[page_no]["cache"] = -1
            s.send(reply.encode() )
            self.lru.remove(page_no)
            self.lru.append(page_no)
        
        print("recv_write_page")
        self.print_self()
        
if __name__ == "__main__":
    my_ip = sys.argv[1]
    my_port = int(sys.argv[2])
    n_pages = int(sys.argv[3])
    if len(sys.argv) > 4: 
        neighbour_ip = sys.argv[4]
        neighbour_port = int(sys.argv[5])
    
    mm = memory_manager()
    if len(sys.argv) == 4:
        mm.standalone_init(n_pages, my_port, my_ip)
    else:
        mm.send_ask_neighbour(my_ip, my_port, n_pages,  neighbour_ip, neighbour_port )
        mm.send_advertise()

    s = socket.socket()
    s.bind((my_ip,my_port))
    s.listen(5)
    while True:
        c, addr = s.accept() 
        message = json.loads(c.recv(2048).decode())
        if message["type"] == "send_ask_neighbour":
            mm.recv_ask_neighbour(c)
        elif message["type"] == "send_advertise":
            mm.recv_advertise(message)
        elif message["type"] == "read_page":
            mm.recv_read_page(c, message['page_no'])
        elif message["type"] == "write_page":
            mm.recv_write_page(c, message['page_no'], message['data'])
        elif message["type"] == "refresh":
            mm.print_self()
        elif message["type"] == "get_details":
            mm.recv_get_details(c)
        elif message["type"] == "send_swap_request":
            mm.recv_swap_request(c, message)
        elif message["type"] == "send_copy_request":
            mm.recv_copy_request(c, message)
        elif message["type"] == "send_new_page_loc":
            mm.recv_new_page_loc(message)
        elif message["type"] == "send_add_cache_info":
            mm.recv_add_cache_info( message)
        elif message["type"] == "send_delete_cache_info":
            mm.recv_delete_cache_info( message)
        elif message["type"] == "send_delete_total_cache":
            mm.recv_delete_total_cache(message)
        

    
