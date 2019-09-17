#!/bin/bash
# filename: reboot_sw.sh
# Author: lufei
# Date: 20190916 16:57:38
# for reboot testing deployment
# Only appropriate for isoft sw_64 os by now



script=/tmp/reboot.sh
reboot_times=500

setting_files(){
# creating reboot script
cat > $script << EOF
#!/bin/bash
  

echo \$((\$(cat /tmp/reboot_times)-1)) > /tmp/reboot_times

if [ \$(cat /tmp/reboot_times) -gt 0 ]; then
sleep 60

echo reboot_times: \$(cat /tmp/reboot_times) >> /tmp/reboot_uptime
echo reboot_times: \$(cat /tmp/reboot_times) >> /tmp/reboot_w

uptime >> /tmp/reboot_uptime
w >> /tmp/reboot_w

echo now reboot: \$(date) >> /tmp/reboot_uptime
echo now reboot: \$(date) >> /tmp/reboot_w
reboot
fi
EOF

# Make test run on boot
echo "source $script &" >> /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local

# settings about automated login with user name test.
sed -i 's/#autologin-user=/autologin-user=test/' /etc/lightdm/lightdm.conf

# settings of test time
echo $reboot_times > /tmp/reboot_times

}

setting_files
