#! /usr/bin/python


#********************************************************************
#     Author: Liang Men                                             *
#
# The Subfunction of PEAK is used to sweep the tempory files in the 
# main directory. Attention the /runs direcotry contains the previous
# results and .pbs files for Kraken.  
#  
#********************************************************************

import os, sys, re, commands, pprint, glob,shutil
from string import Template


def clean_jobs(main_dir, compile_dirs, allib, allcompiler):

   #print main_dir
   for sub_dir in os.listdir(main_dir):
	dir_path = os.path.join(main_dir, sub_dir)
	print dir_path
	if os.path.isdir(os.path.join(main_dir, sub_dir)):

	    if sub_dir in compile_dirs:
		print '+++++' + sub_dir + '+++++'
		print 'rm -f '+ dir_path +'/*.o '
		print 'rm -f '+ dir_path +'/*.mod '
		print 'rm -rf '+ dir_path + '/runs'
		print 'rm -f '+ dir_path + '/build.sh'

		os.system('rm -f '+ dir_path +'/*.o ')
		os.system('rm -f '+ dir_path +'/*.mod ')
		os.system('rm -rf '+ dir_path + '/runs')
		os.system('rm -f '+ dir_path + '/build.sh')

		for lib in allib:
		    for penv in allcompiler:
			exe = sub_dir + '-' + lib + '-' + penv
			os.system('rm -rf ' + dir_path + '/' + exe)  
			print 'rm -rf ' + dir_path + '/' + exe

	    elif sub_dir == 'hpl-2.0':
		print '\n\n+++++' + sub_dir + '+++++\n\n'
	
		root_dir = os.getcwd()
		hpl_dir = root_dir + '/' + dir_path
		os.chdir(hpl_dir)

		for lib in allib:
		    for penv in allcompiler:
			if os.path.isfile (hpl_dir + '/Make.' + lib + '-' + penv):
				print 'make arch=' + lib + '-' + penv + ' clean'
				os.system ('make arch=' + lib + '-' + penv + ' clean')
				print 'remove ' + hpl_dir + '/Make.' + lib + '-' + penv
				os.remove(hpl_dir + '/Make.' + lib + '-' + penv)
			
		print 'rm -f runjobs.sh'
		print 'rm -rf lib/*'
		os.system('rm -f runjobs.sh')
		os.system('rm -rf lib/*')
		print 'rm -rf bin/*'
		os.system('rm -rf bin/*')
			
		os.chdir(root_dir)






















