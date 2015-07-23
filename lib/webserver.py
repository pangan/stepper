import socket
import sys
import threading
import re
import datetime 

class WebServer(object):
	def __init__(self,port=8080, template='index.html'):
		self.client = None
		self.template = template
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1 )
		server_address = ('0.0.0.0', port)
		print >>sys.stderr, 'starting up on %s port %s' % server_address
		self.sock.bind(server_address)
		self.sock.listen(1)

	def parse_data(self, raw_data):
	    m = re.search('\?(.+?) ', raw_data)
	    if m:
	        tmp_params = m.group(1).split('&')
	        ret_dic = {}
	        for item in tmp_params:
	            var_tmp = item.split('=')
	            ret_dic[var_tmp[0]]=var_tmp[1]

	        return ret_dic

	    else:
	        return None

	def resp_html(self):
	    html_file = open(self.template,'r')
	    html = html_file.readlines()
	    return html



	def read(self):
		connection, self.client = self.sock.accept()
		data = connection.recv(1024)
		data_dic = self.parse_data(data)
		for html_lines in self.resp_html():
			connection.sendall(html_lines)

		connection.close()
		return data_dic



	def close(self):
		self.sock.close()