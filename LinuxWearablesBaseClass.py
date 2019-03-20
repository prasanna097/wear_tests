'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging, os
from IOTTests.IOTLibrary import IOTLibrary
from IOTTests.IOTConstants import IOTSEGMENTS, FILE
from IOTTests.AssignDeviceObject import AssignDeviceObject
from IOTTests.LETest import LETest
from IOTTests.Wearables.JsonUtility import JsonUtility
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary
from IOTTests.Wearables.LinuxWearablesConstants import PATH, UI_ACTIVITY


log = logging.getLogger(__name__)


class LinuxWearablesBaseClass(LETest):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.testName = self.__class__.__name__
        self.skipBTCheck = False


    def setup(self):
        super().setup()
        if not self.deviceConnectors:
            log.error("Either spiderboard or device not connected at the start of the run. Can't proceed")
            raise Exception('Device Not Connected')
        getDevObj = AssignDeviceObject(self.device)
        self.device, otherDevices = getDevObj.AssignDeviceObject(self.deviceIdDeviceMap, IOTSEGMENTS.LW.value['DevIdPattern'], 2)
        self.iotLibObj = IOTLibrary(self.device)
        if len(otherDevices) == 0:
            raise Exception('Only One Device Present and Companion Missing')
        self.campDevice = otherDevices[0]
        self.LWPort = self.device.deviceConnectorPort
        self.campPort = self.campDevice.deviceConnectorPort
        log.info('Creating Screenshot folder in Wearable To Collect Logs')
        self.device.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        self.libObj = LinuxWearablesLibrary(self.device)
        log.info('Checking If Device is Paired')
        if not self.skipBTCheck and not self.checkBTPaired():
            log.info('Device is Not Paired So Not Executing the Test')
            raise Exception('BT Not Paired')
        else:
            output = 'BTPair not required for this testcase' if self.skipBTCheck else 'Device is Paired Executing the Test'
            log.info(output)


    def checkBTPaired(self):
        '''
        Check if the device is paired
        :return: True : If Paired
                 False : If Not Paired
        '''
        try:
            config = JsonUtility.readJsonFile(PATH.JSON_FILE_PATH.value)
            if not config["BTPaired"]["StatusChecked"]:
                config["BTPaired"]["StatusChecked"] = True
                config["BTPaired"]["Status"] = self.iotLibObj.checkUiUp(UI_ACTIVITY.HOMEACTIVITY.value, 50)
                JsonUtility.writeJsonFile(config, PATH.JSON_FILE_PATH.value)
            return config["BTPaired"]["Status"]
        except FileNotFoundError:
            return self.iotLibObj.checkUiUp(UI_ACTIVITY.HOMEACTIVITY.value, 50)

    def cleanUp(self):
        if self.passCtr != self.iteration:
            log.info("Collecting Bug Reports as test failed")
            self.device.removeResource(FILE.BUG_REPORT.value + '/*')
            self.device.getBugReport()
            self.device.pullResource(FILE.BUG_REPORT.value, os.path.join(self.logFolder, 'BugReport_' + self.device.getDeviceId()))
        super().cleanUp()
