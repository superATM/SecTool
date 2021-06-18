import socket
import ipaddress
import sys
from threadpool import makeRequests, ThreadPool
import time


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
        for ip in ipstr.split(","):
            if "/" in ip:
                for addr in ipaddress.ip_network(ip):
                    ip_list.append(str(addr))
            elif "*" in ip:
                sparts = ip.split("*")
                for i in range(0, 256):
                    ip_list.append(sparts[0] + str(i) + sparts[1])
            elif "-" in ip:
                parts = ip.split("-")
                p1 = parts[0]
                p2 = parts[1]
                p1_last_part = p1.split(".")[-1]
                p1_first_part = ".".join(p1.split(".")[0:-1])
                for i in range(int(p1_last_part),int(p2)):
                    ip_list.append(p1_first_part + "." + str(i))
            else:
                ip_list.append(ip)


        return ip_list
    except Exception as e:
        print("IP_Error:", e)


def conn(ip_port):
    try:
        import time
        parts = ip_port.split(":")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.00001)
        s.connect((parts[0], int(parts[1])))
        if s:
            # print("%s is %d"%(ip_port,True))
            return True
    except:
        return False
    return False

def Get_Res(req_socket, result):
    if result:
        print("{0} is Open".format(req_socket.args[0]))




def main(argv):
    # ,
    # argv = "192.168.43.0/24,10.1.*.2,192.168.2.1 20-40"
    try:
        re = []
        ipport = []
        iplist = split_ip(argv[0])
        portlist = split_port(argv[1])
        for ip in iplist:
            for port in portlist:
                #         # print("trying->{}:{}".format(ip,port))
                #         if conn(ip, port):
                #             open_socket.append(ip+":"+str(port))
                # # return open_socket
                #             print("{0} port {1} is open".format(ip, port))
                ipport.append(ip + ":" + str(port))

        # for ip_port in ipport.pop().split(":"):
        start_time = time.time()
        pool = ThreadPool(100)
        request = makeRequests(conn, ipport, Get_Res)
        [pool.putRequest(req) for req in request]
        pool.wait()
        # for i in ipport:
        #     print(conn(i))
        # for i in re:
        #     print("%s is open".format(i))
        print("%.3f Second Finished"%(time.time() - start_time))
    except Exception as e:
        print("Main Error:", e)


if __name__ == '__main__':
    main(sys.argv[1:])
    # print(conn("39.156.66.18:443"))
