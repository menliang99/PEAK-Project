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
LibSci = form.getvalue("LibSci")
ACML = form.getvalue("ACML")
MKL = form.getvalue("MKL")

PGI = form.getvalue("PGI")
GNU = form.getvalue("GNU")
Intel = form.getvalue("Intel")

daxpy = form.getvalue("daxpy")
dgeev = form.getvalue("dgeev")
dgels = form.getvalue("dgels")
dgemm = form.getvalue("dgemm")
dgemv = form.getvalue("dgemv")
dgesv = form.getvalue("dgesv")
dgetrf= form.getvalue("dgetrf")
dpotrf= form.getvalue("dpotrf")
dsygv = form.getvalue("dsygv")

daxpymin = form.getvalue("daxpymin")
dgeevmin = form.getvalue("dgeevmin")
dgelsmin = form.getvalue("dgelsmin")
dgemmmin = form.getvalue("dgemmmin")
dgemvmin = form.getvalue("dgemvmin")
dgesvmin = form.getvalue("dgesvmin")
dgetrfmin= form.getvalue("dgetrfmin")
dpotrfmin= form.getvalue("dpotrfmin")
dsygvmin = form.getvalue("dsygvmin")


daxpymax = form.getvalue("daxpymax")
dgeevmax = form.getvalue("dgeevmax")
dgelsmax = form.getvalue("dgelsmax")
dgemmmax = form.getvalue("dgemmmax")
dgemvmax = form.getvalue("dgemvmax")
dgesvmax = form.getvalue("dgesvmax")
dgetrfmax= form.getvalue("dgetrfmax")
dpotrfmax= form.getvalue("dpotrfmax")
dsygvmax = form.getvalue("dsygvmax")

daxpystep = form.getvalue("daxpystep")
dgeevstep = form.getvalue("dgeevstep")
dgelsstep = form.getvalue("dgelsstep")
dgemmstep = form.getvalue("dgemmstep")
dgemvstep = form.getvalue("dgemvstep")
dgesvstep = form.getvalue("dgesvstep")
dgetrfstep= form.getvalue("dgetrfstep")
dpotrfstep= form.getvalue("dpotrfstep")
dsygvstep = form.getvalue("dsygvstep")

cleanjob = form.getvalue("clean")
compilejob = form.getvalue("compile")
executejob = form.getvalue("execute")

allib = []
libs = ""
if LibSci == "1":
   allib.append('libsci')
   libs = "'libsci', " + libs
if ACML == "1":
   allib.append('acml')
   libs = "'acml', " + libs
if MKL == "1":
   allib.append('mkl') 
   libs = "'mkl', " + libs

allcompiler = []
comps = ""
if PGI == "1":
   allcompiler.append('pgi')
   comps = "'pgi', " + comps
if GNU == "1":
   allcompiler.append('gnu')
   comps = "'gnu', " + comps
if Intel == "1":
   allib.append('intel') 
   comps = "'intel', " + comps



shutil.copy2('Main_temple.py', 'runjobs')
compilescript = "runjobs"
FILE = open(compilescript, "a")

FILE.write("   allib = [" + libs +"]\n") 
FILE.write("   allcompiler = [" + comps +"]\n\n") 

compile_dirs = []
funs = ""

if dgemm == "1":
   compile_dirs.append('dgemm')
   funs = "'dgemm', "+ funs
   dgemmparm = dgemmmin + ', ' + dgemmmax + ', ' + dgemmstep
   FILE.write("   dgemmparm = [" + dgemmparm +"]\n") 
if dgemv == "1":
   compile_dirs.append('dgemv')
   funs = "'dgemv', " + funs
   dgemvparm = dgemvmin + ', ' + dgemvmax + ', ' + dgemvstep
   FILE.write("   dgemvparm = [" + dgemvparm +"]\n") 
if daxpy == "1":
   compile_dirs.append('daxpy')
   funs = "'daxpy', " + funs
   daxpyparm = daxpymin + ', ' + daxpymax + ', ' + daxpystep
   FILE.write("   daxpyparm = [" + daxpyparm +"]\n") 
if dgesv == "1":
   compile_dirs.append('dgesv')
   funs = "'dgesv', " + funs
   dgesvparm = dgesvmin + ', ' + dgesvmax + ', ' + dgesvstep
   FILE.write("   dgesvparm = [" + dgesvparm +"]\n") 
if dgetrf == "1":
   compile_dirs.append('dgetrf')
   funs = "'dgetrf', " + funs
   dgetrfparm = dgetrfmin + ', ' + dgetrfmax + ', ' + dgetrfstep
   FILE.write("   dgetrfparm = [" + dgetrfparm +"]\n") 
if dpotrf == "1":
   compile_dirs.append('dpotrf')
   funs = "'dpotrf', " + funs
   dpotrfparm = dpotrfmin + ', ' + dpotrfmax + ', ' + dpotrfstep
   FILE.write("   dpotrfparm = [" + dpotrfparm +"]\n") 
