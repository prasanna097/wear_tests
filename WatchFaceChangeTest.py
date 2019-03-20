'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK

log = logging.getLogger(__name__)

class WatchFaceChangeTest(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.switchInterval = int(self.arguments.get('--switch-interval', 60))


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            self.currentWatchFace = self.getWatchFace()
            log.info('Current WatchFace ' + self.currentWatchFace[:-2])
            log.info('Changing the WatchFace')
            options = "-w -r -e debug false -e CurrentWatchFace " + self.currentWatchFace[:-2] + " -e class " + self.libObj.getInstrumentationCommand(self.testName)
            output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(output)
            self.changedWatchFace = self.getWatchFace()
            log.info('New WatchFace ' + self.changedWatchFace[:-2])
            self.verifyResults(itrCnt)
            log.info('Sleeping 5 seconds')
            time.sleep(SLEEP.SLEEP_5.value)
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def getWatchFace(self):
        currentActivity = self.device.getCurrentUIActivities()
        currentActivity = currentActivity.splitlines()
        return (currentActivity[0].split('.'))[-1]


    def verifyResults(self, itrCnt):
        if self.currentWatchFace != self.changedWatchFace:
            self.passCtr += 1
            log.info('WatchFaceChangeTest : Successful for Iteration ' + str(itrCnt))
        else:
            self.comments += 'WatchFace did not change'
            log.info('WatchFaceChangeTest : Unsuccessful for Iteration ' + str(itrCnt))
