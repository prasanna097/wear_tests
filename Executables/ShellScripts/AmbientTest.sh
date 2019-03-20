brightness=`cat /sys/class/leds/lcd-backlight/brightness`
echo "Brightness Before Sleep" >> /data/Wearables/brightness.txt
echo $brightness >> /data/Wearables/brightness.txt
sleep 10s
brightness=`cat /sys/class/leds/lcd-backlight/brightness`
echo "Brightness After Sleep" >> /data/Wearables/brightness.txt
echo $brightness >> /data/Wearables/brightness.txt

if [ $brightness -ne 51 ] && [ $brightness -ne 102 ] && [ $brightness -ne 153 ] && [ $brightness -ne 204 ] && [ $brightness -ne 255 ]
    then
        echo "Pass" >> /data/Wearables/brightness.txt
else
        echo "Fail" >> /data/Wearables/brightness.txt
fi
exit 0