
import os
import sys
from getpass import getpass
import subprocess


def call(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr):
	print "[-] %s" % cmd
	return subprocess.call(cmd, shell=shell, stdout=stdout, stderr=stderr)

class Session:
	def __init__(self, argv):
		if len(argv) < 1:
			print "usage: create <user@ip> <extra args>"
			raise ValueError()
		(self.user, self.ip) = argv[0].split('@')
		port = "22"
		self.port = port
		self.active = False
		self.extraArgs = argv[1:]
		self.pipeName = "/tmp/ssherpa_sock_%s-%s" % (self.user, self.ip)

	def connect(self):
		if self.active:
			print "[+] Already Connected to %s@%s" % (self.user, self.ip)
			return True
		sshCmd = "ssh -X %s@%s -MfN -S %s" % (self.user, self.ip, self.pipeName)
		child = call(sshCmd)

		self.active = True
		return True

	def disconnect(self):
		sshCmd = "ssh %s@%s -S %s -O exit" % (self.user, self.ip, self.pipeName)
		child = call(sshCmd)
		try:
			os.unlink(self.pipeName)
		except:
			pass

		self.active = False

	def sexec(self, argv):
		if len(argv) != 1:
			print "[*] no command provided"
			return False
		sshCmd = "ssh %s@%s -S %s %s" % (self.user, self.ip, self.pipeName, argv[0])
		call(sshCmd)
	
	def interact(self):
		child = None
		sshCmd = "ssh %s@%s -S %s" % (self.user, self.ip, self.pipeName)
		child = call(sshCmd)

	def get(self, args):
		if len(args) == 1:
			dst = "."
		else:
			dst = args[1]
		sshCmd = "scp -p -o 'ControlPath %s' %s@%s:%s %s" % (self.pipeName, self.user, self.ip, args[0], dst)
		child = call(sshCmd)

	def put(self, args):
		if len(args) == 1:
			dst = "."
		else:
			dst = args[1]
		sshCmd = "scp -p -o 'ControlPath %s' %s %s@%s:%s" % (self.pipeName, args[0], self.user, self.ip, dst)
		child = call(sshCmd)

	def __str__(self):
		return "%20s %5s %8s" % ("%s@%s" % (self.user, self.ip), self.port, str(self.active))