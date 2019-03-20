'''
Created on Feb 13, 2018

@author: aunnikri
'''
from os.path import abspath
from os.path import join
from enum import Enum
from IOTTests.IOTConstants import IOT

#Path
class PATH(Enum):
    WEARABLE = abspath(join(abspath(IOT), "Wearables"))
    WEARABLE_EXECUTABLES = abspath(join(abspath(WEARABLE), "Executables"))
    WEARABLE_APK_PATH = abspath(join(abspath(WEARABLE_EXECUTABLES),"APK"))
    JSON_FILE_PATH = abspath(join(abspath(WEARABLE_EXECUTABLES),"wearableAPK.json"))
    WEARABLE_SHELL_SCRIPTS = abspath(join(abspath(WEARABLE_EXECUTABLES), "ShellScripts"))
    GPS_FILES_PATH = abspath(join(abspath(WEARABLE_EXECUTABLES), "GPS"))


#generalConstants
class WEARABLE_CONSTANTS(Enum):
    MAX_BRIGHTNESS = 255
    MIN_BRIGHTNESS = 51
    STATUS = ["Off", "On"]
    HOMESCREEN_ACTIVITY = "HomeActivity2"
    CHARGING_ACTIVITY = "ChargingActivity"
    BOOT_ANIMATION_ACTIVITY = "BootAnimation"
    BOOT_ACTIVITY = "BOOTACTIVITY"
    HOME_ACTIVITY = "HOMEACTIVITY"
    BRIGHTNESS_LEVEL = 5
    BRIGHTNESS_MODES = [51, 102, 153, 204, 255]
    RETRY = 20
    DATE_TIME_FORMAT = "%m%d%H%M%Y.%S"
    RESET_DATETIME = "123123592016.59"
    OPEN_ACTIVITY = [r'Selected activity for ambient mode:', r'Potential first ambient activity started:']
    CLOSE_ACTIVITY = r'Force removing'

#Files
class SYSTEM_FILE(Enum):
    DEVICE_DATA = "/data"
    SDCARD = "/sdcard"
    DEVICE_WEARABLE_FOLDER = "/data/Wearables"
    COMP_MUSIC_FOLDER = "/sdcard/Music"
    LOW_POWER_TEST_FOLDER = "/data/Wearables/LowPowerStateTest"
    DEVICE_TIMEOUT = "displayTimeoutTime.txt"
    BRIGHTNESS = "brightness.txt"
    SYSTEM_FRAMEWORK = "/system/framework"
    VIDEO_PLAYBACK_RESULT_FILE = "/data/data/com.android.mediaframeworktest/files/multiMediaTestResult.txt"
    ETC_PERMISSION = "/etc/permissions"
    SYSTEM_ETC_PERMISSION = "/system/etc/permissions"
    SYSTEM_VENDOR_LIB = "/system/vendor/lib"
    SYSTEM_GPS = "/system/app/ODLT"
    CUR_SCREEN_BRIGHTNESS_FILE = "/sys/class/leds/lcd-backlight/brightness"
    ACTIVITY = {
                "STOPWATCH" : "com.google.android.deskclock/com.google.android.wearable.deskclock.stopwatch.StopwatchRoundActivity",
                "ALARM" : "com.google.android.deskclock/com.google.android.wearable.deskclock.alarm.ChooseAlarmTimeRoundActivity",
                "SETTINGS" : "com.google.android.apps.wearable.settings/com.google.android.clockwork.settings.MainSettingsActivity",
                "POP_PLAYER" : "com.estrongs.android.pop/.view.FileExplorerActivity",
                "ESEXPLORER" : "com.estrongs.android.pop/com.estrongs.android.pop.view.FileExplorerActivity"
                }
    PACKAGE = {
                "POP_PLAYER" : "com.estrongs.android.pop",
                "POWERTEST": "com.google.android.powertests",
                "MUSIC_PLAYER" : "jp.flatlib.flatlib3.musicplayerw",
                "VIDEO_PLAYER" : "com.qualcomm.mediaplayer",
                "GPS_TEST" : "com.android.aptgpstest",
                "MULTIMEDIA_FRAMEWORK" : "com.android.mediaframeworktest",
                "WEAR_OS" : "com.google.android.wearable.app"
              }

