#! /usr/bin/python

#********************************************************************
#     Author: Liang Men                                             *
#
# The Subfunction of PEAK is used to compile the benchmarks of the 
# numerical functions. Each numerical benchmark has an independent 
# directory under the main directory. 
#  
#********************************************************************

import os, sys, re, commands, pprint, glob, shutil
from string import Template

##############################Compile JOBS configuration#######################################
def conf_module(lib, compiler, FILE):

	if lib == 'libsci' and compiler == 'pgi':
		FILE.write("module unload PrgEnv-pgi\n")			
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-pgi\n")
	
	elif lib == 'libsci' and compiler == 'intel':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-intel\n")

	elif lib == 'libsci' and compiler == 'gnu':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-gnu\n")

	elif lib == 'acml' and compiler == 'pgi':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-pgi\n")
		FILE.write("module unload xt-libsci\n")
		FILE.write("module load acml\n")

	elif lib == 'acml' and compiler == 'intel':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-intel\n")
		FILE.write("module unload xt-libsci\n")
		FILE.write("module unload acml\n")
		FILE.write("module load acml\n")

	elif lib == 'acml' and compiler == 'gnu':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-gnu\n")
		FILE.write("module unload xt-libsci\n")
		FILE.write("module unload acml\n")
		FILE.write("module load acml\n")

	elif lib == 'mkl' and compiler == 'intel':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-intel\n")
		FILE.write("module unload xt-libsci\n")
		#FILE.write("module unload acml'")
		#FILE.write("module load acml'")

	elif lib == 'mkl' and compiler == 'gnu':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-gnu\n")
		FILE.write("module unload xt-libsci\n")

	elif lib == 'mkl' and compiler == 'pgi':
		FILE.write("module unload PrgEnv-pgi\n")		
		FILE.write("module unload PrgEnv-intel\n")	
		FILE.write("module unload PrgEnv-gnu\n")
		FILE.write("module load PrgEnv-pgi\n")
		FILE.write("module unload xt-libsci\n")

	else:
		print 'Error: Library or Compiler not found'


##############################Compile JOBS configuration#######################################

def conf_platform(lib, compiler, ACMLDIR, MKLDIR):

	if lib == 'libsci' and compiler == 'pgi':
 		LABOPT ='-O3 -fast '
		LABLIB =''
	elif lib == 'libsci' and compiler == 'intel':
		LABOPT='-O3 '
		LABLIB=''
	elif lib == 'libsci' and compiler == 'gnu':
		LABOPT='-O3 '
		LABLIB=''	

	elif lib == 'acml' and compiler == 'pgi':
		LABOPT='-O3 -fast -tp=istanbul-64 -mp -Mcache_align '
		LABLIB=' ' + ACMLDIR + '/pgi64_mp/lib/libacml_mp.a'	

	elif lib == 'acml' and compiler == 'intel':
		LABOPT='-O3 '
		LABLIB=' ' + ACMLDIR + '/ifort64_mp/lib/libacml_mp.a -openmp -lpthread'		

	elif lib == 'acml' and compiler == 'gnu':
		LABOPT='-O3 -fopenmp '
		LABLIB=' ' + ACMLDIR + '/gfortran64_mp/lib/libacml_mp.a'		

	elif lib == 'mkl' and compiler == 'intel':
		LABOPT='-O2 -openmp '
		LABLIB=' -Wl,--start-group ' + MKLDIR + '/mkl/lib/em64t/libmkl_intel_lp64.a ' + MKLDIR + '/mkl/lib/em64t/libmkl_intel_thread.a ' + MKLDIR + '/mkl/lib/em64t/libmkl_core.a -Wl,--end-group -openmp -lpthread'			
		
	elif lib == 'mkl' and compiler == 'gnu':
		LABOPT='-O2 '
		#LABLIB=' -Wl,--start-group -I' + MKLDIR + '/mkl/lib/em64t/ -Wl,--end-group -L' + MKLDIR + '/lib/intel64/ -liomp5'
		LABLIB=' -Wl,--start-group ' + MKLDIR + '/mkl/lib/em64t/libmkl_intel_lp64.a ' + MKLDIR + '/mkl/lib/em64t/libmkl_intel_thread.a ' + MKLDIR + '/mkl/lib/em64t/libmkl_core.a -Wl,--end-group  -L' + MKLDIR + '/lib/intel64/ -liomp5'	
		#LABLIB= ' -L'+ MKLDIR + '/mkl/lib/em64t -Wl, -R' + MKLDIR + '/mkl/lib/em64t -lmkl_lapack -lmkl_intel_lp64 -lmkl_gnu_thread -lmkl_core -lmkl_sequential -lm'
		
	elif lib == 'mkl' and compiler == 'pgi':
		LABOPT='-O3 -fast -tp=istanbul-64 -mp -Mcache_align '
		LABLIB=' -Wl,--start-group ' + MKLDIR + '/mkl/lib/em64t/libmkl_intel_lp64.a ' + MKLDIR + '/mkl/lib/em64t/libmkl_pgi_thread.a ' + MKLDIR + '/mkl/lib/em64t/libmkl_core.a -Wl,--end-group -mp -lpthread'		

	else:
		print 'Error: Library or Compiler not found'

	return LABOPT, LABLIB

