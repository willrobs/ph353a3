niter=10000
points=100
a=0.05

mass=2
bootsamp=35
eecorrdist=15
mprime=2

interval=2
upper=2
lower=2

for mu in {5..40..5}
do
  python reweight.py $niter $points $a $eecorrdist $bootsamp $interval $upper $lower $mass $mu
done

