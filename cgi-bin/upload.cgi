#!/usr/bin/env python
import cgi, os, sys, commands, paramiko

print "Content-Type: text/html\n\n"
print

page1 = """\
<html>
<head><title>First Python HTTP Programming </title></head>
<body>
<h2>File Runjobs has been successfully uploaded to Kraken</h2>
</body>
</html>
"""
page2 = """\
<html>
<head><title>First Python HTTP Programming </title></head>
<body>
<h2>Sorry Authentication Failure. Please upload again.</h2>
</body>
</html>
"""

page3 = """\
<html>
<head><title>First Python HTTP Programming </title></head>
<body>
<h2>Errors Happen. Please download the file and upload it manually.</h2>
</body>
</html>
"""

#remotehost = 'pacman.ddns.uark.edu'
remotehost = 'login.kraken.nics.xsede.org'
logname = 'mliang'

form = cgi.FieldStorage();
UserID = form.getvalue("Username")
updatingkey = form.getvalue("Key")

ConFlag = 0

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	ssh.connect(remotehost, username = UserID, password = updatingkey)
	upfile = 'runjobs'
	remotedir = '/lustre/scratch/' + UserID + '/peak/' #mliang/peak/'
	filename = 'runjobs'
	ftp = ssh.open_sftp()
	ftp.put( upfile,  os.path.join(remotedir, filename))
	ftp.close()
	ConFlag = 1
	print page1
except paramiko.AuthenticationException:
  	ConFlag = 2
	print page2
except socket.error, e:
  	ConFlag = 3
	print page3

