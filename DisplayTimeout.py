'''
Created on Feb 14, 2018

@author: aunnikri
'''
import logging, time
from Constants import FrameworkConstants
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import SHELL_SCRIPTS, PATH, SYSTEM_FILE, WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class DisplayTimeout(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.usbMode = eval(self.arguments.get('--USBMode',str(False)))


    def setup(self):
        super().setup()
        log.info("Pushing DisplayTimeout File")
        self.libObj.checkAndPush(PATH.WEARABLE_SHELL_SCRIPTS.value, SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value, SHELL_SCRIPTS.DISPLAY_TIMEOUT_TEST.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            if self.usbMode:
                self.executeWithUSB()
            else:
                self.executeWithoutUSB()
            result = self.device.readDeviceFileContent(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SYSTEM_FILE.DEVICE_TIMEOUT.value)
            self.device.removeResource(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SYSTEM_FILE.DEVICE_TIMEOUT.value)
            log.info(result)
            self.verifyResults(itrCnt, result)
        self.checkResult(self.passCtr, self.iteration)


    def executeWithUSB(self):
        self.LWPort.disconnectUsb()
        self.LWPort.connectUsb()
        self.device.executeCommandOnDevice('sh ' + SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SHELL_SCRIPTS.DISPLAY_TIMEOUT_TEST.value)
        log.info('Sleeping 30 seconds')
        time.sleep(SLEEP.SLEEP_30.value)


    def executeWithoutUSB(self):
        self.device.executeCommandOnDevice('nohup sh ' + SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SHELL_SCRIPTS.DISPLAY_TIMEOUT_TEST.value + ' > /data/Wearables/consoleOutput.txt 2>&1 &')
        self.LWPort.disconnectUsb()
        log.info('Sleeping 20 seconds')
        time.sleep(SLEEP.SLEEP_20.value)
        self.LWPort.connectUsb()


    def verifyResults(self, itrCnt, output):
        if FrameworkConstants.TEST_RESULT.PASS.value in output:
            log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
            self.passCtr += 1
        else:
            self.comments += 'Failed for iteration ' + str(itrCnt)
            log.info(self.testName + 'Failed for iteration ' + str(itrCnt))


    def cleanUp(self):
        self.device.removeResource(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value)
        super().cleanUp()
