from access_module import access_page

class group_chat:

    def __init__(self):
        self.ip = input("Enter ip for the memory manager ")
        self.port = int(input("Enter port for the memory manager "))
        self.access = access_page(self.ip, self.port)
        self.pages = int(input("enter number of pages"))
        self.name_page = self.access.get_details()['total_pages'] - self.pages
        self.status_page = self.name_page + 1
        self.name = input("Enter Name ")
        self.access.write(self.name, self.name_page)
        self.dict_status = {}

    def update_status(self):
        self.status = input('Enter updated status')
        self.access.write(self.status, self.status_page)

    def check_updates(self):        
        for i in range(1, self.access.get_details()["total_pages"], self.pages):
            if i not in self.dict_status:
                self.dict_status[i] = ""
            new_status = self.access.read(i)
            new_name = self.access.read(i-1)
            if self.dict_status[i] != new_status and i != self.status_page:
               # print(new_name + " : " + new_status)
               print(new_name)
               print(new_status)
               self.dict_status[i] = new_status
if __name__ == "__main__":
    g = group_chat()
    while True:
        inp = int(input("Enter 1 to write and 2 to read"))
        if inp == 1:
            g.update_status()
        else:
            g.check_updates()



