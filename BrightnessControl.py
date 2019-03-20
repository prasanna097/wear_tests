'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS, ADB_KEYEVENT_KEYCODES
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK, SYSTEM_FILE, WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class BrightnessControl(LinuxWearablesBaseClass):


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        log.info('Getting Current Brightness')
        self.initialBrightness = self.device.getBrightness()
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            failCount = 0
            for brightnessLevel in range(WEARABLE_CONSTANTS.BRIGHTNESS_LEVEL.value):
                options = "-w -r -e debug false -e BrightnessLevel " + str(brightnessLevel + 1) + " -e class " + self.libObj.getInstrumentationCommand(self.testName)
                log.info('Setting Brightness to Lvl ' + str(brightnessLevel + 1) + ' for iteration ' + str(itrCnt))
                output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
                log.info(output)
                self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.DEVICE_WAKEUP.value)
                log.info('Reading brightness from Device')
                curBrightness = self.device.readDeviceFileContent(SYSTEM_FILE.CUR_SCREEN_BRIGHTNESS_FILE.value)
                if "ChangeSuccessful" in output:
                    log.info("Successful - Brightness now " + str(curBrightness) + " level for Iteration : " + str(itrCnt))
                else:
                    self.comments += "Unsuccessful - Brightness now " + str(curBrightness) + " level instead of " + str(WEARABLE_CONSTANTS.BRIGHTNESS_MODES.value[brightnessLevel]) + "for Iteration : " + str(itrCnt)
                    log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
                    failCount += 1
            if not failCount:
                log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
                self.passCtr += 1
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def cleanUp(self):
        if self.setUpSuccessful:
            self.device.setBrightness(self.initialBrightness)
        super().cleanUp()