if dgels == "1":
   compile_dirs.append('dgels')
   funs = "'dgels', " + funs
   dgelsparm = dgelsmin + ', ' + dgelsmax + ', ' + dgelsstep
   FILE.write("   dgelsparm = [" + dgelsparm +"]\n") 
if dgeev == "1":
   compile_dirs.append('dgeev')
   funs = "'dgeev', " + funs
   dgeevparm = dgeevmin + ', ' + dgeevmax + ', ' + dgeevstep
   FILE.write("   dgeevparm = [" + dgeevparm +"]\n") 

if dsygv == "1":
   compile_dirs.append('dsygv')
   funs = "'dsygv', " + funs
   dsygvparm = dsygvmin + ', ' + dsygvmax + ', ' + dsygvstep
   FILE.write("   dsygvparm = [" + dsygvparm +"]\n") 

FILE.write("   compile_dirs = [" + funs +"]\n\n") 

FILE.write("   routine_params = []\n")

FILE.write("   for i in compile_dirs:\n")
FILE.write("""\troutine = i + "parm"\n""")
FILE.write("\troutine_params.append(eval(routine))\n\n")


if cleanjob == "1":
	FILE.write("   cleanjobs.clean_jobs (main_dir, compile_dirs, allib, allcompiler)\n")
if compilejob == "1":
	FILE.write("   compilejobs.compile_jobs (main_dir, compile_dirs, allib, allcompiler, ACMLDIR, MKLDIR)\n")
if executejob == "1":
	FILE.write("   executejobs.execute_jobs (main_dir, compile_dirs, allib, allcompiler, routine_params)\n")
FILE.write("""\n\n\nif __name__ == "__main__":\n""")
FILE.write("\tmain()")

FILE.close()



tar = tarfile.open("AllPythonScripts.tar.bz2", "w:bz2")

for name in ["cleanjobs.py", "compilejobs.py", "executejobs.py", "runjobs"]:
	tar.add(name)
tar.close()

pspath = "../py"
if not os.path.isdir(pspath):
	os.makedirs(pspath)
	os.system('chmod 755 ../py')
else:
	os.system('rm -rf ../py')
	os.makedirs(pspath)
	os.system('chmod 755 ../py')

os.system('mv runjobs ../py/runjobs')
os.system('chmod 755 ../py/runjobs')
os.system('mv AllPythonScripts.tar.bz2 ../py/AllPythonScripts.tar.bz2')
os.system('chmod 755 ../py/AllPythonScripts.tar.bz2')

page2 = """\

<html>
<head>
<title>NICS PeaK</title>
<![if !IE]>  <link href="../styles/screen.css" rel="stylesheet" type="text/css" media="screen" /> <![endif]>
</head>
<body>
<form action="upload.cgi" enctype="multipart/form-data" method="POST">

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
                            <th width="1000"><br><b>Performance Generation</b><br></th>    
                        </tr>

   	</table>
   	<hr /> 
  	
  	<table> 
    	 <tr>
     		<td width="700">Selected Numerical Function:</td> 
    	 </tr>
     	<tr>
      		<td width = "300"></td>
     		<td width = "1000" > -------<b>""" + funs + """</b>-------- </td>
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
  	
	
  	 <table> 
    	 <tr>
     	 <td width="500">Selected Avaliable Compiler:</td> 
     	</tr>

    	 <tr>
        	<td width = "300"></td>
      	  	<td width = "500" > -------<b>""" + comps + """</b>------- </td>
      		<td width = "300"></td>
     	</tr>
   </table>

   <hr/>

     <table>

    	 <tr>

     	 <td width="500">Downloading Python Scripts:</td> 

     	</tr>
     <tr>

	<ul>

	<td width = "500"><li><a href="../py/runjobs">python script for running</a></li></td>
      	 <td width = "300"></td>
	</ul>

      </tr>  

     <tr>

	<ul>

	 <td width = "500"><li><a href="../py/AllPythonScripts.tar.bz2">Downloading all the python scripts </a></li></td>
      	 <td width = "300"></td>
	</ul>

      </tr>

       </table>

	<hr />

    <table>

    	 <tr>

     	 <td width="500">Uploading Scripts to Kraken:</td> 

     	</tr>
     <tr>
      	 <td width = "300"></td>
	 <td width = "500" align = "center">User @ Kraken: <input type = "text" name = "Username" size="15"></td>
      	 <td width = "300"></td>

      </tr>  

     <tr>
      	 <td width = "300"></td>
	 <td width = "500" align = "center">Key to Kraken:  <input type="password" name = "Key" size="16"></td>
      	 <td width = "300"></td>

      </tr>

       </table>

       <div>
            <table align = "left" width = "700" >
	    <tr>
		<td></td>
		<td align = "center"><br><input type = "submit" value = "Upload to Kraken" ></td>
	    </tr>

	    </table>
	</div>

   </div>

</div>

</body>
</html>
"""
print page2


