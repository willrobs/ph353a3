niter=10000
points=100
a=0.05
step=0.25
ttime=1000
mass=2
mu=10
anharm=2
corrdist=500
bootsamp=75
eecorrdist=15
d_volume=0.01
data_sets=200
mprime=1.8
muprime=10.2


python data.py $niter $points $a $step $ttime $mass $mu $anharm

python bin.py $niter $points $a $corrdist $mass $mu

python gse.py $niter $points $a $bootsamp $mass $mu

python fee.py $niter $points $a $eecorrdist $bootsamp $mass $mu

python probd.py $niter $points $a $d_volume $data_sets $mass $mu

python reweight.py $niter $points $a $eecorrdist $bootsamp $mprime $muprime $mass $mu