# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:44:03 2018

First version of experimental design related to Pathfinder project 2

@author: jsuvilehto
"""

# Change this to True when you want to run video recording, e.g. when really collecting subjects
# Keeping it at false helps when you work on the code with computers with no webcam or cv2 package
record = True
byFrames = True  # True = Video file and False = by frame at moment

# change this to point to the folder where you keep the code
scriptloc = r'C:\Users\niall\Documents\Faces Study\faces-master'  # os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import sys

sys.path.append(scriptloc)
import time
import pyaudio
import wave
# import os
# import inspect
from psychopy import visual, core, iohub
import numpy as np
from trialFunctions import runFaceTrialPosNeg, runTextTrial, initSub

if record:
    from videoFunctions import stoprecording, startRecordingProc
    from Video_Audio_Merge import AudioRecorder, start_audio_recording, stop_AudioRecording, start_AVrecording, \
        stop_AVrecording

mainDir = scriptloc
subid, textTrials, faceTrials = initSub(mainDir)

video_loc = mainDir + '\\subjects\\' + str(subid) + '\\video\\'
audio_loc = mainDir + '\\subjects\\' + str(subid) + '\\audio\\'
beh_loc = mainDir + '\\subjects\\' + str(subid) + '\\behavioural\\'

# instructions are set here - you can find from the code where each gets called.
instrTexts = {
    'expstart': "Thank you for participating in this study. \n\nThe video recording will start as soon as the experiment starts. Please press any key to start the experiment and the video recording.",
    'panasstart': 'The following task consists of a number of words that describe diferent feelings and emotions. Read each item and then indicate in the scale below to what extent you feel this way right now. \n\nPlease press any key to start',
    'facestart': 'You will soon start a new task where you are asked to evaluate facial expressions from photographs. \n\nThe faces will be presented in the centre of the screen and they will appear for about half a second only. For each face decide whether the expression on the face is a negative or a positive one. You may feel like you are guessing, and there are no right or wrong answers. Just answer as quickly as you can according to your gut reaction. \n\nThe next face will be presented after you have responded to the previous one or at the latest after 10 seconds since you saw the previous face. There will be a short practice first where your responses will not be scored and I will tell you when the real task starts. \n\nPlease press any key to continue.',
    'faceinstr': 'Please place your hands on the keyboard so that your right index finger is on the \'j\' key and your left index finger is on the \'f\' key. \n\nPlease press  \'j\' or \'f\' to continue.',
    'posneginstr': 'If you think the mood of the person you see is negative, press \'f\' on your keyboard. If you think the mood of the person you see is positive, press \'j\' on your keyboard.',
    'posneginstrreverse': 'If you think the mood of the person you see is negative, press \'j\' on your keyboard. If you think the mood of the person you see is positive, press \'f\' on your keyboard.',
    'posnegarrows': '<--- negative \t\t\t positive --->',
    'posnegarrowsreverse': '<--- positive \t\t\t negative --->',
    'blockbegin': 'Next, you will start the actual experiment. Some of the facial expressions might be very subtle. \n\nRemember, you may feel like you are guessing, and there are no right or wrong answers. Just answer as quickly as you can according to your gut reaction. \n\nPlease press  \'j\' or \'f\' to start the actual task.',
    'blockbreak': 'Please press  \'j\' or \'f\' to continue the task.',
    'thankyou': 'Thank you subject ' + str(
        subid) + ',\nyou have now completed the whole experiment. \n\nPress any key to close this window.'}

exampleImages = [scriptloc + '\\example_images\\sad_example.jpg',
                 scriptloc + '\\example_images\\happy_example.jpg',
                 scriptloc + '\\example_images\\fear_example.jpg',
                 scriptloc + '\\example_images\\surprise_example.jpg']

# use iohub and keyboard to capture key press events
io = iohub.launchHubServer()
keyboard = io.devices.keyboard
mouse = io.devices.mouse

# randomise direction of pos/neg in faces
posNegDir = np.random.random()
if (posNegDir < 0.5):
    thisSubPosNegText = instrTexts['posneginstr']
    thisSubPosNegArrows = instrTexts['posnegarrows']
else:
    thisSubPosNegText = instrTexts['posneginstrreverse']
    thisSubPosNegArrows = instrTexts['posnegarrowsreverse']
##
# Create the visual elements used in the experiment
# these are later modified to show different texts, instructions anli
#
# Karen! Change these when playing with fonts etc
##

generalTextSize = 30
generalWrapWidth = 850

win = visual.Window(
    size=[1920, 1080],
    units="pix",
    fullscr=True,
    # color = [0.079,0.079,0.079]
    color=[0.4, 0.4, 0.4])

img = visual.ImageStim(win=win, mask=None,
                       interpolate=True, pos=(0, 50))

fixation = visual.TextStim(win=win, pos=[0, 50], text='+', height=150,
                           color='black')

instructions = visual.TextStim(
    win=win,
    height=generalTextSize,
    wrapWidth=generalWrapWidth,
    pos=(0, 300),
    color='black')

answerGuide = visual.TextStim(
    win=win,
    height=generalTextSize,
    wrapWidth=generalWrapWidth,
    pos=(0, -200),
    text=thisSubPosNegArrows,
    color='black')

stimText = visual.TextStim(
    win=win,
    wrapWidth=generalWrapWidth,
    pos=(0, 180),
    height=5,
    color='black')

newTaskText = visual.TextStim(
    height=generalTextSize,
    win=win,
    wrapWidth=generalWrapWidth,
    pos=(0, 200),
    color='black')

##
# Run the actual experiment
##
# Display welcome and warning about recording
newTaskText.setText(instrTexts['expstart'])
newTaskText.draw()
win.flip()
keyboard.waitForKeys(clear=True, etype=keyboard.KEY_RELEASE)
keyboard.clearEvents()

# if running video, start recording after keyboard input (above)
if record:
    videoOutfile = video_loc + 'sub_' + str(subid)
    audiofilename = audio_loc + 'sub_' + str(subid)

    # audio_path=audioOutfile
    startRecordingProc(videoOutfile, byFrames)
    start_audio_recording()
# startAudio...(audioOutfile)

# give the subject instructions for PANAS
newTaskText.setText(instrTexts['panasstart'])
newTaskText.draw()
win.flip()
keyboard.waitForKeys(clear=True, etype=keyboard.KEY_RELEASE)

## make a text file to save data from text trials
timestr_text = time.strftime("%Y%m%d-%H_%M_%S")
textFileName = 'textResponses'

# make text files for outputting responses, name the columns
textDataFile = open(beh_loc + 'sub_' + str(subid) + '_' + textFileName + '_' + timestr_text + '.csv', 'w')
textDataFile.write('stimulusWord,showOrder,response,stimulusTimeStamp,timeToResponse\n')
mousePosFile = open(beh_loc + 'sub_' + str(subid) + '_mouseTracking_' + timestr_text + '.csv', 'w')
mousePosFile.write('timeStamp,XPos,YPos,deltaX,deltaY,buttonLeft,buttonMiddle,buttonRight\n')
##run text trials
for currTrial in textTrials:
    mouseRecord = []
    res = runTextTrial(currTrial, win, instructions, stimText, mouse, mouseRecord)
    rating = (res['rating'] or -1)  # returns -1 in case rating wasn't done within the specified time frame
    textDataFile.write(
        '%s,%i,%i,%.5f,%.5f\n' % (res['stimText'], res['showOrder'], rating, res['startTime'], res['timeStamp']))
    mousePosFile.writelines('%.5f,%i,%i,%i,%i,%s,%s,%s\n' % (
    mousePos[0], mousePos[1], mousePos[2], mousePos[3], mousePos[4], mousePos[5], mousePos[6], mousePos[7]) for mousePos
                            in mouseRecord)
textDataFile.close()
mousePosFile.close()

## give the subject instructions for face rating task
## the instructions for faces are so long we need to shift the position of the text
keyboard.clearEvents()
newTaskText.setPos((0, 50))
newTaskText.setText(instrTexts['facestart'])
newTaskText.draw()
win.flip()
keyboard.waitForKeys(clear=True, etype=keyboard.KEY_RELEASE)
print
keyboard.state
win.flip()
keyboard.clearEvents()
# moving text back after the long instructions
newTaskText.setPos((0, 200))
img.setPos((0, 30))
# show instructions for faces-task plus example images to practice
faceTestDataFile = open(beh_loc + 'sub_' + str(subid) + '_timestamps_for_face_tests.csv',
                        'w')  # a simple text file with 'comma-separated-values'
faceTestDataFile.write('stimFile,imageShowTime,imageShowTimeInKeyTimeType,keyDown, keyUp\n')
for i in range(len(exampleImages) + 1):
    if i == 0:
        newTaskText.setText(instrTexts['faceinstr'])
    else:
        newTaskText.setText(thisSubPosNegText)
    newTaskText.draw()
    if i is not 0:
        answerGuide.draw()
        testImageTime = time.time()
        testImageKeyTypeTime = core.getTime()
        img.setImage(exampleImages[i - 1])
        img.draw()
        # faceTestDataFile.write('%s,%.5f\n' %(exampleImages[i-1], testImageTime))
    win.flip()
    key = keyboard.waitForKeys(keys=['f', 'j'], clear=True, etype=keyboard.KEY_RELEASE)
    if i is not 0:
        faceTestDataFile.write('%s,%.5f,%.5f,%.5f,%.5f\n' % (
        exampleImages[i - 1], testImageTime, testImageKeyTypeTime, key[-1].time - key[-1].duration, key[-1].time))
    # print('got key press at ' + str(key[0].time))
    # print keyboard.state
    win.flip()
faceTestDataFile.close()

# revert back to regular positioning of stimulus image
img.setPos((0, 50))
# make a text file to save data from face trials
timestr_face = time.strftime("%Y%m%d-%H_%M_%S")
faceFileName = 'faceResponses'
faceDataFile = open(beh_loc + 'sub_' + str(subid) + '_' + faceFileName + '_' + timestr_face + '.csv',
                    'w')  # a simple text file with 'comma-separated-values'
faceDataFile.write('stimFile,TrialType,block,showOrder,response,startTime,startTimeKeyStyle,keydownTime,keyupTime\n')
# run face trials
for n, trialBlock in enumerate(faceTrials):
    keyboard.clearEvents()
    if n == 0:
        newTaskText.setText(instrTexts['blockbegin'])
    else:
        newTaskText.setText(instrTexts['blockbreak'])
    newTaskText.draw()
    win.flip()
    keyboard.waitForKeys(keys=['f', 'j'], clear=True, etype=keyboard.KEY_RELEASE)
    win.flip()
    for currTrial in trialBlock:
        startTime = time.time()
        res = runFaceTrialPosNeg(currTrial, win, img, instructions, answerGuide, fixation, keyboard, posNegDir)
        imagetype = []
        if "Sad" in res['stimFile']:

            imagetype = 1
        elif "Happy" in res['stimFile']:

            imagetype = 2
        elif "Fear" in res['stimFile']:
            imagetype = 3
        else:
            imagetype = 4
        rating = (res['rating'] or 0)  # returns 0 in case rating wasn't done within the specified time frame
        faceDataFile.write('%s,%i,%i,%i,%i,%.5f,%.5f,%.5f,%.5f\n' % (
        res['stimFile'], imagetype, n, res['showOrder'], rating, res['startTime'], res['startTime2'], res['keydown'],
        res['keyup']))
faceDataFile.close()

newTaskText.setText(instrTexts['thankyou'])
newTaskText.draw()
win.flip()
keyboard.waitForKeys(clear=True, etype=keyboard.KEY_RELEASE)

if record:
    stoprecording()
    stop_AudioRecording()

io.quit()
win.close()
core.quit()

print('Done')