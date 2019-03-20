'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import WEARABLE_CONSTANTS

log = logging.getLogger(__name__)

class AirplaneTest(LinuxWearablesBaseClass):


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            mode = self.device.isAirplaneModeSet()
            log.info('Airplane Mode : ' + WEARABLE_CONSTANTS.STATUS.value[mode] + ' Turning it : ' + WEARABLE_CONSTANTS.STATUS.value[mode ^ 1])
            mode ^= 1
            if self.toggleAirplaneMode(mode, itrCnt):
                mode ^= 1
                if self.toggleAirplaneMode(mode, itrCnt):
                    self.passCtr += 1
                    log.info('Airplane Mode : ' + WEARABLE_CONSTANTS.STATUS.value[mode ^ 1] + "/" + WEARABLE_CONSTANTS.STATUS.value[mode] + ' Successful for Iteration ' + str(itrCnt))
        self.checkResult(self.passCtr, self.iteration)


    def toggleAirplaneMode(self, mode, itrCnt):
        self.device.setAirplaneMode(bool(mode))
        if self.device.isAirplaneModeSet() == mode:
            log.info('Airplane Mode : ' + WEARABLE_CONSTANTS.STATUS.value[mode] + ' Successful, Turning It : ' + WEARABLE_CONSTANTS.STATUS.value[mode ^ 1])
            return True
        else:
            self.comments += 'Airplane Mode : ' + WEARABLE_CONSTANTS.STATUS.value[mode] + ' Unsuccessful for Iteration ' + str(itrCnt)
            log.info('Airplane Mode : ' + WEARABLE_CONSTANTS.STATUS.value[mode] + ' Unsuccessful for Iteration ' + str(itrCnt))
            return False


    def cleanUp(self):
        self.device.setAirplaneMode(False)
        super().cleanUp()
