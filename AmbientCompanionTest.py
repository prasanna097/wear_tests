'''
Created on Apr 4, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS, ADB_KEYEVENT_KEYCODES
from IOTTests.IOTLibrary import IOTLibrary
from IOTTests.IOTConstants import SLEEP, FILE
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary
from IOTTests.Wearables.LinuxWearablesConstants import APK, WEARABLE_CONSTANTS, SYSTEM_FILE

log = logging.getLogger(__name__)

class AmbientCompanionTest(LinuxWearablesBaseClass):


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        log.info('Checking/Installing the Automation APK on companion')
        compLibObj = LinuxWearablesLibrary(self.campDevice)
        compLibObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'comp')
        log.info('Turning On Bluetooth in Wearable')
        self.compIotLibObj = IOTLibrary(self.campDevice)
        log.info('Creating Screenshot folder in Companion and Wearable To Collect Logs')
        self.campDevice.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        self.device.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        self.libObj.toggleBluetooth(True)
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            initialAmbientMode = self.libObj.isAmbientModeSet()
            log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Turning it : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode ^ True])
            initialAmbientMode ^= True
            if self.toggleAmbientMode(initialAmbientMode, itrCnt):
                initialAmbientMode ^= True
                if self.toggleAmbientMode(initialAmbientMode, itrCnt):
                    self.passCtr += 1
                    log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode ^ True] + "/" + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Successful for Iteration ' + str(itrCnt))
        self.campDevice.executeAmCommand(AM_SUB_COMMANDS.FORCE_STOP.value, ' ' + SYSTEM_FILE.PACKAGE.value['WEAR_OS'])
        self.compIotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def toggleAmbientMode(self, initialAmbientMode, itrCnt):
        options = "-w -r -e debug false " + '-e DeviceId ' + self.device.getDeviceId() + ' -e Mode ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + " -e class " + self.libObj.getInstrumentationCommand(self.testName)
        output = self.campDevice.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
        log.info(output)
        self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.BACK.value)
        self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.BACK.value)
        time.sleep(SLEEP.SLEEP_10.value)
        if self.libObj.isAmbientModeSet() == initialAmbientMode:
            log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Successful, Turning It : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode ^ True])
            return True
        else:
            self.comments += 'Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Unsuccessful for Iteration ' + str(itrCnt)
            log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Unsuccessful for Iteration ' + str(itrCnt))
            return False


    def cleanUp(self):
        if self.setUpSuccessful:
            self.libObj.toggleAmbientMode(True)
        super().cleanUp()
