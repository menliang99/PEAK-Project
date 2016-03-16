#! /usr/bin/python

#********************************************************************
#     Author: Liang Men                                             *
#
# The Subfunction of PEAK is used to execute the benchmark of the  
# numerical functions. Each numerical benchmark has an independent 
# directory under the main directory. The matrixsizes are an input
# parameter from the main function.
# The script creates a /runs directory under the numerical directory,
# which includes the PBS files for Kraken and the execution results. 
#  
#********************************************************************

import os, sys, re, commands, pprint, glob,shutil
from string import Template

def qsubs(sub_dir,exe, dir_path, startnum, totalnum, stepnum):

	newpath = dir_path + "/runs"
	if not os.path.isdir(newpath):
	    os.makedirs(newpath)

	pbsfilename = 'job-' + exe + '.pbs'	
	PBSFILE = open(pbsfilename, "w")
	PBSFILE.write ("#PBS -N" + exe + "\n")
	PBSFILE.write ("#PBS -A UT-SUPPORT " + "\n")
	PBSFILE.write ("#PBS -j oe" + "\n")
	PBSFILE.write ("#PBS -l walltime=2:00:00,size=12" + "\n")
	#PBSFILE.write ("#PBS -q debug" + "\n")
	#print os.getcwd()
	#print dir_path
	PBSFILE.write ("cd " + newpath + "\n")
	PBSFILE.write ("export OMP_NUM_THREADS=12" + "\n")
	PBSFILE.write ("export MKL_NUM_THREADS=12" + "\n")

	i = startnum

	while (i <= totalnum):
		PBSFILE.write ("aprun -n 1 -d 12 ../" + exe + " " + str(i) + "\n" )
		if sub_dir == 'daxpy':
			i = i * stepnum
		elif sub_dir == 'dgemv':
			i = i * stepnum
		else:
			i = i + stepnum			
	PBSFILE.close()
	shutil.move(os.getcwd()+"/"+pbsfilename, newpath+"/"+pbsfilename)

	main_dir = os.getcwd()

	os.chdir(newpath)

	#print os.getcwd()

	os.system('qsub job-' + exe + '.pbs')
	#os.system('rm -rf *.pbs')
	os.chdir(main_dir)

def conf_par(sub_dir, compile_dirs, routine_params):

	dd = dict(zip(compile_dirs,routine_params))
   	globals().update(dd)

   	#for l in compile_dirs:
	#	print eval(l)

	startnum = eval(sub_dir)[0]
	totalnum = eval(sub_dir)[1]
	stepnum = eval(sub_dir)[2]

	return startnum, totalnum, stepnum
'''
	if sub_dir == 'dgemm':
		startnum = 1000
		totalnum = 10000
		stepnum = 1000

	elif sub_dir == 'dgemv':
		startnum = 2000
		totalnum = 140000
		stepnum = 2000

	elif sub_dir == 'daxpy':
		startnum = 10000000
		totalnum = 80000000
		stepnum = 10000000

	elif sub_dir == 'dgesv':
		startnum = 1000
		totalnum = 10000
		stepnum = 1000

	elif sub_dir == 'dgetrf':
		startnum = 2000
		totalnum = 16000
		stepnum = 2000

	elif sub_dir == 'dpotrf':
		startnum = 2000
		totalnum = 16000
		stepnum = 2000

	elif sub_dir =='dgels':
		startnum = 2000
		totalnum = 16000
		stepnum = 2000

	elif sub_dir == 'dgeev':
		startnum = 1000
		totalnum = 8000
		stepnum = 1000

	elif sub_dir == 'dsygv':
		startnum = 500
		totalnum = 8000
		stepnum = 1000
	else:
		print "Lapack routine path no found!"
'''	



def execute_jobs(main_dir, compile_dirs, allib, allcompiler, routine_params):

   #print main_dir
   for sub_dir in os.listdir(main_dir):
	dir_path = os.path.join(main_dir, sub_dir)
	print dir_path
	if os.path.isdir(os.path.join(main_dir, sub_dir)):

	    if sub_dir in compile_dirs:
		print '+++++' + sub_dir + '+++++'
		os.system('rm -f '+ '*.o '+' *.pbs')

		for lib in allib:
		    print '\t====' + lib + '====='
		    for penv in allcompiler:
			exe = sub_dir + '-' + lib + '-' + penv
			if os.path.isfile(dir_path + '/' + exe):
				startnum, totalnum, stepnum  = conf_par(sub_dir, compile_dirs, routine_params)			
				qsubs(sub_dir, exe, dir_path, startnum, totalnum, stepnum)	
			else:
				print "Compiling not finished for " + exe + "!" 	


	    elif sub_dir == 'hpl-2.0--':
		print '\n\n+++++' + sub_dir + '+++++\n\n'

		for lib in allib:
		    print '\t====' + 'HPL-' + lib + '====='
		    for penv in allcompiler:
	
			root_dir = os.getcwd()
			hpl_dir = root_dir + '/' + dir_path

			bin_dir = hpl_dir + '/bin/' + lib + '-' + penv

			os.chdir(bin_dir)

			if os.path.isfile(bin_dir + '/HPL.pbs'):
				os.remove(bin_dir + '/HPL.dat')
				shutil.copy2(hpl_dir+'/HPL.dat', bin_dir+'/HPL.dat')			
			else:
				shutil.copy2(hpl_dir+'/HPL.dat', bin_dir+'/HPL.dat')

			if os.path.isfile(bin_dir + '/HPL.pbs'):
				os.remove(bin_dir + '/HPL.pbs')
				shutil.copy2(hpl_dir+'/HPL.pbs', bin_dir+'/HPL.pbs')			
			else:
				shutil.copy2(hpl_dir+'/HPL.pbs', bin_dir+'/HPL.pbs')


			if os.path.isfile(bin_dir + '/xhpl'):
			     os.system("qsub HPL.pbs")
			else:
			     print "ERROR: XHPL file does not exist in" + bin_dir + "!"

			os.chdir(root_dir)






















