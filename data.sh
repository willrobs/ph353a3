niter=10000
points=100
a=0.05
step=0.18
ttime=1000

m=2
mu=10

corrdist=500
bootsamp=75
eecorrdist=15

for m in {2..10..2}
  do

    python data.py $niter $points $a $step $ttime $m $mu $anharm

    python bin.py $niter $points $a $corrdist $m $mu

    python gse.py $niter $points $a $bootsamp $m $mu

    python fee.py $niter $points $a $eecorrdist $bootsamp $m $mu

  done
