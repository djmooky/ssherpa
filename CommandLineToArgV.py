#!/usr/bin/env python

def CommandLineToArgV(line):
	l = len(line)

	in_QM = False
	in_TEXT = False
	in_SPACE = True
	
	_argv = ""
	for i in range(l):

		if in_QM:
			if line[i] == '"':
				in_QM = False
			else:
				_argv += line[i]
		else:
			if line[i] == '"':
				in_QM = True
				in_TEXT = True
				in_SPACE = False
			elif line[i] == ' ' or line[i] == '\t' or line[i] == '\r' or line[i] == '\n':
				_argv += '\0'
				in_TEXT = False
				in_SPACE = False
			else:
				_argv += line[i]


	return _argv.split('\0')


if __name__ == '__main__':
	line = "this is a test -p of the 10981823 \" operating + 1\" system"
	print("parsing the line: \n%s" % line)
	foo = CommandLineToArgV(line)
	c = 0
	for i in foo:
		print "%d: '%s'" % (c, i)
		c = c+1