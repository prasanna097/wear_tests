#!/system/bin/bash
sleep 2
tempString=`cat /sys/class/leds/lcd-backlight/brightness`
echo "Brightness Value : $tempString"
sleepTime=1
count=40
while [ 1 ]
do
    brightness=`cat /sys/class/leds/lcd-backlight/brightness`
    echo "Result Value : $brightness"
    echo "Count Value : $count"
    sleep 1
    count=$((count - 1))
    ((sleepTime++))
    if [ $brightness -ne 51 ] && [ $brightness -ne 102 ] && [ $brightness -ne 153 ] && [ $brightness -ne 204 ] && [ $brightness -ne 255 ]   ;   then
            break
    fi
    if [ $count -eq 0 ]    ;   then
            break
    fi
done
if [ $count -eq 0 ] ;   then
        echo "Fail" >> /data/Wearables/displayTimeoutTime.txt
else
    totalTime=$((sleepTime + 2))
    echo "Total Display Time Out ==> $totalTime" > /data/Wearables/displayTimeoutTime.txt
    if [ $totalTime -le 30 ]    ;   then
            echo "Pass" >> /data/Wearables/displayTimeoutTime.txt
    else
            echo "Fail" >> /data/Wearables/displayTimeoutTime.txt
    fi
    echo "Count :  $count"
fi
exit 0