
import pexpect
import os
import sys

def call(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr):
	return pexpect.spawn(cmd, logfile=stdout)

class Session:
	def __init__(self, cinfo, password, port="22", *xargs):
		
		(self.user, self.ip) = cinfo.split('@')
		self.password = password
		self.port = port
		self.active = False
		self.extraArgs = xargs
		self.pipeName = "/tmp/sheshells_sock_%s" % cinfo
		self.pipeChild = None
		self.activeShell = None

	def connect(self):
		if self.active:
			print "[+] Already Connected to %s@%s" % (self.user, self.ip)
			return True
		sshCmd = "ssh -X %s@%s -MN -S %s" % (self.user, self.ip, self.pipeName)
		print sshCmd
		self.pipeChild = call(sshCmd)
		r = self.pipeChild.expect(["Are you sure", "assword:"])
		if r == 0:
			self.pipeChild.sendline("yes")
		elif r == 1:
			self.pipeChild.sendline(self.password)
		else:
			print "[*] Undefined error response"
			return False

		self.active = True
		return True

	def disconnect(self):
		sshCmd = "ssh %s@%s -S %s -o exit" % (self.user, self.ip, self.pipeName)
		self.pipeChild = call(sshCmd)
		os.unlink(self.pipeName)
		self.active = False

	def interact(self):
		child = None
		if self.activeShell == None:
			sshCmd = "ssh %s@%s -S %s" % (self.user, self.ip, self.pipeName)
			print sshCmd
			child = call(sshCmd)
		else:
			child = self.activeShell
		child.interact()
		if not child.isalive():
			self.activeShell = child

	def get(self, args):
		if len(args) == 1:
			dst = "."
		else:
			dst = args[1]
		sshCmd = "scp -p -o 'ControlPath /tmp/%s' %s@%s:$%s %s" % (self.pipeName, self.user, self.ip, args[0], dst)
		child = call(sshCmd)

	def put(self, args):
		if len(args) == 1:
			dst = "."
		else:
			dst = args[1]
		sshCmd = "scp -p -o 'ControlPath /tmp/%s' %s %s@%s:$%s" % (self.pipeName, args[0], self.user, self.ip, dst)
		child = call(sshCmd)

	def get(self, args):

		pass

	def __str__(self):
		return "%20s %20s %5s %8s" % ("%s@%s" % (self.user, self.ip), self.password, self.port, str(self.active))