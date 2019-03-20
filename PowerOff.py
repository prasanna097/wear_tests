'''
Created on Apr 24, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import ADB_KEYEVENT_KEYCODES
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK, UI_ACTIVITY, WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class PowerOff(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.scenario = self.arguments.get('--Scenario', WEARABLE_CONSTANTS.HOME_ACTIVITY.value)
        self.testName = self.testName + '_' + self.scenario
        self.activityList = (UI_ACTIVITY.__dict__[self.scenario.upper()].value)


    def setup(self):
        super().setup()
        log.info('Checking/Installing the Automation APK on both LW and Companion')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'LW')


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            if itrCnt != 1:
                self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.HOME.value)
                log.info('Sleeping 20 seconds')
                time.sleep(SLEEP.SLEEP_20.value)
                self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.BACK.value)
            log.info('Doing Device ' + self.scenario)
            mode = " "
            if self.scenario == WEARABLE_CONSTANTS.HOME_ACTIVITY.value:
                mode = " -e Scenario Restart "
            options = "-w -r -e debug false" + mode + " -e class " + self.libObj.getInstrumentationCommand("PowerOff")
            result = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(result)
            self.LWPort.disconnectUsb()
            log.info('sleeping 60 seconds')
            time.sleep(SLEEP.SLEEP_60.value)
            self.LWPort.connectUsb()
            self.verifyResults(itrCnt)
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def verifyResults(self, itrCnt):
        log.info("Waiting for UI")
        result = self.checkHomeActivityUp(itrCnt, self.activityList)
        if self.scenario == WEARABLE_CONSTANTS.BOOT_ACTIVITY.value:
            log.info("Waiting for Device To completely bootup")
            restartActivityList = (UI_ACTIVITY.__dict__[WEARABLE_CONSTANTS.HOME_ACTIVITY.value].value)
            if not self.checkHomeActivityUp(itrCnt, restartActivityList):
                log.info("Home Activity not Up After Shutdown")
                self.comments += "Home Activity not Up After Shutdown"
                result = False
        if result:
            log.info('Successfully Completed device ' + self.scenario + ' for iteration ' + str(itrCnt))
            self.passCtr += 1
        else:
            self.comments += 'Successfully Completed device ' + self.scenario + ' for iteration ' + str(itrCnt)
        self.device.rootDevice()
        self.device.remountDevice()


    def checkHomeActivityUp(self, itrCnt, activityList):
        uiActivity = self.iotLibObj.checkUiUp(activityList, 50)
        if uiActivity:
            log.info(uiActivity + ' is Up for Iteration ' + str(itrCnt))
            return uiActivity
        self.comments += 'UI not Up for Iteration ' + str(itrCnt)
        log.info('UI not Up for Iteration ' + str(itrCnt))
