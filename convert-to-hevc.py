#!/usr/bin/env python3

import subprocess, os, re, sys, glob
import config

if len(sys.argv) == 1:
    globbed = False
else:
    globbed = True
    config.sourcevideos = glob.glob(sys.argv[1],recursive=True)

sourcefilesize = 0
destfilesize = 0
sourcesize = 0
destsize = 0
processlog = open("processed.log",'a')

for videoarr in config.sourcevideos:
    array = videoarr.split('|')
    video = array[0]

    if globbed == False:
        sourcefilepath = os.path.join(config.sourcebasedir, video)
    else:
        sourcefilepath = video
    if os.path.isdir(sourcefilepath):
        continue
    sourcefilesize = os.path.getsize(sourcefilepath)
    sourcefile = os.path.basename(sourcefilepath)
    sourcefilename, sourcefiletype = os.path.splitext(sourcefile)
    if sourcefiletype in config.skippedfiles:
        continue
    if globbed:
        destfile = os.path.join(os.path.dirname(sourcefilepath),sourcefilename + '.HEVC_CONV.mkv')
    else:
        destfile = os.path.join(config.outputdir, sourcefilename + '.mkv')



    failmarker = os.path.join(os.path.dirname(sourcefilepath),'.' + sourcefile + '.failed-hevc')
    completemarker = os.path.join(os.path.dirname(sourcefilepath),'.' + sourcefile + '.complete-hevc')
    if os.path.isfile(failmarker):
        print('File conversion failed in a previous attempt: %s' % video)
        processlog.write('File already failed conversion: %s\n' % video)
        processlog.flush()
        continue
    if os.path.isfile(completemarker):
        print('File already processed sucessfully: %s' % video)
        processlog.write('File already completed conversion: %s\n' % destfile)
        processlog.flush()
        continue

    print('======Starting file process=====')
    print('Source file path: %s' % sourcefilepath)
    print('Source file: %s' % sourcefile)
    print('Source file name: %s' % sourcefilename)
    print('Source file type: %s' % sourcefiletype)
    print('Source file size: %s' % sourcefilesize)
    print('Destination file: %s' % destfile)
    print('Checking video codec of sourcefile')

    sourcecodec = ''
    try:
        sourcecodec = subprocess.check_output([config.ffprobe, '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', '-hide_banner', '-i', sourcefilepath])
        sourcecodec = sourcecodec.strip().decode()
        print('Source codec: %s' % sourcecodec)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        sourcecodec = 'nonevideo'

    if sourcecodec in config.allowedcodecs:
        print('Allowed codec found! continuing...')
    else:
        print('File already HEVC or invalid\\not allowed format, skipping file')
        continue

    if sourcefilesize < config.minimumvidsize:
        with open(failmarker,'a') as f:
            f.write('File size smaller than configured minimum allowed!')
        print('File size smaller than configured minimum allowed!')
        processlog.write('File size smaller than configured minimum allowed: %s\n' % video)
        continue

    try:
        print('Converting: %s to %s' % (sourcefilepath,destfile))
        if len(array) == 1:
            subprocess.call([config.ffmpeg, '-i', sourcefilepath, '-c:a', 'copy', '-c:v', 'hevc_nvenc', '-preset', 'slow', '-crf', str(config.crf), destfile])
        elif len(array) == 3:
            vidstream = array[1]
            audstream = array[2]
            print('Source video stream: %s' % vidstream)
            print('Source audio stream: %s' % audstream)
            subprocess.call([config.ffmpeg, '-i', sourcefilepath, '-c:a', 'copy', '-c:v', 'hevc_nvenc', '-preset', 'slow', '-map', '0:' + vidstream, '-map','0:' + audstream, '-crf', str(config.crf), destfile])
        elif len(array) == 4:
            vidstream = array[1]
            audstream = array[2]
            substream = array[3]
            print('Source video stream: %s' % vidstream)
            print('Source audio stream: %s' % audstream)
            print('Source subtitle stream: %s' % substream)
            subprocess.call([config.ffmpeg, '-i', sourcefilepath, '-c:a', 'copy', '-c:v', 'hevc_nvenc', '-preset', 'slow', '-map', '0:' + vidstream, '-map', '0:' + audstream, '-map', '0:' + substream, '-crf', str(config.crf), destfile])

        destfilesize = os.path.getsize(destfile)
        destfilesizeMB = str(round((destfilesize/1024)/1024,2)) + 'MB'
        sourcefilesizeMB = str(round((sourcefilesize/1024)/1024,2)) + 'MB'
        print('\nOld file size: %s, New file size: %s\n' % (sourcefilesizeMB,destfilesizeMB))
        if sourcefilesize < destfilesize:
            os.remove(destfile)
            with open(failmarker,'a') as f:
                f.write('New size smaller than original!')
            print('Converted video was larger then source.  Deleted and marking as failed!')
            processlog.write('Processing %s failed!\n' % video)
        else:
            with open(completemarker,'a'):
                os.utime(completemarker)
            sourcesize += sourcefilesize
            destsize += destfilesize
            processlog.write('Processing %s completed!  Old file size: %s, New file size: %s\n' % (destfile,sourcefilesizeMB,destfilesizeMB))
    except KeyboardInterrupt:
        print('Procssing cancelled!')
        if os.path.isfile(destfile):
            os.remove(destfile)
            print('Removed partially processed file')
        break
    processlog.flush()

processlog.write('Conversion complete!\n')
processlog.write('Total source size: %sGB\nTotal destination size: %sGB\n' % (str(((sourcesize/1024)/1024)/1024),str(((destsize/1024)/1024)/1024)))
processlog.close()
print('Conversion complete!')
print('Total source size: %sGB\nTotal destination size: %sGB' % (str(((sourcesize/1024)/1024)/1024),str(((destsize/1024)/1024)/1024)))
