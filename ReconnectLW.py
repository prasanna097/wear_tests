'''
Created on Apr 24, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import SLEEP, FILE
from IOTTests.IOTLibrary import IOTLibrary
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary
from IOTTests.Wearables.LinuxWearablesConstants import APK, UI_ACTIVITY, SYSTEM_FILE

log = logging.getLogger(__name__)

class ReconnectLW(LinuxWearablesBaseClass):


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK on both LW and Companion')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'LW')
        compLibObj = LinuxWearablesLibrary(self.campDevice)
        compLibObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'comp')
        log.info('Turning on Bluetooth')
        self.libObj.toggleBluetooth(True)
        self.compIotLibObj = IOTLibrary(self.campDevice)
        log.info('Creating Screenshot folder in Companion and Wearable To Collect Logs')
        self.campDevice.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        self.device.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        log.info('Sleeping 10 seconds')
        time.sleep(SLEEP.SLEEP_10.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info('Checking If Connected Before Reboot')
            if not self.checkComp('Connected'):
                self.comments += "Not Connected before Reboot"
                log.info(self.testName + ' Failed for iteration ' + str(itrCnt))
                continue
            log.info('Connected Before reboot')
            self.device.reboot()
            if not self.iotLibObj.checkUiUp(UI_ACTIVITY.HOMEACTIVITY.value, 50):
                self.comments += 'UI not up after reboot ' + self.testName + ' Failed for iteration ' + str(itrCnt)
                log.info('UI not up after reboot ' + self.testName + ' Failed for iteration ' + str(itrCnt))
                continue
            log.info('Checking If Disconnected After Reboot')
            if self.checkComp(''):
                log.info('Disconnected after Reboot for Iteration ' + str(itrCnt))
            log.info('Device Up, Waiting for Auto Reconnect')
            log.info('Sleeping 40 seconds')
            time.sleep(SLEEP.SLEEP_60.value)
            if self.checkComp('Connected'):
                log.info('Device Connected After Reboot ' + self.testName + ' Passed for iteration ' + str(itrCnt))
                self.passCtr += 1
            else:
                self.comments += 'Device not Connected After Reboot ' + self.testName + 'Failed for iteration ' + str(itrCnt)
                log.info('Device not Connected After Reboot ' + self.testName + 'Failed for iteration ' + str(itrCnt))
        self.campDevice.executeAmCommand(AM_SUB_COMMANDS.FORCE_STOP.value, ' ' + SYSTEM_FILE.PACKAGE.value['WEAR_OS'])
        self.compIotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def checkComp(self, checkString=""):
        if checkString == "Connected":
                checkString = "-e Check " + checkString
        options = "-w -r -e debug false " + checkString + " -e class " + self.libObj.getInstrumentationCommand('CompReconnect')
        output = self.campDevice.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
        log.info(output)
        if 'Successful' in output:
            return True
        return False
