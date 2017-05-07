niter=10000
points=300
a=0.1
step=0.25
ttime=500
mass=2
mu=10
corrdist=500
bootsamp=75
eecorrdist=20
d_volume=0.01
data_sets=200
mprime=2
muprime=10.2


python shodata.py $niter $points $a $step $ttime $mass $mu

python shobin.py $niter $points $a $corrdist $mass $mu

python shogse.py $niter $points $a $bootsamp $mass $mu

python shofee.py $niter $points $a $eecorrdist $bootsamp $mass $mu

python shoprobd.py $niter $points $a $d_volume $data_sets $mass $mu

python shoreweight.py $niter $points $a $eecorrdist $bootsamp $mprime $muprime $mass $mu