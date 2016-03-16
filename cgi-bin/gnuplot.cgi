#!/usr/bin/env python
import cgi, os, sys, commands, shutil, tarfile
import subprocess
print "Content-Type: text/html\n\n"
print
page1 = """\
<html>
<head><title>First Python HTTP Programming </title></head>
<body>
<h2>Hello World!</h2>
</body>
</html>
"""


form = cgi.FieldStorage();
LibSci = form.getvalue("Libsci")
ACML = form.getvalue("acml")
MKL = form.getvalue("mkl")


Selfun = form.getvalue("FunSel")


allib = []
libs = ""
if LibSci == "1":
   allib.append('libsci')
   libs = "LibSci  " + libs
if ACML == "1":
   allib.append('acml')
   libs = "ACML  " + libs
if MKL == "1":
   allib.append('mkl') 
   libs = "MKL  " + libs

allcompiler = ['pgi', 'intel', 'gnu']

compile_dirs = []
if Selfun == 'Vall':
   compile_dirs = ['dgemm', 'dgemv', 'daxpy', 'dgesv', 'dgetrf', 'dpotrf', 'dgels', 'dgeev', 'dsygv']
   Selfun = 'All Avaliable Functions'
elif Selfun == 'Vnone':
   compile_dirs = []
   Selfun = 'None'
else:
   compile_dirs.append(Selfun)

pspath = "../ps"
if not os.path.isdir(pspath):
   os.makedirs(pspath)
   os.system('chmod 755 ../ps')
else:
   os.system('rm -rf ../ps')
   os.makedirs(pspath)
   os.system('chmod 755 ../ps')

for sub_dir in compile_dirs:

	diagramname = sub_dir + ".plot"
   	shutil.copy2('Temple.plot', diagramname)
	FILE = open(diagramname, "a")
	FILE.write('set title "' + sub_dir + '"\n')

	if sub_dir == 'daxpy':
		FILE.write('set logscale x\n')	
	if sub_dir == 'dgemv':
		FILE.write('set logscale x\n')	

	FILE.write('set output "' + sub_dir + '-flops.ps"\n')
	FILE.write("plot \\\n")
	lsnum = 1
	for lib in allib:
	    ptnum = 4	    
	    for penv in allcompiler:
	#	FILE.write( '"' + "< sqlite3 test.db " +  '\\' + '"' + "select * from LapackResult where routine = \\'"+ sub_dir + "\\' and library = \\'" + lib + "\\' and compiler = \\'" + penv + "\\' ;" + "\\"+ '" "' + " using 4:5 axes x1y1 title " + '"' + lib + '-' + penv + '"' + ' with linespoints ls ' + str(lsnum) + ' pt ' + str(ptnum) + ' ps 1, \\\n')
		FILE.write( '"' + "< sqlite3 test.db " +  '\\' + '"' + "select * from LapackResult where routine = \\'"+ sub_dir + "\\' and library = \\'" + lib + "\\' and compiler = \\'" + penv + "\\' ;" + "\\"+ '" "' + " using 4:5 axes x1y1 title " + '"' + lib + '-' + penv + '"' + ' with linespoints lw 2, \\\n')
		ptnum = ptnum + 2
	    lsnum = lsnum + 1
	FILE.write("1/0 notitle\n")
	FILE.close()
	os.system('gnuplot ' + diagramname)
#	os.system('rm -rf ' + diagramname)
	os.system('mv ' + sub_dir +'-flops.ps ' + '../ps/' + sub_dir + '-flops.ps')
  	os.system('chmod 755 ../ps/' + sub_dir + '-flops.ps')
