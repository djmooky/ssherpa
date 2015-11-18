
import cmd
from Session import Session
from CommandLineToArgV import CommandLineToArgV


class CMD(cmd.Cmd):
	currentSessionId = 0
	sessionCount = 0
	sessionList = {}

	def __updatePrompt(self):
		self.prompt = "ssherpa [%d] >> " % self.currentSessionId

	def __idInSesslist(self, id):
		if id in self.sessionList:
			return True
		return False

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.__updatePrompt()

	def do_create(self, line):
		sessId = self.sessionCount + 1
		argv = CommandLineToArgV(line)
		try:
			s = Session(argv)
			self.sessionList[sessId] = s
			self.sessionCount = sessId
			print "[+] Added as session %d" % sessId
		except:
			pass

	def do_sesslist(self, line):
		print "%4s %20s %5s %8s" % ("ID", "user@addr", "port", "Active?")
		for k in self.sessionList:
			print "%4s %s" % (str(k), self.sessionList[k])

	def do_attach(self, line):
		args = CommandLineToArgV(line)
		if len(args) is not 1:
			print "usage: attach <n>"
			return
		id = int(args[0])
		if self.__idInSesslist(id):
			self.currentSessionId = id
			self.__updatePrompt()
		else:
			print "no session id %d in list" % id

	def do_connect(self, line):
		if self.__idInSesslist(self.currentSessionId):
			self.sessionList[self.currentSessionId].connect()
		else:
			print "no session id %d in list" % self.currentSessionId

	def do_disconnect(self, line):
		if self.__idInSesslist(self.currentSessionId):
			self.sessionList[self.currentSessionId].disconnect()
		else:
			print "no session id %d in list" % self.currentSessionId

	def do_interact(self, line):
		if self.__idInSesslist(self.currentSessionId):
			self.sessionList[self.currentSessionId].interact()
		else:
			print "no session id %d in list" % self.currentSessionId

	def do_put(self, line):
		args = CommandLineToArgV(line)
		if self.__idInSesslist(self.currentSessionId):
			self.sessionList[self.currentSessionId].put(args)
		else:
			print "no session id %d in list" % self.currentSessionId

	def do_get(self, line):
		args = CommandLineToArgV(line)
		if self.__idInSesslist(self.currentSessionId):
			self.sessionList[self.currentSessionId].get(args)
		else:
			print "no session id %d in list" % self.currentSessionId

	def do_exec(self, line):
		args = CommandLineToArgV(line)
		if self.__idInSesslist(self.currentSessionId):
			self.sessionList[self.currentSessionId].sexec(args)
		else:
			print "no session id %d in list" % self.currentSessionId

	def do_quit(self, line):
		print "Closing existing connections"
		for k in self.sessionList:
			self.sessionList[k].disconnect()
		print "Exiting"
		return True


