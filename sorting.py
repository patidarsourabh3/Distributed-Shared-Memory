from access_module import access_page
import random
#sorting with fixed number of pages
if __name__ == "__main__":
    ip = input("enter ip : ")
    port = int(input("enter port : "))
    a = access_page(ip, port)
    pages = int(input("enter number of pages : "))
    randomlist = random.sample(range(0, pages), pages)
    print(randomlist)
    for i in range(len(randomlist)):
        a.write(randomlist[i], i)
    for i in range(0,pages):
        for j in range(i+1, pages):
            v1 = a.read(i)
            v2 = a.read(j)
            if v1 < v2:
                a.write(v2, i)
                a.write(v1, j)
    for i in range(len(randomlist)):
        print(a.read(i))
