'''
Created on May 14, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import IOT_CLIPS_AUDIO, FILE, SLEEP
from IOTTests.IOTLibrary import IOTLibrary
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesLibrary import LinuxWearablesLibrary
from IOTTests.Wearables.LinuxWearablesConstants import APK, PATH, SYSTEM_FILE

log = logging.getLogger(__name__)

class AudioTest(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.codec = self.arguments['--codec']
        self.testName = 'AudioPlayback_' + self.codec
        self.audioFile = 'Test_Audio.' + self.codec


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        log.info(self.audioFile)
        compLibObj = LinuxWearablesLibrary(self.campDevice)
        log.info('Checking/Installing the Automation APK')
        self.libObj.checkAndInstallAPK(APK.AUTOMATION_APK.value)
        compLibObj.checkAndInstallAPK(APK.AUTOMATION_APK.value, 'comp')
        self.installAudioAPK(self.libObj, APK.LW_AUDIO.value, self.device)
        self.installAudioAPK(compLibObj, APK.COMPANION_AUDIO.value, self.campDevice)
        self.compIotLibObj = IOTLibrary(self.campDevice)
        log.info('Creating Screenshot folder in Companion and Wearable To Collect Logs')
        self.campDevice.makeDirectoryOnDevice(FILE.SCREENSHOT.value)
        log.info('Pushing audio Files to companion')
        audioFilePath = self.libObj.buildPath(IOT_CLIPS_AUDIO, self.audioFile)
        self.campDevice.makeDirectoryOnDevice(SYSTEM_FILE.COMP_MUSIC_FOLDER.value)
        self.campDevice.pushResource(audioFilePath, SYSTEM_FILE.COMP_MUSIC_FOLDER.value)
        log.info('Syncying The Audio File from Companion to Wearable Device')
        options = "-w -r -e debug false -e class " + self.libObj.getInstrumentationCommand('AudioCompSync')
        output = self.campDevice.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
        self.libObj.toggleBluetooth(True)
        log.info('Sleeping 10 seconds')
        time.sleep(SLEEP.SLEEP_10.value)
        if 'Fail' in output:
            log.info(output)
            self.comments += 'Sync from companion to wearable did not occur'
            raise Exception('Sync from companion to wearable did not occur')
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            log.info('Now Playing The song ' + self.audioFile)
            options = "-w -r -e debug false -e Filename " + self.audioFile + " -e class " + self.libObj.getInstrumentationCommand('AudioLWPlay')
            output = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(output)
            if 'AudioPlayedSuccessfully' in output:
                self.passCtr += 1
                log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
            else:
                self.comments += 'Failed for iteration ' + str(itrCnt)
                log.info(self.testName + 'Failed for iteration ' + str(itrCnt))
        self.iotLibObj.pullScreenshots(self.logFolder)
        self.compIotLibObj.pullScreenshots(self.logFolder)
        self.checkResult(self.passCtr, self.iteration)


    def installAudioAPK(self, libObj, audioAPK, device):
        log.info('Installing APK on ' + device.getDeviceId())
        installAPK = libObj.buildPath(PATH.WEARABLE_APK_PATH.value, audioAPK)
        device.installApp(installAPK)


    def cleanUp(self):
        if self.setUpSuccessful:
            self.campDevice.unInstallApp(SYSTEM_FILE.PACKAGE.value['MUSIC_PLAYER'])
            self.device.unInstallApp(SYSTEM_FILE.PACKAGE.value['MUSIC_PLAYER'])
            self.campDevice.removeResource(SYSTEM_FILE.COMP_MUSIC_FOLDER.value)
        super().cleanUp()
