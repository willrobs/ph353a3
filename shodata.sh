niter=10000
points=300
a=0.1
step=0.25
ttime=5000

m=2
mu=10

corrdist=500
bootsamp=75
eecorrdist=25

for mu in {30..30..10}
  do

    python shodata.py $niter $points $a $step $ttime $m $mu 

    python shobin.py $niter $points $a $corrdist $m $mu

    python shogse.py $niter $points $a $bootsamp $m $mu

    python shofee.py $niter $points $a $eecorrdist $bootsamp $m $mu

  done
