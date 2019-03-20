'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging
from Utilities.Helpers.HostUtilities import LINUX_FILEPATH_DELIMITER
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import SHELL_SCRIPTS, PATH, SYSTEM_FILE, WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class OpenKill(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.activityList = (self.arguments.get('--activityList', "STOPWATCH,ALARM,SETTINGS")).split(',')


    def setup(self):
        super().setup()
        log.info("Pushing ActivityLaunch File")
        self.libObj.checkAndPush(PATH.WEARABLE_SHELL_SCRIPTS.value, SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value, SHELL_SCRIPTS.ACTIVITY_LAUNCH_TEST.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info('Clearing logcat')
            self.iotLibObj.clearLogcat()
            activityStarted = True
            log.info('Opening and Killing activities now')
            comment = ''
            self.device.executeCommandOnDevice('sh ' + SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + LINUX_FILEPATH_DELIMITER + SHELL_SCRIPTS.ACTIVITY_LAUNCH_TEST.value)
            for activity in self.activityList:
                if not self.checkLogs(activity):
                    activityStarted = False
                    comment += activity + ' Open And Kill Unsuccessful\n'
                    log.info(activity + ' Open And Kill Unsuccessful')
                else:
                    log.info(activity + ' Open And Kill Successful')
            if activityStarted:
                log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
                self.passCtr += 1
            else :
                self.comments += comment + ' Failed for iteration ' + str(itrCnt)
        self.checkResult(self.passCtr, self.iteration)


    def checkLogs(self, activity):
        logCat = self.device.checkLogcat(SYSTEM_FILE.ACTIVITY.value[activity])
        for activity in WEARABLE_CONSTANTS.OPEN_ACTIVITY.value:
            if activity in logCat and WEARABLE_CONSTANTS.CLOSE_ACTIVITY.value in logCat:
                return True
        return False


    def cleanUp(self):
        self.device.removeResource(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value)
        super().cleanUp()
