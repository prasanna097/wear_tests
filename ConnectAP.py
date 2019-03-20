'''
Created on APR 23, 2018

@author: aunnikri
'''
import logging, time
from IOTTests.IOTConstants import SLEEP, FILE
from IOTTests.IOTLibrary import IOTLibrary
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS, ADB_KEYEVENT_KEYCODES
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary
from IOTTests.Wearables.LinuxWearablesConstants import APK

log = logging.getLogger(__name__)

class ConnectAP(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.apId = self.arguments.get('--ApId','APT-Sanity')
        self.password = self.arguments.get('--Password', 'donotask')


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK on both LW and Companion')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'LW')
        compLibObj = LinuxWearablesLibrary(self.campDevice)
        compLibObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'comp')
        self.compIotLibObj = IOTLibrary(self.campDevice)
        log.info('Creating Screenshot folder in Companion and Wearable To Collect Logs')
        self.campDevice.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        log.info('Turning On Bluetooth')
        self.libObj.toggleBluetooth(True)
        log.info('Sleeping 10 seconds')
        time.sleep(SLEEP.SLEEP_10.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info('Selecting the AP on LW')
            options = "-w -r -e debug false -e APID " + self.apId + " -e class " + self.libObj.getInstrumentationCommand('ConnectWifi')
            self.campDevice.inputKeyEvent(ADB_KEYEVENT_KEYCODES.BACK.value)
            output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(output)
            if 'Successful' in output:
                log.info(self.testName + 'APId Does not require password, Passed for iteration: ' + str(itrCnt))
                self.passCtr += 1
                continue
            elif 'Fail' in output:
                self.comments += 'ApId not found for iteration ' + str(itrCnt)
                log.info('ApId not found ' + self.testName + ' Failed for iteration: ' + str(itrCnt))
                continue
            log.info('Waiting for Password to be entered from Companion')
            options = "-w -r -e debug false -e Password " + self.password + " -e class " + self.libObj.getInstrumentationCommand('CompWifi')
            output = self.campDevice.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(output)
            if 'Successful' not in output:
                self.comments += 'Wrong Password, Failed for iteration ' + str(itrCnt)
                log.info(self.testName + 'Wrong Password, Failed for iteration ' + str(itrCnt))
                continue
            log.info('Password Entered Successful, Checking again in LW')
            options = "-w -r -e debug false -e APID " + self.apId + " -e class " + self.libObj.getInstrumentationCommand('CheckWifi')
            output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(output)
            if 'Successful' in output:
                log.info(self.testName + ' and check AP in saved Networks, Passed for iteration: ' + str(itrCnt))
                self.passCtr += 1
            elif 'Connected' in output:
                self.comments += 'Connected to AP but not found in saved networks, Failed for iteration ' + str(itrCnt)
                log.info(self.testName + 'Connected to AP but not found in saved networks, Failed for iteration ' + str(itrCnt))
            else:
                self.comments += 'Failed both Connect and Remember AP'
                log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
        self.compIotLibObj.pullScreenshots(self.logFolder)
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)
