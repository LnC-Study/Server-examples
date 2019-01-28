import select
import socket

from Logger import Logger
from Session import Session
import config

class Server:
    def __init__(self, _host, _port, _eventQueue = None):
        self.serverSocket = self._init_server_socket( _host, _port)

        self.epoll = select.epoll()
        self.epoll.register( fd= self.serverSocket.fileno(),
                             eventmask= select.EPOLLIN | select.EPOLLET)
        self.eventQueue, self.connections, self.sessions = _eventQueue, {}, {}

        Logger.logWriter.debug('Register the server on socket epoll')

    def _init_server_socket(self, _host, _port):
        server = socket.socket( family= socket.AF_INET,
                                type= socket.SOCK_STREAM)

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        server.setblocking( False)
        server.bind( (_host, _port))
        server.listen( config.SERVER['MAX_LISTENER'])

        Logger.logWriter.info(f'Initialize the Socket {_host}:{_port}')
        return server

    def _handle_accept(self):
        connection, address = self.serverSocket.accept()
        connection.setblocking( False)
        self.epoll.register( fd= connection.fileno(),
                             eventmask= select.EPOLLIN | select.EPOLLET | select.EPOLLRDHUP)
        self.connections[ connection.fileno()] = connection
        self.sessions[ connection.fileno()] = Session(self.eventQueue)

        Logger.logWriter.info(f'Register a new client: {connection}/{address}')

    def _handle_message(self, fileno):
        try:
            data = self.connections[ fileno].recv( config.RECV_BUF_SIZE)
            if len(data) == 0:
                self._cleanUp_session( fileno)
            else:
                self.sessions[ fileno].proc( data)
        except socket.error as e:
            print( e)
            self._cleanUp_session( fileno)

    def _cleanUp_session(self, fileno):
        self.epoll.unregister( fileno)
        self.sessions[ fileno].teardown()
        self.connections[ fileno].close()
        Logger.logWriter.info(f'Clean up session[{fileno}]')

    def _loop(self):
        try:
            while True:
                events = self.epoll.poll( timeout= 0.5)
                for fileno, event in events:
                    if fileno is self.serverSocket.fileno():
                        # Accept new connection
                        self._handle_accept()
                    elif event & select.EPOLLIN:
                        # Message inbounded
                        self._handle_message( fileno)
                    elif event & select.EPOLLRDHUP:
                        # Half close
                        self._cleanUp_session( fileno)

        finally:
            self.shutdown()

    def start(self):
        self._loop()

    def shutdown(self):
        self.epoll.unregister( self.serverSocket.fileno())
        self.epoll.close()
        self.serverSocket.close()

        Logger.logWriter.info('Shutdown server')