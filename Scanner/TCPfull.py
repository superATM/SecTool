import socket
import ipaddress
import sys
# import thread

def split_port(portstr):
    try:
        port_list = []
        for port in portstr.split(","):
            if "-" in port:
                pparts = port.split("-")
                if pparts[0] > pparts[1]:
                    return Exception
                else:
                    for i in range(eval(pparts[0]), eval(pparts[1]) + 1):
                        port_list.append(i)
            else:
                port_list.append(port)
        return port_list
    except Exception as e:
        print("Port_Error:", e)

def split_ip(ipstr):
    try:
        ip_list = []

        # iplist, portlist = ipstr.split(" ")
        for ip in ipstr.split(","):
            if "/" in ip:
                for addr in ipaddress.ip_network(ip):
                    ip_list.append(str(addr))
            elif "*" in ip:
                sparts = ip.split("*")
                for i in range(0,256):
                    ip_list.append(sparts[0]+str(i)+sparts[1])
            # elif "-" in ip:
            #     parts = ip.split("-")
            #     p1 = parts[0]
            #     p2 = parts[1]
            #
        return ip_list
    except Exception as e:
        print("IP_Error:",e)


def conn(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip,port))
        if s:
            return True
    except :
        return False
    return False


def main(argv):
    # ,
    # argv = "192.168.43.0/24,10.1.*.2,192.168.2.1 20-40"
    try:
        open_socket = []
        iplist = split_ip(argv[0])
        portlist = split_port(argv[1])
        for ip in iplist:
            for port in portlist:
                print("trying->{}:{}".format(ip,port))
                if conn(ip, port):
                    open_socket.append(ip+":"+str(port))
        return open_socket
                    # print("{0} port {1} is open".format(ip, port))
    except Exception as e:
        print("Main Error:",e)



if __name__ == '__main__':
    print(sys.argv[1:])
    main(sys.argv[1:])
