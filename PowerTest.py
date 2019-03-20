'''
Created on Apr 03, 2018

@author: aunnikri
'''
import logging
import time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS, ADB_KEYEVENT_KEYCODES
from Utilities.Commands.ExecutionProperties import ExecutionProperties
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import SYSTEM_FILE, APK, POWER_TEST, PATH

log = logging.getLogger(__name__)

class PowerTest(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        type = self.arguments['--TestType']
        self.testName = self.testName + '_' + type
        self.displayType = POWER_TEST.__dict__[type].value[0]
        self.uiActivity = POWER_TEST.__dict__[type].value[1]
        self.suspendTime = int(self.arguments.get('--SuspendTime', 60))


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        installAPK = self.libObj.buildPath(PATH.WEARABLE_APK_PATH.value, APK.POWER_TEST.value)
        self.device.installApp(installAPK)
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        self.libObj.toggleAmbientMode(True)
        self.device.setAirplaneMode(True)
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            options = '-e class com.google.android.powertests.' + self.displayType + ' -w com.google.android.powertests/android.test.InstrumentationTestRunner'
            self.device.inputKeyEvent(ADB_KEYEVENT_KEYCODES.DEVICE_WAKEUP.value)
            log.info('Changing Timeout and Running in Background')
            changeExecutionProperties = ExecutionProperties()
            changeExecutionProperties.setBackgroundExecution(True)
            self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options, changeExecutionProperties)
            log.info('Starting the ' + self.displayType)
            log.info('Sleeping 20 seconds')
            time.sleep(SLEEP.SLEEP_20.value)
            if self.device.isUIUp(self.uiActivity):
                self.passCtr += 1
                log.info(self.uiActivity + ' is up. ' + self.testName + " passed for Iteration " + str(itrCnt))
            else:
                self.comments += self.testName + " failed for Iteration " + str(itrCnt)
                log.info(self.testName + " failed for Iteration " + str(itrCnt))
            self.device.killProcess('com.google.android.powertests')
        self.checkResult(self.passCtr, self.iteration)


    def cleanUp(self):
        self.device.setAirplaneMode(False)
        if self.setUpSuccessful:
            self.device.unInstallApp(SYSTEM_FILE.PACKAGE.PACKAGE.value['POWERTEST'])
        super().cleanUp()