class POWER_TEST(Enum):
    LOW_RESOLUTION_STATIC = ["LowResStaticDisplayTest#testStaticDisplay", "PowerDisplayLowResTestActivity"]
    STATIC = ["StaticDisplayTest", "PowerDisplayTestActivity"]
    ANIMATED = ["AnimatedDisplayTest", "PowerAnimatedImageTestActivity"]


# For Instrumentation Commands
class INSTRUMENTATION(Enum):
    AUTOMATION_PACKAGE = "com.qualcomm.linuxwearables."
    TEST_RUNNER = "test/android.support.test.runner.AndroidJUnitRunner"
    CLICK_ME = "#clickMe "
    TEST_CASE_INSTRUMENTATION_ARGUMENTS ={
                                    "Stopwatch" : "Stopwatch",
                                    "AmbientTest" : "AmbientLW",
                                    "DeviceInfo" : "DeviceInfo",
                                    "Alarm" : "Alarm",
                                    "TakeBugReport" : "TakeBugReport",
                                    "SetTimer" : "SetTimer",
                                    "AudioCompDelete" : "PlayMusicCompanionDeleteMusic",
                                    "AudioCompSync" :  "PlayMusicCompanion",
                                    "AudioLWPlay" : "PlayMusic",
                                    "ConnectWifi" : "ConnectWifiLW",
                                    "CheckWifi" : "CheckWifiLW",
                                    "CompWifi" : "CompWifiPass",
                                    "LowPowerTest" : "LowPowerTest",
                                    "DeviceSearch" : "BTSearch",
                                    "BTPairingLW" : "BTPairLWSetup",
                                    "BTPairing" : "BTPairCompanion",
                                    "CompReconnect" : "LWReconnect",
                                    "PowerOff" : "PowerOff",
                                    "BatteryGauge" : "BatteryGauge",
                                    "GPSOn" : "GPS",
                                    "WatchFaceChangeTest" : "WatchfaceChange",
                                    "GPSCheck" : "GPSCheck",
                                    "BrightnessControl" : "BrightnessCheck",
                                    "AmbientCompanionTest" : "AmbientComp",
                                    "VideoPlaybackFile" : "-a android.intent.action.VIEW --ez android.intent.extra.START_PLAYBACK true -d file:////sdcard/",
                                    "VideoPlayback" : "-n com.estrongs.android.pop/.app.PopVideoPlayer"
                                    }


#APK Lists
class APK(Enum):
    AUTOMATION_APK = ["app-debug.apk", "app-debug-androidTest.apk"]
    ESEXPLORER_APK = "esExplorer.apk"
    MEDIAPLAYER_APK = "MediaPlayer.apk"
    MULTIMEDIA_PLAYER_APK = "MultimediaFrameworkTest.apk"
    POWER_TEST = "PowerTests.apk"
    LW_AUDIO = "AudioWearable.apk"
    COMPANION_AUDIO = "AudioCompanion.apk"
    GPS_APK = "AndroidGPSTest.apk"

class SHELL_SCRIPTS(Enum):
    ACTIVITY_LAUNCH_TEST = "ActivityLaunchTest.sh"
    DISPLAY_TIMEOUT_TEST = "DisplayTimeoutLW.sh"
    AMBIENT_USB_TEST = "AmbientTest.sh"

class UI_ACTIVITY(Enum):
    HOMEACTIVITY = ["HomeActivity2", "ChargingActivity"]
    BOOTACTIVITY = ["BootAnimation"]

class GPS_FILE(Enum):
    QTI_LOCATION_JAR = "com.qti.location.sdk.jar"
    QTI_LOCATION_XML = "com.qti.location.sdk.xml"
    LIB_SO = "libdiagbridge.so"
    OLDT_APK = "ODLT.apk"
    QMAP = "qmapbridge.jar"
    QCOM_QMAP = "com.qualcomm.qmapbridge.xml"
    QCOM_LOCAION = "com.qualcomm.location.xml"
