'''
Created on May 28, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK

log = logging.getLogger(__name__)

class BatteryGauge(LinuxWearablesBaseClass):


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.LWPort.disconnectUsb()
            self.LWPort.connectUsb()
            log.info('Sleeping for 5 seconds')
            time.sleep(SLEEP.SLEEP_5.value)
            options = "-w -r -e debug false -e class " + self.libObj.getInstrumentationCommand(self.testName)
            output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            self.validateResult(output, itrCnt)
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def validateResult(self, result, itrCnt):
        if "Passed 3" in result:
            self.passCtr += 1
            log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
        else:
            log.info(result)
            self.comments += 'Failed for iteration ' + str(itrCnt)
            log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
