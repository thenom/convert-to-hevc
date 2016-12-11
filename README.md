# convert-to-hevc

Script to convert multiple video files into HEVC\x265 using the nvenc hardware codec and copy the audio.  The resulting video file will have 1 video\audio\subtitle stream from the source video (if they exist.  i.e. if the source has no subtitles then there will be none in the destination).

Videos that have attempted processing will be logged out to ./processed.log.

This is setup to use the hevc_nvenc video codec that uses Nvidia GFX hardware to re-encode the video.  You need to make sure that your version of ffmpeg has this compiled into the binary:

```
$ ffmpeg -encoders | grep -i hevc_nvenc
 V..... hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
```
---
### config.py example

```
ffmpeg = '/usr/bin/ffmpeg'     # source of the ffmpeg binary
ffprobe = '/usr/bin/ffprobe'   # source of the ffprobe binary

# sourcevideos either has to be a string representing the suffix path after the sourcebasedir.
# or
# csv of the path,videostream,audiostream  (PIPE delimited! (|))
# or
# csv of the path,videostream,audiostream,subtitlestream  (PIPE delimited! (|))
sourcebasedir = '/home/fred/Videos/myvideos'   # the prefix for the video path were all are the same
sourcevideos = [      # source videos will be (sourcebasedir + sourcevideos)
    '/holiday 2016/video1.avi',
    '/party 10-12/party.mkv',
    '/my film/film 2014.mkv|0|2',               # use stream 0 as the video and stream 2 as the audio
    '/my other subtitled file/film.mkv|0|2|5'   # use stream 0 as the video, 2 as the audio and 5 for the subtitles
]

outputdir = '/home/fred/Videos/converted/'    # output folder for converted videos for you to check
crf = 28    # the output quality (0-51).  28 is supposed to be visually the same as source.

allowedcodecs = ['x264','h264']    # allowed cource codecs to convert
skippedfiles = ['.jpg','.sub','.idx','.nfo','.tbn','.srt','.png']   # ignored files
```
---
### to run:

with source videos supplied in the config:
```
$ python3 convert-to-hevc.py
```

OR with glob provided:
```
$ python3 convert-to-hevc.py "/home/fred/Video/LoadsOfVideos/**"
```
This will output all converted videos to the same source folder but with a '.HEVC_CONV.mkv' suffix.  With a glob provided, it will ignore all the sourcebasedir and sourcevideos config settings.

*Note: Using the glob option will use ffmpeg's best quality stream selection so may not result in the required audio\video stream*

---
### to check:

The accept-hevc.py script will search for all files with HEVC_CONV in the name and allow you to check\process them.

```
$ python3 accept-hevc.py /home/fred/Videos/ <command>
```

The commands list:

- simulate
  - This will list all of the videos found and specify the new file and the old
- review
  - This will play all found files one by one so you chan check the quality\streams
- run
  - This will replace the old file with the new converted ones, asking for confirmation of each
- run_y
  - This will replace the old file with the new converted ones without asking for confirmation
