'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import ADB_KEYEVENT_KEYCODES
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK, SYSTEM_FILE, WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class TouchToWake(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.ambientMode = bool(int(self.arguments['--ambientMode']))
        if not self.ambientMode:
            self.testName = 'BlankToInteractive'


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        log.info('Checking/Installing the Automation APK on LW')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        log.info('Toggling the ambient mode')
        self.libObj.toggleAmbientMode(self.ambientMode)
        self.initialBrightness = self.device.getBrightness()
        log.info('Setting Brightness to max')
        self.device.setBrightness(WEARABLE_CONSTANTS.MAX_BRIGHTNESS.value)
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info('Putting Device To Suspend Mode')
            log.info('Sleeping 20 seconds')
            time.sleep(SLEEP.SLEEP_20.value)
            log.info('Getting brightness before wakeup')
            self.curAmbBrightness = self.device.readDeviceFileContent(SYSTEM_FILE.CUR_SCREEN_BRIGHTNESS_FILE.value)
            log.info('Waking Device From Suspend Mode')
            self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.DEVICE_WAKEUP.value)
            log.info('Getting brightness after wakeup')
            self.curWakeBrightness = self.device.readDeviceFileContent(SYSTEM_FILE.CUR_SCREEN_BRIGHTNESS_FILE.value)
            self.verifyResults(itrCnt)
        self.checkResult(self.passCtr, self.iteration)


    def verifyResults(self, itrCnt):
        if self.curAmbBrightness != self.curWakeBrightness :
            log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
            self.passCtr += 1
        else:
            if self.curWakeBrightness != WEARABLE_CONSTANTS.MAX_BRIGHTNESS.value :
                self.comments += 'Failed for iteration ' + str(itrCnt) + ' As the device Did not wake Up from Suspend mode'
                log.info(self.testName + 'Failed for iteration ' + str(itrCnt) + ' As the device Did not wake Up from Suspend mode')
            else:
                self.comments += 'Failed for iteration ' + str(itrCnt) + ' As the device Did not go to Suspend mode'
                log.info(self.testName + 'Failed for iteration ' + str(itrCnt) + ' As the device Did not go to Suspend mode')


    def cleanUp(self):
        if self.setUpSuccessful:
            self.device.setBrightness(self.initialBrightness)
            self.libObj.toggleAmbientMode(True)
        super().cleanUp()
