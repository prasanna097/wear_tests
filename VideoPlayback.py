'''
Created on Feb 09, 2018

@author: aunnikri
'''
import logging, time
from Devices.Android.AndroidConstants import AM_SUB_COMMANDS
from IOTTests.IOTConstants import IOT_CLIPS_VIDEO
from IOTTests.Wearables.LinuxWearablesBaseClass import LinuxWearablesBaseClass
from IOTTests.Wearables.LinuxWearablesConstants import APK, SYSTEM_FILE, PATH

log = logging.getLogger(__name__)

class VideoPlayback(LinuxWearablesBaseClass):


    def __init__(self, testId=None, context=None, arguments=None):
        super().__init__(testId, context, arguments)
        self.videoFormat = self.arguments['--videoFormat']
        self.videoFile = self.videoFormat
        if self.videoFormat.lower() == "mp4":
            self.compression = self.arguments['--compression']
            self.videoFile += '_' + self.compression
        self.testName = 'VideoPlayback_' + self.videoFile
        self.videoFile = 'video_' + self.videoFile + '.' + self.videoFormat


    def setup(self):
        self.setUpSuccessful = False
        super().setup()
        videoFilePath = self.libObj.buildPath(IOT_CLIPS_VIDEO, self.videoFile)
        log.info('Pushing video files to LW')
        self.device.pushResource(videoFilePath, "/sdcard/")
        installAPK = self.libObj.buildPath(PATH.WEARABLE_APK_PATH.value, APK.MULTIMEDIA_PLAYER_APK.value)
        log.info('Installing MediaPlayer App')
        self.device.installApp(installAPK)
        self.setUpSuccessful = True


    def execute(self):
        for itrCnt in range(self.iteration):
            itrCnt += 1
            self.dataSource.updateIteration(self.testId, itrCnt)
            self.device.removeResource(SYSTEM_FILE.DEVICE_WEARABLE_FOLDER.value + '/' + SYSTEM_FILE.VIDEO_PLAYBACK_RESULT_FILE.value)
            options = '-e iterations 1 -e file_path /sdcard/' + self.videoFile +  ' -e playback_operation Regular -e class com.android.mediaframeworktest.functional.MediaRecordPlayTest#testVideoPlayback -w com.android.mediaframeworktest/.MultiMediaRecorderStressTestRunner'
            log.info('Playing Video Now for iteration : ' + str(itrCnt))
            result = self.device.executeAmCommand(AM_SUB_COMMANDS.INSTRUMENT.value, options)
            log.info(result)
            content = self.device.readDeviceFileContent(SYSTEM_FILE.VIDEO_PLAYBACK_RESULT_FILE.value)
            self.verifyResults(itrCnt, content)
        self.checkResult(self.passCtr, self.iteration)


    def verifyResults(self, itrCnt, content):
        if 'Test Result = true' in content:
            log.info(self.testName + ' Passed for iteration: ' + str(itrCnt))
            self.passCtr += 1
        else:
            self.comments += self.videoFile + 'Did not play for iteration : ' + str(itrCnt)
            log.info(self.testName + ' Failed for iteration: ' + str(itrCnt))


    def cleanUp(self):
        if self.setUpSuccessful:
            log.info('Uninstalling Media Player App')
            self.device.unInstallApp(SYSTEM_FILE.PACKAGE.value['MULTIMEDIA_FRAMEWORK'])
            log.info('Removing Video File')
            self.device.removeResource(SYSTEM_FILE.SDCARD.value + '/' + self.videoFile)
        super().cleanUp()
