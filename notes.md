# Advanced Lane Finding Projects Notes

## TO DO

In no particular order:

  - with present algorithm
    - save all the frames to a directory
    - run code collect all values and correlate them to a frames
    - do the same thing for partial frame and see if I can correlate that with the full video
  - implement convolution for finding lines
  - compare convolution to sliding windows line finding by writing analysis plotting code
  - write a loop to test different threshold values for the difficult train part and
    collect the missed frames and chose the best setting
  - write routines to save images for bad line identification and then manually
    see how I can improve it
  - figure out why the radius of curvature go nuts in some part of the graph
  - implement the smoothing algorithm and compare missed images look
  - implement not blindly searching for lane lines but using the previous lane results to speed up
    the search and collect statistics on this.

## Vidoe Sample Creation

Used the following command to create the video clips below.
```
ffmpeg -i CarND-Advanced-Lane-Lines/project_video.mp4 -ss 19 -t 6 -acodec copy -vcodec copy project_video_s19t6.mp4
```
The **GB** column below states which clips are good, bad or unclassified.

| Clip Name | GB |Description |
| --- | --- |
| project_video_1s.mp4 | G | Mainly use to test algorithms
| project_video_4s.mp4 |  | |
| project_video_out.mp4 |  | |
| project_video_s20t6.mp4 | G | First problematic part of road |
| project_video_s21t2.mp4 |  | |
| project_video_s22t1.mp4 |  | |
| project_video_s23t1.mp4 |  | |
| project_video_s24t1.mp4 |  | |
| project_video_s38t5.mp4 | G | Second problematic part of the road |
| project_video_s39t2.mp4 |  | |
| project_video_s40t2.mp4 |  | |
