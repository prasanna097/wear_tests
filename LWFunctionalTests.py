'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from Constants import FrameworkConstants
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK

log = logging.getLogger(__name__)

class LWFunctionalTests(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.testName = self.arguments['--testname']


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info("Executing the Test")
            devId = ""
            if self.testName == "DeviceInfo":
                devId = "-e DeviceId " + str(self.device.getDeviceId())
            options = "-w -r -e debug false " + devId + " -e class " + self.libObj.getInstrumentationCommand(self.testName)
            output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(output)
            self.verifyResults(itrCnt, output)
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def verifyResults(self, itrCnt, output):
        if FrameworkConstants.TEST_RESULT.PASS.value in output:
            log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
            self.passCtr += 1
        else:
            self.comments += self.testName + 'Failed for iteration ' + str(itrCnt)
            log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