############################## COMPILE JOBS sub function #######################################

def routine_compile(dir_path, sub_dir, lib, penv, ACMLDIR, MKLDIR):

	scriptname = "compile.sh"
	FILE = open(scriptname, "w")
	FILE.write("#!/bin/csh \n\n")
	conf_module(lib, penv, FILE)
	LABOPT, LABLIB = conf_platform(lib, penv, ACMLDIR, MKLDIR)

	print '\t\t****' + lib + '-' + penv + '****'
	exe = sub_dir + '-' + lib + '-' +penv
	compiling = 'ftn ' + LABOPT + '-o '+ dir_path + '/' + exe +' ' + dir_path + '/timing_'+ sub_dir +'.f90' + LABLIB


	FILE.write("\n"+compiling +"\n")
	FILE.close()

	os.system('chmod 755 compile.sh')
	print compiling
	os.system('./compile.sh')
	os.system('rm -rf compile.sh')

############################## COMPILE JOBS sub function #######################################
def hpl_compile(dir_path, sub_dir, lib, penv, ACMLDIR, MKLDIR):

	print '\t\t****' + 'HPL-' + lib + '-' + penv + '****'
	os.system('rm -f '+ dir_path + '/Make.' + lib + '-' + penv)
	Makefilename = 'Make.' + lib + '-' + penv
	MAKEFILE = open(Makefilename, "w")
	LABOPT, LABLIB = conf_platform(lib, penv, ACMLDIR, MKLDIR)
	MAKEFILE.write ("ARCH =" + lib + "-" + penv + "\n")
	MAKEFILE.write ("LABOPT =" + LABOPT + "\n")
	MAKEFILE.write ("LABLIB =" + LABLIB + "\n")
	MAKEFILE.close()
	os.system ('mv ' + Makefilename +' '+ dir_path + '/' + Makefilename)
	print ('mv ' + Makefilename +' '+ dir_path + '/' + Makefilename)

	scriptname = "compile.sh"
	FILE = open(scriptname, "w")
	FILE.write("#!/bin/csh \n\n")


	FILE.write("cat Make.LAB >> "+ Makefilename + "\n")
	conf_module(lib, penv, FILE)
	FILE.write("pwd\n")
	FILE.write("make arch=" + lib + "-" +  penv + " clean_arch" + "\n")	
	FILE.write("make arch=" + lib + "-" +  penv + "\n")
	#FILE.write("rm -rf " + Makefilename + "\n")
	FILE.close()
	os.system('chmod 755 compile.sh')
	os.system('mv '+scriptname + ' '+ dir_path + '/'+scriptname)


	main_dir = os.getcwd()
	print main_dir
	os.chdir( dir_path)

	os.system('./compile.sh')
	os.chdir(main_dir)

	os.system('rm -rf compile.sh')

############################## COMPILE JOBS #######################################
def compile_jobs (main_dir, compile_dirs, allib, allcompiler, ACMLDIR, MKLDIR):


   #print main_dir
   for sub_dir in os.listdir(main_dir):
	dir_path = os.path.join(main_dir, sub_dir)
	print dir_path
	if os.path.isdir(os.path.join(main_dir, sub_dir)):

	    if sub_dir in compile_dirs:
		print '+++++' + sub_dir + '+++++'
		os.system('rm -f '+ '*.o ')

		for lib in allib:
		    print '\t====' + lib + '====='
		    for penv in allcompiler:
			routine_compile(dir_path, sub_dir, lib, penv, ACMLDIR, MKLDIR)

	    elif sub_dir == 'hpl-2.0--':
		print '\n\n+++++' + sub_dir + '+++++\n\n'
		for lib in allib:
		    print '\t====' + 'HPL-' + lib + '====='
		    for penv in allcompiler:
			hpl_compile(dir_path, sub_dir, lib, penv, ACMLDIR, MKLDIR)























