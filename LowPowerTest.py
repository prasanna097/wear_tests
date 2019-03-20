'''
Created on Apr 03, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.LPMLibrary import LPMLibrary
from IOTTests.IOTConstants import LOW_POWER_TEST
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import WEARABLE_CONSTANTS, APK

log = logging.getLogger(__name__)

class LowPowerTest(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.testType = self.arguments['--TestType']
        self.testName += '_' + self.testType
        self.suspendTime = int(self.arguments.get('--SuspendTime', 60))
        self.wifi = eval(self.arguments.get('--WiFi',str(False)))
        if self.wifi:
            self.testName = self.testName + 'WifiOn'
        self.wakeLock = eval(self.arguments.get('--WakeLock',str(False)))
        self.checkString = (LOW_POWER_TEST.__dict__['LW'].value)[self.testType][0]
                                                                                


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        log.info('Turning On AirplaneMode')
        self.device.setAirplaneMode(True)
        log.info('Turning off Location, NFC, Bluetooth and Wifi')
        options = "-w -r -e debug false -e WiFi " + str(self.wifi) + " -e class " + self.libObj.getInstrumentationCommand('LowPowerTest')
        output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
        log.info(output)
        if 'Fail' in output:
            log.info(output)
            self.comments += 'Error While Turning Off the Location, NFC, Bluetooth and Wifi'
            raise Exception('Error while turning off')
        log.info('Setting the Brightness to minimum')
        self.device.setBrightness(WEARABLE_CONSTANTS.MIN_BRIGHTNESS.value)
        if self.wakeLock:
            log.ingo('Turning on the WakeLock')
            self.device.toggleDummyWakeLock(True)
        self.LPMLibrary = LPMLibrary(self.device)
        self.checkFile = self.LPMLibrary.getStatsFile((LOW_POWER_TEST.__dict__['LW'].value)[self.testType][1])


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info("Initial Count : ")
            self.previousValue = self.LPMLibrary.getLPMCount(self.checkFile, self.checkString)
            self.LWPort.powerOff()
            log.info('Sleeping ' + str(self.suspendTime) + ' seconds')
            time.sleep(self.suspendTime)
            self.LWPort.powerOn()
            log.info("Current Count : ")
            self.currentValue = self.LPMLibrary.getLPMCount(self.checkFile, self.checkString)
            self.verifyResults(itrCnt)
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def verifyResults(self, itrCnt):
        if self.LPMLibrary.verifyLPMResults(self.previousValue, self.currentValue):
            log.info(self.testName + " passed for Iteration " + str(itrCnt))
            self.passCtr += 1
        else:
            self.comments += " Failed for Iteration " + str(itrCnt)
            log.info(self.testName + " failed for Iteration " + str(itrCnt))


    def cleanUp(self):
        try:
            self.device.setAirplaneMode(False)
            self.libObj.toggleAmbientMode(True)
            if self.wakeLock:
                self.device.toggleDummyWakeLock(False)
        except Exception as e:
            self.comments += "Unexpected error while cleaning up test:" + e.__str__()
            logging.error("Unexpected error while cleaning up test:" + e.__str__())
        finally:
            super().cleanUp()
