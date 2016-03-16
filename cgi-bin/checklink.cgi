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
libr = form.getvalue("library")
comp = form.getvalue("compiler")


if computer == "1":
	platform = "Kraken"
elif computer == "2":
	platform = "Nautilus"
else:
	platform = "-- --"

if libr == "1":
	lib = "LibSci"
elif libr == "2":
	lib = "ACML"
elif libr == "3":
	lib = "MKL"
else:
	lib = "-- --"

if comp == "1":
	compiler = "PGI"
elif comp == "2":
	compiler = "Intel"
elif comp == "3":
	compiler = "Intel"
else:
	compiler = "-- --"


if platform == "Kraken":

	if lib == 'LibSci' and compiler == 'PGI':
 		LABOPT ='-O3 -fast '
		LABLIB =''
	elif lib == 'LibSci' and compiler == 'Intel':
		LABOPT='-O3 '
		LABLIB=''
	elif lib == 'LibSci' and compiler == 'Intel':
		LABOPT='-O3 '
		LABLIB=''	

	elif lib == 'ACML' and compiler == 'PGI':
		LABOPT='-O3 -fast -tp=istanbul-64 -mp -Mcache_align '
		LABLIB=' $(ACMLDIR)/pgi64_mp/lib/libacml_mp.a'	

	elif lib == 'ACML' and compiler == 'Intel':
		LABOPT='-O3 '
		LABLIB=' $(ACMLDIR)/ifort64_mp/lib/libacml_mp.a -openmp -lpthread'		

	elif lib == 'ACML' and compiler == 'Intel':
		LABOPT='-O3 -fopenmp '
		LABLIB=' $(ACMLDIR)/gfortran64_mp/lib/libacml_mp.a'		

	elif lib == 'MKL' and compiler == 'Intel':
		LABOPT='-O2 -openmp '
		LABLIB=' -Wl,--start-group $(MKLDIR)/mkl/lib/em64t/libmkl_intel_lp64.a $(MKLDIR)/mkl/lib/em64t/libmkl_intel_thread.a $(MKLDIR)/mkl/lib/em64t/libmkl_core.a -Wl,--end-group -openmp -lpthread'			
		
	elif lib == 'MKL' and compiler == 'Intel':
		LABOPT='-O2 '
		LABLIB=' -Wl,--start-group $(MKLDIR)/mkl/lib/em64t/libmkl_intel_lp64.a $(MKLDIR)/mkl/lib/em64t/libmkl_gnu_thread.a $(MKLDIR)/mkl/lib/em64t/libmkl_core.a  -Wl,--end-group -L$(MKLDIR)/lib/intel64/ -liomp5'
		
	elif lib == 'MKL' and compiler == 'PGI':
		LABOPT='-O3 -fast -tp=istanbul-64 -mp -Mcache_align '
		LABLIB=' -Wl,--start-group $(MKLDIR)/mkl/lib/em64t/libmkl_intel_lp64.a $(MKLDIR)/mkl/lib/em64t/libmkl_pgi_thread.a $(MKLDIR)/mkl/lib/em64t/libmkl_core.a -Wl,--end-group -mp -lpthread'		

	else:
		LABOPT ='--Not Available '
		LABLIB ='-- '

elif platform == "Nautilus":

	LABOPT ='--Not Available '
	LABLIB ='--'
else:
	LABOPT ='--Not Available '
	LABLIB ='--'


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
      <td width="500">Selected Library:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + lib + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  

   <table> 
     <tr>
      <td width="500">Selected Compiler:</td> 
     </tr>
     <tr>
      <td width = "300"></td>
      <td width = "500" > -------<b>""" + compiler + """</b>------- </td>
      <td width = "300"></td>
     </tr>
   </table>
   <hr />  

     <table align = "center" >
		<b>Use this Link Line: </b>
     </table> 

     <table> 

     <tr>
     </tr>

     <tr>
      <td width="800" border = "2">""" + LABOPT + LABLIB + """</td> 
     </tr>


   </table>

    </div>
</div>

</body>
</html>
"""


print page2




