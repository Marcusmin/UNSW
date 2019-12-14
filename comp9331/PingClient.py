#Python 3
import sys
import time
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (sys.argv[1], int(sys.argv[2]))
s.connect(address)

for _ in range(10):
    localtime = time.asctime(time.localtime(time.time()))
    string = f'PING {_} {localtime}\r\n'
    t0 = time.perf_counter()
    s.sendto(str.encode(string), address)    
    s.settimeout(1)
    try: 
    	data, addr = s.recvfrom(1024)
    except socket.timeout:
        print(f'ping to {sys.argv[1]}, seq = {_+1}, time out')
        continue
    rrt = int(str((time.perf_counter() - t0)*1000).split('.')[0])
    if (rrt > 1000):
        print(f'ping to {sys.argv[1]}, seq = {_+1}, time out')
        continue
    else:
        print(f'ping to {sys.argv[1]}, seq = {_+1}, rtt = {rrt} ms')

s.close()
