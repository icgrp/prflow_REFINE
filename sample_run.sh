#####################################
## Rendering, no identical version ##
#####################################
# mkdir -p incr_mono_RND
mkdir -p incr_NoC_RND

# cp Makefile_RND Makefile

# NoC->Monolithic version
make clear_incr
source send_static.sh
sleep 10
ssh -i ~/.ssh/id_rsa_zcu102 root@10.10.7.1 "cd /run/media/mmcblk0p1/; rm -rf __static_loaded__; /sbin/reboot"

make incr_NoC | tee incr_NoC_RND.txt
cp -r ./input_src/rendering/  ./incr_NoC_RND/
mv incr_NoC_RND.txt ./incr_NoC_RND/


# Monolithic only version
make clear_incr
source send_static.sh
sleep 10
ssh -i ~/.ssh/id_rsa_zcu102 root@10.10.7.1 "cd /run/media/mmcblk0p1/; rm -rf __static_loaded__; /sbin/reboot"

make incr_mono | tee incr_mono_RND.txt
cp -r ./input_src/rendering/  ./incr_mono_RND/
mv incr_mono_RND.txt ./incr_mono_RND/