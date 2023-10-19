echo "****************************************************"
echo "\t\tTRACKING"
echo "****************************************************"
echo ""

sudo systemctl stop pigpiod
export GPIOZERO_PIN_FACTORY=pigpio

echo "PiGPIO démarré"
echo ""
echo "Voulez vous avec ou sans GUI (O/n)"
read userInput_1 
if userInput_1 == 'n'
then
sudo pigpiod
python3 nogui_pimotorft.py
else
sudo pigpiod
python3 nogui_pimotorft.py
fi


