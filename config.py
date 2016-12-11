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

allowedcodecs = ['x264','h264','mp4v','xvid','div3','mpeg4','mpeg2video']
skippedfiles = ['.jpg','.sub','.idx','.nfo','.tbn','.srt','.png']

# any files smaller than this will be ignored (800MB)
minimumvidsize = 800000000
