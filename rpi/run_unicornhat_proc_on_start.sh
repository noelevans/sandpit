#! /bin/sh
# /etc/init.d/run_unicornhat_proc_on_start.sh 
#

# Run this when starting RPi. This file must be copied to
# /etc/init.d/
# and run
# sudo chmod 755 /etc/init.d/run_unicornhat_proc_on_start.sh
# sudo update-rc.d run_unicornhat_proc_on_start.sh defaults
#
# Refer to this for guidance:
# https://unix.stackexchange.com/questions/56957/

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    sudo python all_lines_status.py
    ;;
  *)
    echo "Usage: /etc/init.d/run_unicornhat_proc_on_start.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