page2 = """\
<html>
<head>
<title>NICS PeaK</title>
<![if !IE]>  <link href="../styles/screen.css" rel="stylesheet" type="text/css" media="screen" /> <![endif]>
</head>
<body>

<div id="wrapper">

	<div id="header">
        <h1><!--<br><font size="80" face="arial" color="white">
            Hthreads MPSoPC in the Cloud</font>--><img src = "../images/peak.png"/></h1>



	</div>
	<div id="menu">
                <center>
		<ul>
            <a href="../index.html"><li>Home</li></a>
            <a href="../link.html"><li>Compiler Linking Tool</li></a>
            <a href="../execute.html"><li>Program Execution Tool</li></a>
	    <a href="../generate.html"><li>PEAK Performance Generator</li></a>
            <a href="../database.html"><li>PEAK Performance Checkout</li></a>
            <a href="http://www.nics.tennessee.edu/"><li>NICS Home Page</li></a>
		</ul>
                </center>
	</div>

	<div id="content">
         <table align = "center" >
                        <tr>
                            <th width="1000"><br><b>Performance Checkout</b><br></th>    
                        </tr>

   </table>
   <hr />   	
   <table> 
     <tr>
      <td width="500">Selected Numerical Function:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "300" > -------<b>""" + Selfun + """</b>-------- </td>
      <td width = "300"></td>
     </tr>
   </table>

   <hr />   	
   <table> 
     <tr>
      <td width="500">Selected Numerical Library:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + libs + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  

	<ul>
		<li><a href="../ps/""" + sub_dir + """-flops.ps">Downloading Diagram --- """ + sub_dir + """-flops.ps </a></li>
		
	</ul>
    </div>
</div>

</body>
</html>
"""




page3 = """\
<html>
<head>
<title>NICS PeaK</title>
<![if !IE]>  <link href="../styles/screen.css" rel="stylesheet" type="text/css" media="screen" /> <![endif]>
</head>
<body>

<div id="wrapper">

	<div id="header">
        <h1><!--<br><font size="80" face="arial" color="white">
            Hthreads MPSoPC in the Cloud</font>--><img src = "../images/peak.png"/></h1>



	</div>
	<div id="menu">
                <center>
		<ul>
            <a href="../index.html"><li>Home</li></a>
            <a href="../link.html"><li>Compiler Linking Tool</li></a>
            <a href="../execute.html"><li>Program Execution Tool</li></a>
	    <a href="../generate.html"><li>PEAK Performance Generator</li></a>
            <a href="../database.html"><li>PEAK Performance Checkout</li></a>
            <a href="http://www.nics.tennessee.edu/"><li>NICS Home Page</li></a>
		</ul>
                </center>
	</div>

	<div id="content">
         <table align = "center" >
                        <tr>
                            <th width="1000"><br><b>Performance Checkout</b><br></th>    
                        </tr>

   </table>
   <hr />   	
   <table> 
     <tr>
      <td width="500">Selected Numerical Function:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + Selfun + """</b>-------- </td>
      <td width = "300"></td>
     </tr>
   </table>

   <hr />   	
   <table> 
     <tr>
      <td width="500">Selected Numerical Library:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + libs + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  
	<ul>
		<li><a href="../ps/dgemm-flops.ps">Downloading Diagram --- dgemm-flops.ps </a></li>
		<li><a href="../ps/dgemv-flops.ps">Downloading Diagram --- dgemv-flops.ps </a></li>
		<li><a href="../ps/daxpy-flops.ps">Downloading Diagram --- daxpy-flops.ps </a></li>
		<li><a href="../ps/dgesv-flops.ps">Downloading Diagram --- dgesv-flops.ps </a></li>
		<li><a href="../ps/dgetrf-flops.ps">Downloading Diagram --- dgetrf-flops.ps </a></li>
		<li><a href="../ps/dpotrf-flops.ps">Downloading Diagram --- dpotrf-flops.ps </a></li>
		<li><a href="../ps/dgels-flops.ps">Downloading Diagram --- dgels-flops.ps </a></li>
		<li><a href="../ps/dgeev-flops.ps">Downloading Diagram --- dgeev-flops.ps </a></li>
		<li><a href="../ps/dsygv-flops.ps">Downloading Diagram --- dsygv-flops.ps </a></li>		
	</ul>
    </div>
</div>

</body>
</html>
"""

if Selfun == 'All Avaliable Functions':
   print page3
else:
   print page2



