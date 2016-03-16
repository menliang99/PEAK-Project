#! /usr/bin/python

#********************************************************************
#     Author: Liang Men                                             *
#
# The script is not included in the PEAK website.
# It is used to update the sqlite database test.db after finishing 
# the execution on Kraken. The old performance data will be covered 
# if it has the same entry with the new one. 
# The Script generates the LapackResult.csv file containing all the
# entries in the database.  
#  
#********************************************************************

import os, sys, re, commands, pprint, glob, shutil, fnmatch,csv
import sqlite3 as lite
from string import Template

def Import_Data(main_dir, cur, con):

   #compile_dirs = ['dgemm']
   compile_dirs = ['dgemm', 'dgemv', 'daxpy', 'dgesv', 'dgetrf', 'dpotrf', 'dgels', 'dgeev', 'dsygv']
   allib = ['libsci', 'acml', 'mkl']	
   allcompiler = ['pgi', 'intel', 'gnu']

   con = lite.connect('test.db')
   cur = con.cursor()
   #cur.execute('Drop table if exists LapackResult;')
   cur.execute('CREATE TABLE IF NOT EXISTS LapackResult ( routine text, library text, compiler text, matrixsize integer, performance REAL);')
   cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS LapackResult_idx ON LapackResult(routine, library, compiler, matrixsize);')

   #cur.execute('delete from LapackResult;')

   for sub_dir in os.listdir(main_dir):
	dir_path = os.path.join(main_dir, sub_dir)
	print dir_path
	if os.path.isdir(os.path.join(main_dir, sub_dir)):

	    if sub_dir in compile_dirs:
		print '+++++' + sub_dir + '+++++'

		for lib in allib:
		    for penv in allcompiler:
			exe = sub_dir + '-' + lib + '-' + penv
			if os.path.isdir(dir_path + '/runs'):
			  for file in os.listdir(dir_path + '/runs'):
			    if fnmatch.fnmatch(file, exe + '.*'):
				print file
				for line in open(dir_path + '/runs/' + file, 'rb'):
				    if '@' in line:
					string = line.split()
					newdata = [sub_dir, lib, penv, string[1], string[3]]
					
					con.execute("insert or replace into LapackResult (routine, library, compiler, matrixsize, performance) values (?, ?, ? ,? ,?)", newdata)
		con.commit()


def Export_All_Data(filename, cur):

   data = cur.execute("SELECT * FROM LapackResult")

   with open(filename + '.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(['Routine', 'Library', 'Compiler', 'MatrixSize','Performance'])
	writer.writerows(data)
   f.close()	

def Export_Sel_Data(filename, sel, cur):

   compile_dirs = ['dgemm', 'dgemv', 'daxpy', 'dgesv', 'dgetrf', 'dpotrf', 'dgels', 'dgeev', 'dsygv']
   allib = ['libsci', 'acml', 'mkl']	
   allcompiler = ['pgi', 'intel', 'gnu']

   if sel in compile_dirs:
	data = cur.execute("SELECT * FROM LapackResult where routine = " + "'" + sel + "'" + ";")
   
   elif sel in allib:
	data = cur.execute("SELECT * FROM LapackResult where library = " + "'" + sel + "'" + ";")
	 
   elif sel in allcompiler:
	data = cur.execute("SELECT * FROM LapackResult where compiler = " + "'" + sel + "'" + ";")
   else:
	print "Error: select criterion not found!"


   with open(filename + '.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(['Routine', 'Library', 'Compiler', 'MatrixSize','Performance'])
	writer.writerows(data)
   f.close()

def Delete_Data(Rout, Lib, Comp, cur):

   compile_dirs = ['dgemm', 'dgemv', 'daxpy', 'dgesv', 'dgetrf', 'dpotrf', 'dgels', 'dgeev', 'dsygv']
   allib = ['libsci', 'acml', 'mkl']	
   allcompiler = ['pgi', 'intel', 'gnu']

   if Rout in compile_dirs:
	cur.execute("delete from LapackResult where routine = " + "'" + Rout + "'" + ";")
   
   if Lib in allib:
	cur.execute("delete from LapackResult where library = " + "'" + Lib + "'" + ";")
	 
   if Comp in allcompiler:
	cur.execute("delete from LapackResult where compiler = " + "'" + Comp + "'" + ";")

def main():

   default_main_dir = os.getcwd() + '/LAB'
   set_main_path = raw_input("Enter the main path [Default is " + default_main_dir +" ]:")
   if set_main_path == '':
	main_dir = default_main_dir
   else:
	main_dir = set_main_path

   con = lite.connect('test.db')
   cur = con.cursor()
   Import_Data(main_dir, cur, con)

   Export_All_Data('LapackResult', cur)
   Export_Sel_Data('LapackResult2', 'fft', cur)
   #Delete_Data('none', 'none', 'gnu', cur)	
   con.commit()

if __name__ == "__main__":
	main()





















