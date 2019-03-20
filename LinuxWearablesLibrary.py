'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging
import time
from os.path import abspath
from os.path import join
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.JsonUtility import JsonUtility
from IOTTests.Wearables.LinuxWearablesConstants import SYSTEM_FILE, INSTRUMENTATION, WEARABLE_CONSTANTS, PATH


log = logging.getLogger(__name__)


class LinuxWearablesLibrary(object):

    def __init__(self, device):
        self.device = device

    def buildPath(self, dir, data):
        return (abspath(join(abspath(dir), data)))

    def getInstrumentationCommand(self, className):
        '''
        Gets the classname of the APK automation script
        :param className: Acts as key to dictionary that contains the classnames
        :return:
        '''
        return INSTRUMENTATION.AUTOMATION_PACKAGE.value + INSTRUMENTATION.TEST_CASE_INSTRUMENTATION_ARGUMENTS.value[className] + INSTRUMENTATION.CLICK_ME.value + INSTRUMENTATION.AUTOMATION_PACKAGE.value + INSTRUMENTATION.TEST_RUNNER.value


    def checkAndInstallAPK(self, apklist, dev = 'LW', mandatory = False):
        '''
        This functions checks if the APK is already installed or not, if not then installs the APK
        :param apk: The APK to be installed
        :return:
        '''
        try:
            config = JsonUtility.readJsonFile(PATH.JSON_FILE_PATH.value)
            for apk in apklist:
                if mandatory or not config[dev][apk]:
                    log.info('APK ' + apk + ' Installing it now')
                    installAPK = abspath(join(abspath(PATH.WEARABLE_APK_PATH.value), apk))
                    self.device.installApp(installAPK)
                    config[dev][apk] = True
                    JsonUtility.writeJsonFile(config, PATH.JSON_FILE_PATH.value)
                else:
                    log.info('APK ' + apk + ' Already Installed')
        except FileNotFoundError:
            for apk in apklist:
                self.device.installAPK(apk)


    def checkAndPush(self, resourceLocation, deviceLocation, binary):
        '''
        This functions creates a directory if not present and then pushes the required file
        :param resourceLocation: Source of the resource
        :param deviceLocation: Destination of the resource
        :param binary: resource name
        :return:
        '''
        self.device.makeDirectoryOnDevice(deviceLocation)
        resource = abspath(join(abspath(resourceLocation), binary))
        if self.device.doesResourceExist(deviceLocation + '/' + binary):
            log.info("Binary Already Present")
        else:
            log.info("Pushing Binary")
            self.device.pushResource(resource, deviceLocation)
            self.device.giveRootPermission(deviceLocation + '/' + binary)


    def isAmbientModeSet(self):
        '''
        To check if the device is in Ambient Mode or not
        :return:
        '''
        time.sleep(SLEEP.SLEEP_30.value)
        brightness = int(self.device.readDeviceFileContent(SYSTEM_FILE.CUR_SCREEN_BRIGHTNESS_FILE.value))
        return (brightness != 0)


    def inAmbientMode(self):
        '''
        Checks if the Device is in Ambient Mode or Interactive Mode
        :return:
        '''
        brightness = int(self.device.readDeviceFileContent(SYSTEM_FILE.CUR_SCREEN_BRIGHTNESS_FILE.value))
        if brightness in WEARABLE_CONSTANTS.BRIGHTNESS_MODES.value:
            return False
        return True


    def toggleAmbientMode(self, enable):
        '''
        To change the Ambient mode settings of the device
        :param enable: 1/0
        :return:
        '''
        mode = WEARABLE_CONSTANTS.STATUS.value[enable]
        options = "-w -r -e debug false -e Mode " + mode + " -e class " + self.getInstrumentationCommand("AmbientTest")
        self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)


    def setTime(self, curTime):
        log.info('Setting time on ' + self.device.getDeviceId())
        self.device.executeCommandOnDevice('su 0 toybox date ' + curTime)
        log.info('Sleeping for 10 Seconds')
        time.sleep(SLEEP.SLEEP_10.value)


    def getDateAndTime(self):
        command = 'date +%d/%m/%Y::%H:%M:%S'
        time = self.device.executeCommandOnDevice(command)
        log.info('Time on ' + self.device.getDeviceId() + ' : ' + time)
        return time

    def toggleBluetooth(self, on=True):
        key = 8
        if on:
            key = 6
        command = "service call bluetooth_manager " + str(key)
        self.device.executeCommandOnDevice(command)

    def doFDR(self, iotLibObj):
        if not iotLibObj.enterBootLoader(self.device.getDeviceId()):
            log.info('Failed, Device is not moved to Fastboot mode')
            return False
        log.info('Resetting the Device')
        self.device.factoryDataReset()
        deviceUp = iotLibObj.exitBootLoader(["WelcomeActivity"])
        if deviceUp:
            return True
        log.info("Device Did not exit bootloader mode")
        return False