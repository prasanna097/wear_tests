#!/system/bin/sh
#
sleep 5
am start -n com.google.android.deskclock/com.google.android.wearable.deskclock.alarm.ChooseAlarmTimeRoundActivity
sleep 5
am start -n com.google.android.apps.wearable.settings/com.google.android.clockwork.settings.MainSettingsActivity
sleep 5
am start -n com.google.android.deskclock/com.google.android.wearable.deskclock.stopwatch.StopwatchRoundActivity
sleep 5

am force-stop com.google.android.deskclock
am force-stop com.google.android.apps.wearable.settings
am force-stop com.google.android.deskclock
exit 0
