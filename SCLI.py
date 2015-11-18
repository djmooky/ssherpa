
import cmd
from Session import Session
from CommandLineToArgV import CommandLineToArgV


class CMD(cmd.Cmd):
	currentSessionId = 0
	sessionCount = 0
	sessionList = {}

	def __updatePrompt(self):
		self.prompt = "SShells [%d] >> " % self.currentSessionId

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
		if len(argv) < 2:
			print "usage: create user ip password <extra args>"
			return
		s = Session(argv[0], argv[1])
		self.sessionList[sessId] = s
		self.sessionCount = sessId

	def do_sesslist(self, line):
		print "%4s %20s %20s %5s %8s" % ("ID", "user@addr", "password", "port", "Active?")
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
			self.sessionList[self.currentSessionId].connect()
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

	def do_quit(self, line):
		print "Closing existing connections"
		for k in self.sessionList:
			self.sessionList[k].disconnect()
		print "Exiting"
		return True

