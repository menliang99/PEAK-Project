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
computer = form.getvalue("computer")
pname = form.getvalue("program_name")
Nodes = form.getvalue("nodenum")
MKLenable = form.getvalue("IsMKL")
Comp = form.getvalue("Compiler")
Numa = form.getvalue("IsNUMA")



if computer == "1":
	platform = "Kraken"
elif computer == "2":
	platform = "Nautilus"
else:
	platform = "-- --"

if pname == "":
	Pname = "Not-Defined"
else:
	Pname = pname

if MKLenable == "1":
	
	MKLstat = "Yes"
else:
	MKLstat = "No"

if Comp == "1":
	
	compiler = "Intel"
else:
	compiler = " Not Intel"

if Numa == "1":
	
	archi = "NUMA"
else:

	archi = "None NUMA"

PBSscript = Pname + ".pbs"
FILE = open(PBSscript, "w")


FILE.write("\n#PBS -N " + Pname +"\n")
FILE.write("#PBS -A UT-SUPPORT \n")
FILE.write("#PBS -j oe\n")

if platform == "Kraken":

    FILE.write("#PBS -l walltime=2:00:00,size=" + str(12*int(Nodes)) + "\n\n")

    if MKLenable == "0":
	FILE.write("export OMP_NUM_THREADS=" + str(12*int(Nodes)) + "\n")

    elif MKLenable == "1":
	if Comp == "0":
		FILE.write("export MKL_DYNAMIC=FLASE\n")
		FILE.write("export KMP_AFFINITY=disabled\n")
		FILE.write("export MKL_NUM_THREADS=" + str(12*int(Nodes)) + "\n")

	elif Comp == "1":
		if Numa == "0":
			FILE.write("export MKL_DYNAMIC=FLASE\n")
			FILE.write("export KMP_AFFINITY=disabled\n")
			FILE.write("export MKL_NUM_THREADS=" + str(12*int(Nodes)) + "\n")

		elif Numa == "1":				
			FILE.write("export MKL_DYNAMIC=TRUE\n")
			FILE.write("export KMP_AFFINITY=enabled\n")	
			FILE.write("export MKL_NUM_THREADS=" + str(12*int(Nodes)) + "\n")

    FILE.write("\naprun -n " + str(Nodes) + " -d " + str(12*int(Nodes)) + " ./" + Pname +"\n")

elif platform == "Nautilus":
    
    FILE.write("#PBS -l walltime=1:00:00,ncpus=" + str(16*int(Nodes)) + "\n\n")

    if MKLenable == "0":
	FILE.write("export OMP_NUM_THREADS=" + str(16*int(Nodes)) + "\n")

    elif MKLenable == "1":
	if Comp == "0":
		FILE.write("export MKL_DYNAMIC=FLASE\n")
		FILE.write("export KMP_AFFINITY=disabled\n")
		FILE.write("export MKL_NUM_THREADS=" + str(16*int(Nodes)) + "\n")

	elif Comp == "1":
		if Numa == "0":
			FILE.write("export MKL_DYNAMIC=FLASE\n")
			FILE.write("export KMP_AFFINITY=disabled\n")
			FILE.write("export MKL_NUM_THREADS=" + str(16*int(Nodes)) + "\n")

		elif Numa == "1":				
			FILE.write("export MKL_DYNAMIC=TRUE\n")
			FILE.write("export KMP_AFFINITY=enabled\n")	
			FILE.write("export MKL_NUM_THREADS=" + str(16*int(Nodes)) + "\n")
    nn = int(Nodes)
    if nn < 4:
	FILE.write("\ndplace -x2 ./" + Pname +"\n") 
    else:
	FILE.write("\ndplace -x2 numactl --interleave= `cat /dev/cpuset/torque/$PBS_JOBID/mems` ./" + Pname +"\n")

   
FILE.close()

pspath = "../pbs"
if not os.path.isdir(pspath):
	os.makedirs(pspath)
   	os.system('chmod 755 ../pbs')
else:
	os.system('rm -rf ../pbs')
	os.makedirs(pspath)
   	os.system('chmod 755 ../pbs')

os.system('mv ' + Pname + '.pbs ../pbs/' + Pname + '.pbs')
os.system('chmod 755 ../pbs/'  + Pname + '.pbs')

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
		<b>Compiler and Library Link Advisor</b>
     </table> 
        <hr />   
	
    <table> 
     <tr>
      <td width="500">Selected Platform:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "300" > -------<b>""" + platform + """</b>-------- </td>
      <td width = "300"></td>
     </tr>
   </table>

   <hr />   	

   <table> 
     <tr>
      <td width="500">Program Name is:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + Pname + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  


   <table> 
     <tr>
      <td width="500">Number of Computing Nodes:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + Nodes + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  

   <table> 
     <tr>
      <td width="500">Is MKL Linked:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + MKLstat + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  


   <table> 
     <tr>
      <td width="500">Compiler Status:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + compiler + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  

   <table> 
     <tr>
      <td width="500">Selected System Architecture:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + archi + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  


     	<ul>
		<li><a href="../pbs/""" + Pname + """.pbs">Downloading this PBS Script for Execution on """ + platform + """ </a></li>
		
	</ul>

    </div>
</div>

</body>
</html>
"""


print page2




