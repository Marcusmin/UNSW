#Python version is 3.7.3
import sys
import socket
import copy
import time

UPDATE_INTERVAL = 1
ROUTE_UPDATE_INTERVAL = 30
TIME_OUT = 1

def process_text(file_name):#this function can extra link-state from the text file
    try:
        f = open(file_name)
    except FileNotFoundError:
        print('please enter right file name.')
        sys.exit()
    content = []#include local node and directly linked nodes
    time = []
    for line in f.readlines():
        content.append(line.strip().split())
    vertex_text.append(content[0][0])#original vertex
    for each in content[2:]:
        port.append(int(each[2]))
        vertex_text.append(each[0])
        time.append(float(each[1]))
    for i in range(1, len(port)+1):
        rtt.append((str(vertex_text[0]) + str(vertex_text[i]), time[i-1]))
    return int(content[0][1]), [content[0][0]], rtt

#message = [('FA', 2.2), ('FD', 0.7), ('FE', 6.2)]
def update_text(message, useful_vertex, rtt):#update vertex[] & rtt[] by receiving content//message is list// realize the dynamic changes in network
    for each in message:
        if each[0][0] not in useful_vertex:
            useful_vertex.append(each[0][0])
        if each not in rtt:
            rtt.append(each)

def clean_text(useful_vertex):#clean useless node(some failed nodes)
    new_rtt = []
    for each in rtt:
        if each[0][0] in useful_vertex and each[0][1] in useful_vertex and each != '':
            new_rtt.append(each)
    return new_rtt

def send(s, rtt, port):#send the link-state information to directly linked nodes
    send_content = str(rtt)
    for each in port:
        addr = ('127.0.0.1', each)
        s.sendto(send_content.encode(encoding = 'UTF-8', errors = 'strict'),addr)

def receive(s):# receive the link-state information from directly linked nodes
    try:
        data,addr = s.recvfrom(2048)
        if data == '':
            return ''
        data_decode = eval(data.decode(encoding = 'UTF-8', errors = 'strict'))
        return data_decode
    except socket.timeout:
        return ''

def Dij(a):# throught the dijkstra algorithm get the shorest path
    used = set(a)
    cost[a] = 0
    pre[a] = a
    for each in rtt:
        if a in each[0]:
            cost[each[0].replace(a, '')] = each[1]
            pre[each[0].replace(a, '')] = a
    while (used != set(useful_vertex)):
        min_num = 99999
        for each in rtt:
            if each[0][0] in used and each[0][1] not in used and each[1] < min_num:
                min_num = each[1]
                node = each[0][1]
        if min_num != 99999:
            used.add(node)
            for each in rtt:
                if each[0][0] == node:
                    if cost[each[0].replace(node, '')] > cost[node] + each[1] and each[0][1] not in used:
                        cost[each[0].replace(node, '')] = cost[node] + each[1]
                        pre[each[0].replace(node, '')] = node

def print_path(useful_vertex, pre, rtt ,cost):#print the output based on the specification
	for each in useful_vertex:
		if each != ori_vertex[0]:
			temp = each
			head = each
			while (pre[each] != ori_vertex[0]):
				each = pre[each]
				temp += each
			temp += pre[each]
			temp = temp[::-1]
			print(f'Least cost path to router {head}:{temp} and the cost is {cost[head]:.1f}')


file_name = sys.argv[1]
vertex_text = []#vertex//text temp
port = []#send port//[5000, 5003, 5004]
rtt = []#send content ->rtt//will be modified or clean
ori_port, ori_vertex, ori_rtt = copy.deepcopy(process_text(file_name))#get the original content <- text -> (ori_vertex)['F', 'A', 'D', 'E']; (ori_rtt)[('FA', 2.2), ('FD', 0.7), ('FE', 6.2)]
useful_vertex = copy.deepcopy(ori_vertex)#vertex//will be modified


while 1:
    start_time = time.time()#timer start
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#construct socket
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#re-use ip and port
    s.settimeout(TIME_OUT)
    s.bind(('127.0.0.1', ori_port))
    receive_times = len(port)
    send(s, ori_rtt, port)#first send
    rtt = copy.deepcopy(ori_rtt)#initialize the sending content
    print(f'I am Router {ori_vertex[0]}')
    for i in range(2):#UDP unreliable so send 3 times
        for j in range(receive_times):
            message = receive(s)
            if message != '':
                update_text(message, useful_vertex, rtt)
            else:
                continue
        time.sleep(UPDATE_INTERVAL)
        send(s, rtt, port)
    rtt = clean_text(useful_vertex)
    cost = {}
    pre = {}
    for each in useful_vertex:
        cost[each] = 99999
    Dij(ori_vertex[0])
    end_time = time.time()#timer end
    duration = end_time - start_time
    wait_time = ROUTE_UPDATE_INTERVAL - duration if duration < ROUTE_UPDATE_INTERVAL else 0#ensure 30 second
    for _ in range(int(wait_time)):#it will still broadcast during rest time
        send(s, rtt, port)
        time.sleep(UPDATE_INTERVAL)
    if len(useful_vertex) > 1:
        print_path(useful_vertex, pre, rtt ,cost)
    useful_vertex = copy.deepcopy(ori_vertex)#initialize the useful vertex
    s.close()


