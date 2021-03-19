import os
from psychopy import core, visual, gui, event
from datetime import datetime

datadir = os.getcwd()

print("The current working directory is %s" % datadir)

myDlg = gui.Dlg(title="Post scanning questionnaire")
myDlg.addText('Subject info')
myDlg.addField('Subject ID:')
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    print(ok_data)
else:
    print('user cancelled')

subid = ok_data[0]
subdata = datadir + '/data/' + subid

if not os.path.isdir(subdata):
    os.mkdir(subdata)

questions = ['How pleasant was the partner touch?',
             'How relaxing was the partner touch?',
             'How pleasant was the stranger touch?',
             'How relaxing was the stranger touch?',
             'How trustworthy did you find the stranger?',
             'How attractive did you find the stranger?',
             'How was the interaction with the nurse?']

left_labels = ['very unpleasant', 'not at all relaxing', 'very unpleasant',
               'not at all relaxing', 'very untrustworthy', 'very unattractive', 'very stressful']
right_labels = ['very pleasant', 'very relaxing', 'very pleasant',
                'very relaxing', 'very trustworthy', 'very attractive', 'very calming']

win = visual.Window(
    #size=[1920, 1080],
    size=[900, 600],
    units='norm',
    fullscr=True,# True if you want whole screen and False if not (False is just for debugging really)
    color='black')

vas = visual.Slider(win,
                    ticks=(-10, 10),
                    labels=('', ''),
                    granularity=0,
                    color='white')

anchor_left = visual.TextStim(win, text='foo',
                              pos=[0.2, -0.2],
                              alignHoriz='center')


anchor_right = visual.TextStim(win, text='bar',
                              pos=[1.3, -0.2],
                              alignHoriz='center')

message = visual.TextStim(win, text='press any key to start',
                          pos=[0.7, 0.5],
                          alignHoriz='center',
                          wrapWidth=1.5)

message.autoDraw = True  # Automatically draw every frame
win.flip()
event.waitKeys()
print(message.height)

message.text = 'You will rate your perception of the experiment. You will see a line where the ends represent two extremes. Please click on the line where your experience was. Once you click, you cannot change your response. If you feel like you accidentally clicked wrong, please tell the experimenter and you can re-do the rating. \n \n click any key to start'
message.height = 0.08
message.pos = [0.7, 0]
win.flip()
event.waitKeys()

message.height = 0.1
message.pos = [0.8, 0.5]
subdatafile = subdata + '/ratings.txt'
with open(subdatafile, 'a+') as ratingFile:
    ratingFile.write('time: ' +datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '\n')

for i, question in enumerate(questions):
    message.text = question
    win.flip()
    core.wait(1.0)
    anchor_left.text = left_labels[i]
    anchor_right.text = right_labels[i]
    while not vas.rating:
        vas.draw()
        anchor_left.draw()
        anchor_right.draw()
        win.flip()
    with open(subdatafile, 'a+') as ratingFile:
        ratingFile.write('Q' + str(i) + ' VAS: ' + str(vas.rating) + ' RT: ' + str(vas.rt) + '\n')
    print(f'Rating: {vas.rating}, RT: {vas.rt}')
    vas.reset()


message.text = 'That\'s it! Thank you!'
win.flip()
event.waitKeys()

win.close()
core.quit()
