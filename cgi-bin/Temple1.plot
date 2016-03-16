set lmargin 9
set bmargin 8
set rmargin 3
set tmargin 2

set ylabel "Gflops"
set xlabel "Size"
set yrange [0:]
set xrange [:]
set terminal postscript color

set style line 1 lt 1 lw 2 lc rgb "red"
set style line 2 lt 1 lw 2 lc rgb "blue"
set style line 3 lt 1 lw 2 lc rgb "forest-green"

set style data lines
set datafile separator "|"

set key box linestyle 3
set key below center
set grid

