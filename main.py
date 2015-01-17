import os
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer


class MomServer(object):
	
	def __init__(self, stream, address):
		self.stream 	=	stream
		self.address 	=	address
		self.stream.set_close_callback(self._on_close)
		self.stream.read_until('\n', self._on_read_line)


	def _on_read_line(self, data):
		data = data.rstrip()
		self.stream.write(data, self._on_write_complete)


	def _on_write_complete(self):
		if not self.stream.reading():
			self.stream.read_until('\n', self._on_read_line)
		self.stream.close()


	def _on_close(self):
		pass


class Server(TCPServer):

	def __init__(self, io_loop=None, ssl_options=None, **kwargs):
		TCPServer.__init__(self, io_loop=io_loop, ssl_options=ssl_options, **kwargs)

	def handle_stream(self, stream, address):
		MomServer(stream, address)




if __name__ == '__main__':
	server = Server()
	port = int(os.environ.get("RUPPELLS_SOCKETS_LOCAL_PORT", 1234))
  	server.listen(port)
	IOLoop.instance().start()