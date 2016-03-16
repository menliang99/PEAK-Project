set lmargin 9
set bmargin 8
set rmargin 3
set tmargin 2

set ylabel "Gflops"
set xlabel "Size"
set yrange [0:]
set xrange [:]
set terminal postscript color

set style line 2

set style data lines
set datafile separator "|"

set key box linestyle 3
set key below center
set grid

set title "dgels"
set output "dgels-flops.ps"
plot \
"< sqlite3 test.db \"select * from LapackResult where routine = \'dgels\' and library = \'mkl\' and compiler = \'pgi\' ;\" " using 4:5 axes x1y1 title "mkl-pgi" with linespoints lw 2, \
"< sqlite3 test.db \"select * from LapackResult where routine = \'dgels\' and library = \'mkl\' and compiler = \'intel\' ;\" " using 4:5 axes x1y1 title "mkl-intel" with linespoints lw 2, \
"< sqlite3 test.db \"select * from LapackResult where routine = \'dgels\' and library = \'mkl\' and compiler = \'gnu\' ;\" " using 4:5 axes x1y1 title "mkl-gnu" with linespoints lw 2, \
1/0 notitle
