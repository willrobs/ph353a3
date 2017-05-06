niter=10000
points=100
a=0.05

mass=2
mu=10
bootsamp=35
eecorrdist=15
mprime=2

interval_mu=1 # check these parameters are definitely correct before running
upper_mu=0
lower_mu=0

interval_m=1
upper_m=1
lower_m=0

for m in {10..10..2}
do
  python reweight.py $niter $points $a $eecorrdist $bootsamp $interval_mu $upper_mu $lower_mu $interval_m $upper_m $lower_m $m $mu
done

