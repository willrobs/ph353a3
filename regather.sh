niter=10000
points=100
a=0.05
step=0.25
ttime=1000

mass=2
mu=10

corrdist=500
bootsamp=75
eecorrdist=15

for mu in {15..15..5}
  do

    python data.py $niter $points $a $step $ttime $mass $mu $anharm

    python bin.py $niter $points $a $corrdist $mass $mu

    python gse.py $niter $points $a $bootsamp $mass $mu

    python fee.py $niter $points $a $eecorrdist $bootsamp $mass $mu

  done
