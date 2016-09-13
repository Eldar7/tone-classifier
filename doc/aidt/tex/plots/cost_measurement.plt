set term png
set key outside
set key right top
set grid
set xrange [0.1:1]
set xtics 0.1,0.1,1
set yrange [0.36:0.52]
set ytics 0.36,0.01,0.52
set xlabel "SVM 'Cost' Parameter Value"
set ylabel "F-macro(neg, pos)"

set output "pics/2015_bank_balanced.png"
plot "2015_bank_balanced.dat" using 1:2 with linespoints title "BANK_01", \
    "2015_bank_balanced.dat" using 1:3 with linespoints title "BANK_02", \
    "2015_bank_balanced.dat" using 1:4 with linespoints title "BANK_03", \
    "2015_bank_balanced.dat" using 1:5 with linespoints title "BANK_04", \
    "2015_bank_balanced.dat" using 1:6 with linespoints title "BANK_05"

set output "pics/2015_ttk_balanced.png"
plot "2015_ttk_balanced.dat" using 1:2 with linespoints title "TCC_01", \
    "2015_ttk_balanced.dat" using 1:3 with linespoints title "TCC_02", \
    "2015_ttk_balanced.dat" using 1:4 with linespoints title "TCC_03", \
    "2015_ttk_balanced.dat" using 1:5 with linespoints title "TCC_04", \
    "2015_ttk_balanced.dat" using 1:6 with linespoints title "TCC_05"
