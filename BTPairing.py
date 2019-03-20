'''
Created on Apr 09, 2018

@author: aunnikri
'''
import logging, time, re
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from Utilities.Commands.ExecutionProperties import ExecutionProperties
from IOTTests.IOTConstants import FILE, SLEEP
from IOTTests.IOTLibrary import IOTLibrary
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary
from IOTTests.Wearables.LinuxWearablesConstants import APK, UI_ACTIVITY, SYSTEM_FILE

log = logging.getLogger(__name__)

class BTPairing(LinuxWearablesBaseClass):


    def setup(self):
        self.skipBTCheck = True
        super().setup()
        log.info('Checking/Installing the Automation APK on both LW and Companion')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'LW', True)
        compLibObj = LinuxWearablesLibrary(self.campDevice)
        compLibObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'comp')
        self.compIotLibObj = IOTLibrary(self.campDevice)
        log.info('Creating Screenshot folder in Companion and Wearable To Collect Logs')
        self.campDevice.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        self.device.makeDirectoryOnDevice(FILE.SCREENSHOT.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            if self.iotLibObj.checkUiUp(UI_ACTIVITY.HOMEACTIVITY.value, 2):
                self.passCtr += 1
                log.info("Already BT Paired")
                continue
            self.campDevice.executeAmCommand(AM_SUB_COMMANDS.FORCE_STOP.value, ' ' + SYSTEM_FILE.PACKAGE.value['WEAR_OS'])
            output = self.pairScreenLW()
            if 'FactoryDataReset' in output:
                log.info('LW Pairing after FDR')
                if self.libObj.doFDR(self.iotLibObj):
                    log.info('FDR Successful')
                    log.info('Installing the Automation APK  both LW after FDR')
                    self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'LW', True)
                    output = self.pairScreenLW()
            if "Successfully" not in output:
                log.info("LW did not go to Pairing Screen : Test Failed")
                break
            match = re.search("BTID = (.*)",output)
            btID = ((match.group(1))[:-1]).replace(" ","_")
            log.info("LW in pairing screen with BTID : " + btID)
            self.iotLibObj.pullScreenshots(self.logFolder)
            self.startTime = 0
            output = self.pairCompanion(btID)
            if "BTID Found" not in output:
                self.campDevice.reboot()
                output = self.pairCompanion(btID)
            if self.iotLibObj.checkUiUp(UI_ACTIVITY.HOMEACTIVITY.value, 50):
                pairTime = (time.time() - self.startTime)/60
                if pairTime <= 10:
                    self.passCtr += 1
                    log.info(self.testName + ' Passed for iteration: ' + str(itrCnt) + 'in ' + str(pairTime) + ' minutes')
                    if 'Without Account Sync' in output:
                        self.comments += 'BT Pairing done without account sync'
                else:
                    self.comments += "Pairing Done in " + str(pairTime) + " minutes"
                    self.comments += 'Failed for Iteration ' + str(itrCnt)
                    log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
            else:
                self.comments += 'Failed for Iteration ' + str(itrCnt)
                log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
        self.campDevice.executeAmCommand(AM_SUB_COMMANDS.FORCE_STOP.value, ' ' + SYSTEM_FILE.PACKAGE.value['WEAR_OS'])
        self.compIotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def pairScreenLW(self):
        options = "-w -r -e debug false -e class " + self.libObj.getInstrumentationCommand('BTPairingLW')
        log.info('Doing SetUp on LW for Pairing')
        output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
        log.info(output)
        return output


    def pairCompanion(self, btid):
        changeTimeout = ExecutionProperties()
        log.info('Changing timeout of command to 15 minutes')
        changeTimeout.setTimeout(900)
        options = "-w -r -e debug false -e BTID " + btid + " -e class " + self.libObj.getInstrumentationCommand(self.testName)
        log.info('Now starting pairing in Companion')
        self.startTime = time.time()
        output = self.campDevice.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options, changeTimeout)
        log.info(output)
        return output
