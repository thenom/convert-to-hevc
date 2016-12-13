#!/usr/bin/env python3

import subprocess, os, re, sys, glob
import config

if len(sys.argv) < 2:
    print('Please provide a folder to process!')
    print('.e.g  accept-hevc.py "/home/fred/videos"')
    sys.exit(1)

simulate = False
review = False
run = False
runy = False
if len(sys.argv) < 3:
    print('Please supply an action!\n\nsimulate: review all the changes it will attempt\nreview: view all the new found converted videos\nrun: replace all the old videos with confirmation on each\nrun_y: replace all the old videos answering yes to confirmations]')
    sys.exit(1)
else:
    if sys.argv[2] == 'simulate':
        simulate = True
    elif sys.argv[2] == 'review':
        review = True
    elif sys.argv[2] == 'run':
        run = True
    elif sys.argv[2] == 'run_y':
        run = True
        runy = True
    else:
        print('Invalid command!\n')
        print('simulate: review all the changes it will attempt\nreview: view all the new found converted videos\nrun: replace all the old videos with confirmation on each\nrun_y: replace all the old videos answering yes to confirmations]')
        sys.exit(1)

sourcepath = os.path.join(sys.argv[1],'**/*HEVC_CONV.mkv')
sourcelist = glob.glob(sourcepath,recursive=True)

for video in sourcelist:
    oldvid = video.replace('HEVC_CONV.mkv','mkv')
    print('New video: %s' % video)
    print('Old video: %s' % oldvid)
    if review == True:
        print('Playing new...')
        subprocess.call(['vlc',video])
    if runy == False and simulate == False and review == False:
        yn = input('Replace the old with the new converted version? [y/n]')
    else:
        yn = 'y'
    if yn == 'y' and run == True and review == False:
        print('Replacing...')
        if simulate == False:
            if os.path.isfile(oldvid):
                os.remove(oldvid)
            os.rename(video,oldvid)
        print('Complete!')
    print('================================')
