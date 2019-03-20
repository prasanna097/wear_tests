'''
Created on Apr 2, 2018

@author: aunnikri
'''
import logging
import time
from Constants import FrameworkConstants
from Devices.Android.AndroidConstants import ADB_KEYEVENT_KEYCODES
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK, WEARABLE_CONSTANTS, SHELL_SCRIPTS, SYSTEM_FILE, PATH

log = logging.getLogger(__name__)

class AmbientUSB(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.usb = eval(self.arguments.get('--USBMode',str(False)))


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        log.info('Installing Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        if not self.usb:
            log.info('Pushing ambient shell script')
            self.libObj.checkAndPush(PATH.WEARABLE_SHELL_SCRIPTS.value, SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value, SHELL_SCRIPTS.AMBIENT_USB_TEST.value)
        log.info('Turning On ambient mode')
        self.libObj.toggleAmbientMode(True)
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            if self.usb:
                result = self.executeUSB()
            else:
                result = self.executeWithoutUSB()
            self.verifyResults(itrCnt, result)
        self.checkResult(self.passCtr, self.iteration)


    def executeUSB(self):
        self.LWPort.disconnectUsb()
        self.LWPort.connectUsb()
        log.info('Sleeping for 30 seconds')
        time.sleep(SLEEP.SLEEP_30.value)
        if self.libObj.inAmbientMode():
            self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.DEVICE_WAKEUP.value)
            if not self.libObj.inAmbientMode():
                return True
            self.comments += 'Device Still in Ambient Mode'
            return False
        self.comments += 'Device did not go into ambient mode'
        return False


    def executeWithoutUSB(self):
        self.device.executeCommandOnDevice('nohup sh ' + SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SHELL_SCRIPTS.AMBIENT_USB_TEST.value + ' > /data/Wearables/consoleOutput.txt 2>&1 &')
        self.LWPort.disconnectUsb()
        log.info('Sleeping for 20 seconds')
        time.sleep(SLEEP.SLEEP_20.value)
        self.LWPort.connectUsb()
        output = self.device.readDeviceFileContent(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SYSTEM_FILE.BRIGHTNESS.value)
        log.info(output)
        if FrameworkConstants.TEST_RESULT.PASS.value in output:
            return True
        self.comments += 'Ambient to interactive with USB Disconnect Failed '
        return False


    def verifyResults(self, itrCnt, output):
        if output:
            self.passCtr += 1
            log.info(self.testName + ' Passed for iteration: Went to Ambient/Sleep Mode in Under 30 seconds for ' + str(itrCnt))
        else:
            log.info(self.testName + 'Failed for iteration ' + str(itrCnt))


    def cleanUp(self):
        self.device.removeResource(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value)
        if self.setUpSuccessful:
            self.libObj.toggleAmbientMode(True)
        super().cleanUp()
