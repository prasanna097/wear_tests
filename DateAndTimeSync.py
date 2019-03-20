'''
Created on Feb 14, 2018

@author: aunnikri
'''
import logging, datetime, time
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import WEARABLE_CONSTANTS
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary

log = logging.getLogger(__name__)

class DateAndTimeSync(LinuxWearablesBaseClass):


    def setup(self):
        super().setup()
        log.info('Turning On Bluetooth')
        self.libObj.toggleBluetooth(True)
        log.info('Sleeping 10 seconds')
        time.sleep(SLEEP.SLEEP_10.value)
        self.compLibObj = LinuxWearablesLibrary(self.campDevice)



    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            self.compLibObj.setTime(datetime.datetime.now().strftime(WEARABLE_CONSTANTS.DATE_TIME_FORMAT.value))
            log.info("Time Before Resetting")
            self.compLibObj.getDateAndTime()
            self.libObj.getDateAndTime()
            log.info('Resetting the Date And Time of Companion Device to Sun Jan  1 00:00:00 IST 2017')
            self.compLibObj.setTime(WEARABLE_CONSTANTS.RESET_DATETIME.value)
            log.info("Time After Resetting")
            self.verifyResults(itrCnt)
        self.checkResult(self.passCtr, self.iteration)


    def verifyResults(self, itrCnt):
        lwTime = self.libObj.getDateAndTime()
        compTime = self.compLibObj.getDateAndTime()
        if lwTime == compTime:
            log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
            self.passCtr += 1
        else:
            self.comments += 'Failed for iteration ' + str(itrCnt)
            log.info(self.testName + 'Failed for iteration ' + str(itrCnt))


    def cleanUp(self):
        try:
            log.info('Resetting the time to Current time')
            self.compLibObj.setTime(datetime.datetime.now().strftime(WEARABLE_CONSTANTS.DATE_TIME_FORMAT.value))
            self.compLibObj.getDateAndTime()
            self.libObj.getDateAndTime()
        except Exception as e:
            logging.error("Unexpected error while cleaning up test:" + e.__str__())
        finally:
            super().cleanUp()

