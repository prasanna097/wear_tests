'''
Created on Feb 14, 2018

@author: aunnikri
'''
import logging
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK, WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class AmbientTest(LinuxWearablesBaseClass):


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        self.setUpSuccessful = True

    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            initialAmbientMode = self.libObj.isAmbientModeSet()
            log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Turning it : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode ^ True])
            initialAmbientMode ^= True
            if self.toggleAmbientMode(initialAmbientMode, itrCnt):
                initialAmbientMode ^= True
                if self.toggleAmbientMode(initialAmbientMode, itrCnt):
                    self.passCtr += 1
                    log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode ^ True] + "/" + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Successful for Iteration ' + str(itrCnt))
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def toggleAmbientMode(self, initialAmbientMode, itrCnt):
        self.libObj.toggleAmbientMode(initialAmbientMode)
        if self.libObj.isAmbientModeSet() == initialAmbientMode:
            log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Successful, Turning It : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode ^ True])
            return True
        else:
            self.comments += 'Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Unsuccessful for Iteration ' + str(itrCnt)
            log.info('Ambient Mode : ' + WEARABLE_CONSTANTS.STATUS.value[initialAmbientMode] + ' Unsuccessful for Iteration ' + str(itrCnt))


    def cleanUp(self):
        if self.setUpSuccessful:
            self.libObj.toggleAmbientMode(True)
        super().cleanUp()
