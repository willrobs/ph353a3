niter=10000
points=300
a=0.1

m=2
#mu=10
bootsamp=35
eecorrdist=15
mprime=2

interval_mu=5 # check these parameters are definitely correct before running
upper_mu=0
lower_mu=5

interval_m=1
upper_m=0
lower_m=0

for mu in {10..10..10}
do
  python shoreweight.py $niter $points $a $eecorrdist $bootsamp $interval_mu $upper_mu $lower_mu $interval_m $upper_m $lower_m $m $mu
done

