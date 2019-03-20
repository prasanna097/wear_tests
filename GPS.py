'''
Created on May 6, 2018

@author: aunnikri
'''
import logging, time, re
from Utilities.Helpers.HostUtilities import LINUX_FILEPATH_DELIMITER
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import SLEEP
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import PATH, SYSTEM_FILE, GPS_FILE, APK, UI_ACTIVITY

log = logging.getLogger(__name__)

class GPS(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.method = (self.arguments.get('--Method', 'apk')).lower()
        self.sleepTime = int(self.arguments.get('--SleepTime', '60'))
        self.testName += '_' + self.method.upper()


    def setup(self):
        super().setup()
        self.setUpSuccessful = False
        getattr(self, self.method + 'Setup')()
        self.setUpSuccessful = True



    def apkSetup(self):
        installAPK = self.libObj.buildPath(PATH.WEARABLE_APK_PATH.value, APK.GPS_APK.value)
        log.info('Installing AndroidGPS Test Apk')
        self.device.installApp(installAPK)


    def uiSetup(self):
        self.valueToGet = [r'Lat', r'Lon', r'Alt']
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        log.info('Disabling verity and rebooting device')
        self.device.disableVerity()
        log.info('Rebooting Device')
        self.device.reboot()
        log.info('Root and remount device after reboot')
        self.device.rootDevice()
        self.device.remountDevice()
        log.info('Checking if Device UI up after reboot')
        self.iotLibObj.verifyDeviceUpOnReboot(UI_ACTIVITY.HOMEACTIVITY.value)
        self.pushGPSFiles()
        log.info('Rebooting Device After Pushing GPS Files')
        self.device.reboot()
        log.info('Remounting the Device')
        self.device.remountDevice()
        log.info('Checking if Device UI up after reboot')
        self.iotLibObj.verifyDeviceUpOnReboot(UI_ACTIVITY.HOMEACTIVITY.value)


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            self.iotLibObj.clearLogcat()
            getattr(self, self.method + 'Execute')(itrCnt)
            getattr(self, self.method + 'VerifyResults')(itrCnt)
        self.checkResult(self.passCtr, self.iteration)


    def apkExecute(self, itrCnt):
        command = '-n com.android.aptgpstest/.GPS'
        log.info('Opening the Android Test GPS App')
        self.device.executeAmCommand(AM_SUB_COMMANDS.START.value,command)
        log.info('Sleeping for ' + str(self.sleepTime) + ' Seconds for iteration : ' + str(itrCnt))
        time.sleep(self.sleepTime)
        log.info('Killing the Android Test App')
        self.device.killProcess(SYSTEM_FILE.PACKAGE.value['GPS_TEST'])


    def uiExecute(self, itrCnt):
        log.info('Sleeping for 10 seconds')
        time.sleep(SLEEP.SLEEP_10.value)
        log.info("Enabling Location")
        self.device.enableLocation()
        log.info('Movig to High GPS Accuracy mode')
        options = "-w -r -e debug false -e class " + self.libObj.getInstrumentationCommand("GPSOn")
        self.output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
        log.info(self.output)
        if 'Pass' not in self.output:
            comments = 'Could not enable Location Fail for Iteration ' + str(itrCnt)
            self.comments += comments
            log.info(comments)
            return
        options = "-w -r -e debug false -e class " + self.libObj.getInstrumentationCommand("GPSCheck")
        log.info('Opening ODLT app and starting Test')
        self.output = (self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)).splitlines()


    def pushGPSFiles(self):
        log.info('Pushing the Required GPS Files')
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.QTI_LOCATION_JAR.value), SYSTEM_FILE.SYSTEM_FRAMEWORK.value)
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.QTI_LOCATION_XML.value), SYSTEM_FILE.ETC_PERMISSION.value)
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.LIB_SO.value), SYSTEM_FILE.SYSTEM_VENDOR_LIB.value)
        self.device.makeDirectoryOnDevice(SYSTEM_FILE.SYSTEM_GPS.value)
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.OLDT_APK.value), SYSTEM_FILE.SYSTEM_GPS.value)
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.QMAP.value), SYSTEM_FILE.SYSTEM_FRAMEWORK.value)
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.QCOM_QMAP.value), SYSTEM_FILE.SYSTEM_ETC_PERMISSION.value)
        self.device.pushResource(self.libObj.buildPath(PATH.GPS_FILES_PATH.value, GPS_FILE.QCOM_LOCAION.value), SYSTEM_FILE.ETC_PERMISSION.value)


    def removeGPSFiles(self):
        log.info('Removing the GPS Files')
        self.device.rootDevice()
        self.device.remountDevice()
        self.device.removeResource(self.iotLibObj.appendLinuxPathDelimiter(SYSTEM_FILE.SYSTEM_FRAMEWORK.value, GPS_FILE.QTI_LOCATION_JAR.value))
        self.device.removeResource(self.iotLibObj.appendLinuxPathDelimiter(SYSTEM_FILE.ETC_PERMISSION.value, GPS_FILE.QTI_LOCATION_XML.value))
        self.device.removeResource(self.iotLibObj.appendLinuxPathDelimiter(SYSTEM_FILE.SYSTEM_VENDOR_LIB.value, GPS_FILE.LIB_SO.value))
        self.device.removeResource(SYSTEM_FILE.SYSTEM_GPS.value)
        self.device.removeResource(self.iotLibObj.appendLinuxPathDelimiter(SYSTEM_FILE.SYSTEM_FRAMEWORK.value, GPS_FILE.QMAP.value))
        self.device.removeResource(self.iotLibObj.appendLinuxPathDelimiter(SYSTEM_FILE.SYSTEM_ETC_PERMISSION.value, GPS_FILE.QCOM_QMAP.value))
        self.device.removeResource(self.iotLibObj.appendLinuxPathDelimiter(SYSTEM_FILE.ETC_PERMISSION.value, GPS_FILE.QCOM_LOCAION.value))
        log.info('Removing Complete')


    def apkVerifyResults(self, itrCnt):
        time.sleep(60)
        fixResults = self.device.checkLogcat('Got fix:')
        if len(fixResults) > 0:
            self.passCtr += 1
            log.info(self.testName + 'Passed for iteration ' + str(itrCnt))
        else:
            comment = self.testName + 'Failed for iteration ' + str(itrCnt)
            self.comments += comment
            log.info(comment)


    def uiVerifyResults(self, itrCnt):
        self.printResults(self.verifyUIResults(self.output),'UI', itrCnt)
        self.printResults(self.verifyLogCatResults(), 'logcat', itrCnt)


    def printResults(self, result, validationmethod, itrCnt):
        if result:
            log.info(self.testName + ' Passed validation through ' + validationmethod + ' for Iteration : ' + str(itrCnt))
            if validationmethod == 'logcat':
                self.passCtr += 1
        else:
            comment = self.testName + ' Failed validation through ' + validationmethod + ' for Iteration : ' + str(itrCnt)
            self.comments += comment
            log.info(comment)


    def verifyLogCatResults(self):
        gpsResults = self.device.checkLogcat('gps')
        getGPSValues = r'gps (\d+.\d+),(\d+.\d+)(.*)alt=(\d+.\d+)(.*)'
        val = re.search(getGPSValues, gpsResults, re.M | re.I)
        if val:
            logCatlat = val.group(1)
            logCatlon = val.group(2)
            logCatalt = val.group(4)
            log.info('Logcat Lattitude : ' + str(logCatlat))
            log.info('Logcat Longitude : ' + str(logCatlon))
            log.info('Logcat Altitude : ' + str(logCatalt))
        fixResults = (self.device.checkLogcat('fix'))
        checkLogCat = ['Waiting for fix = true', 'Passed fix criteria', 'Firing successful fix event', 'Fired successful fix event']
        for line in checkLogCat:
            if line not in fixResults:
                log.info('Did not find ' + line + ' in logcat')
                self.comments += 'Did not find ' + line + ' in logcat'
                return False
        return True


    def verifyUIResults(self, output):
        totalCount = 0
        for line in range(len(output)):
            if not totalCount:
                fixCount = re.search(r'Final Fixes \(Pass/Fail/Tot\):    (\d+) / (\d+) / (\d+)', output[line], re.M | re.I)
                if fixCount:
                    passCount = fixCount.group(1)
                    totalCount = fixCount.group(3)
                    continue
            else:
                val = re.search(self.valueToGet[0] + r':(( )*)(\d+.\d+)(.*)', output[line], re.M | re.I)
                if val:
                    lat = val.group(3)
                    lon = (re.search(self.valueToGet[1] + r':(( )*)(\d+.\d+)(.*)', output[line + 1], re.M | re.I)).group(3)
                    alt = (re.search(self.valueToGet[2] + r':(( )*)(\d+.\d+)(.*)', output[line + 2], re.M | re.I)).group(3)
                    log.info('Lattitude from UI :' + str(lat))
                    log.info('Longitude from UI : ' + str(lon))
                    log.info('Altitude from UI : ' + str(alt))
                    break
        if totalCount != 0 and passCount == totalCount:
            log.info('Total Fixes = ' + str(totalCount) + ' Pass Fixes = ' + str(passCount))
            return True
        else:
            return False


    def apkCleanUp(self):
        log.info('Uninstalling GPS Apk')
        self.device.unInstallApp(SYSTEM_FILE.PACKAGE.value['GPS_TEST'])


    def uiCleanUp(self):
        self.removeGPSFiles()
        log.info('Rebooting the Device')
        self.device.reboot()
        self.device.rootDevice()
        self.device.remountDevice()
        log.info('Checking if UI up after Reboot')
        self.iotLibObj.verifyDeviceUpOnReboot(UI_ACTIVITY.HOMEACTIVITY.value)


    def cleanUp(self):
        if self.setUpSuccessful:
            getattr(self, self.method + 'CleanUp')()
        super().cleanUp()
