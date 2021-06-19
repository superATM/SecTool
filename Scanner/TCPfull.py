import socket
import ipaddress
import sys
from threadpool import makeRequests, ThreadPool
import time


def split_port(portstr):
    """
    从用户输入中拆出端口，包括 80,443,1-65535 等格式

    :param portstr: 例80,443,1-65535
    :return: port_list = ["80","443","1"..."65535"]
    """
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
    """
    从用户输入中拆出ip地址，包括192.168.1.1,192.168.2.0/24(注：使用掩码形式时前面必须是网络号),192.168.3.*,192.168.4.1-5
    :param ipstr: 192.168.1.1,192.168.2.0/24(注：使用掩码形式时前面必须是网络号),192.168.3.*,192.168.4.1-5
    :return: ip_list = ["192.168.1.1","192.168.2.0","192.168.2.1"..."192.168.2.255","192.168.3.0"..."192.168.3.256","192.168.4.1-5"..."192.168.4.5"]
    """
    try:
        ip_list = []
        for ip in ipstr.split(","):
            if "/" in ip:
                for addr in ipaddress.ip_network(ip):
                    ip_list.append(str(addr))
            elif "*" in ip:
                sparts = ip.split("*")
                for i in range(0, 257):
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
    """
    输入ip：port形式的套接字，使用socket进行连接，设置连接超时时间为0.001
    :param ip_port:  ip:port 例：192.168.1.1:443
    :return:True/False
    """
    try:
        parts = ip_port.split(":")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.001)
        # 设置探活超时，设置过大会拖慢性能，设置过小会因为延迟导致无法正常探活
        s.connect((parts[0], int(parts[1])))
        if s:
            return True
    except OSError:
        pass
    except Exception as e:
        print("Connect_Error:", e)
    else:
        return False

def Get_Res(req_socket, result):
    """
    对结果是True的套接字进行打印
    :param req_socket: ip:port 例：192.168.1.1:443
    :param result: True
    :return: 例：192.168.1.1:443 is open
    """
    if result:
        print("{0} is Open".format(req_socket.args[0]))




def main(argv):
    """
    对输入的ip和port进行整理并使用list列举所有套接字。
    使用线程池对套接字进行探活。
    :param argv: filename.py iprange portrange
    :return:打印用时
    """
    try:
        ipport = []
        iplist = split_ip(argv[0])
        portlist = split_port(argv[1])
        for ip in iplist:
            for port in portlist:
                ipport.append(ip + ":" + str(port))
        start_time = time.time()
        pool = ThreadPool(100)
        # 设置线程数
        request = makeRequests(conn, ipport, Get_Res)
        [pool.putRequest(req) for req in request]
        pool.wait()
        print("%.3f Second Finished"%(time.time() - start_time))
    except Exception as e:
        print("Main Error:", e)


if __name__ == '__main__':
    main(sys.argv[1:])
