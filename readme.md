1. copy XinyingS7_Install.sh into /home/pi/Documents/
2. chmod 777 XinyingS7_Install.sh
3. ./XinyingS7_Install.sh
4. sudo nano /home/pi/.bashrc, and add  the following commandlines at the end.
	echo Running at boot
	sh /home/pi/SIM7600_NDIS/sim7600_4G_hat_init
	sudo /usr/bin/python3 /home/pi/Documents/Xinying_demo01/dial.py
	sleep 2 
	sudo python3 /home/pi/Documents/Xinying_demo01/s7readApp.py

5. sudo raspi-config->1.System options->Select->Boot/ Auto Login-> B2 Console Autologin Text console
   ->OK->Finish-> would you like to reboot now? Yes
