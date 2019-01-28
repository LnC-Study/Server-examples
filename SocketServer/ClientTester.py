import concurrent.futures
import socket, time, struct

def tester( _clientId):
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect( ('localhost', 8090))
        for i in range(10):
            time.sleep(2)
            custumData = struct.pack('>hfffq', _clientId+10, 1.5 + i, 2.5 + i, 3.5 + i, 22485)
            print( custumData)
            sock.sendall( custumData)

if __name__ == '__main__':
    processes = 6
    clientIds = [ id for id in range( processes)]
    with concurrent.futures.ProcessPoolExecutor(max_workers= processes) as executor:
        res = executor.map(tester, clientIds)