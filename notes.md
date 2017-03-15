# Advanced Lane Finding Projects Notes

This is my scratch pad for ideas and is not official documentation.

## TO DO

In no particular order:

  - implement convolution for finding lines
    - compare convolution to sliding windows line finding by writing analysis plotting code
  - implement the smoothing algorithm and compare missed images look
  - implement not blindly searching for lane lines but using the previous lane results to speed up
    the search and collect statistics on this.

## Vidoe Sample Creation

Used the following command to create the video clips below.
```
ffmpeg -i CarND-Advanced-Lane-Lines/project_video.mp4 -ss 19 -t 6 -acodec copy -vcodec copy project_video_s19t6.mp4
```
The **GB** column below states which clips are good, bad or unclassified.

| ID | Clip Name | GB |Description |
| 1 | --- | --- |
| 2 | project_video_1s.mp4 | G | Mainly use to test algorithms
| 3 | project_video_4s.mp4 |  | |
| 4 | project_video_out.mp4 |  | |
| 5 | project_video_s20t6.mp4 | G | First problematic part of road |
| 6 | project_video_s21t2.mp4 |  | |
| 7 | project_video_s22t1.mp4 |  | |
| 8 | project_video_s23t1.mp4 |  | |
| 9 | project_video_s24t1.mp4 |  | |
| 10 | project_video_s38t5.mp4 | G | Second problematic part of the road |
| 11 | project_video_s39t2.mp4 |  | |
| 12 | project_video_s40t2.mp4 |  | |

Below -=good, x = bad

| full | s38  | s20 | Video Clip Name |  
|   |   | x | project_video_s20t6_20_100_160_205.mp4
|   |   | x | project_video_s20t6_20_100_160_225.mp4
|   |   | x | project_video_s20t6_20_100_160_255.mp4
|   |   | x | project_video_s20t6_20_100_180_205.mp4
|   |   | x | project_video_s20t6_20_100_180_225.mp4
|   |   | x | project_video_s20t6_20_100_180_255.mp4
|   |   | x | project_video_s20t6_20_100_200_205.mp4
|   |   | x | project_video_s20t6_20_100_200_225.mp4
|   |   | x | project_video_s20t6_20_100_200_255.mp4
|   |   | x | project_video_s20t6_20_120_160_205.mp4
|   |   | x | project_video_s20t6_20_120_160_225.mp4
|   |   | x | project_video_s20t6_20_120_160_255.mp4
|   |   | x | project_video_s20t6_20_120_180_205.mp4
|   |   | x | project_video_s20t6_20_120_180_225.mp4
|   |   | x | project_video_s20t6_20_120_180_255.mp4
|   |   | x | project_video_s20t6_20_120_200_205.mp4
|   |   | x | project_video_s20t6_20_120_200_225.mp4
|   |   | x | project_video_s20t6_20_120_200_255.mp4
|   |   | x | project_video_s20t6_20_80_160_205.mp4
|   |   | x | project_video_s20t6_20_80_160_225.mp4
|   |   | x | project_video_s20t6_20_80_160_255.mp4
|   |   | x | project_video_s20t6_20_80_180_205.mp4
|   |   | x | project_video_s20t6_20_80_180_225.mp4
|   |   | x | project_video_s20t6_20_80_180_255.mp4
|   |   | x | project_video_s20t6_20_80_200_205.mp4
|   |   | x | project_video_s20t6_20_80_200_225.mp4
|   |   | x | project_video_s20t6_20_80_200_255.mp4
|   | x | - | project_video_s20t6_40_100_160_205.mp4
| 7 | - | - | project_video_s20t6_40_100_160_225.mp4
| 7 | - | - | project_video_s20t6_40_100_160_255.mp4
|   |   | x | project_video_s20t6_40_100_180_205.mp4
|   | x | - | project_video_s20t6_40_100_180_225.mp4
| - | - | - | project_video_s20t6_40_100_180_255.mp4
|   |   | x | project_video_s20t6_40_100_200_205.mp4
|   |   | x | project_video_s20t6_40_100_200_225.mp4
|   |   | x | project_video_s20t6_40_100_200_255.mp4
|   | x | - | project_video_s20t6_40_120_160_205.mp4
| 8 | - | - | project_video_s20t6_40_120_160_225.mp4
| 7 | - | - | project_video_s20t6_40_120_160_255.mp4
|   |   | x | project_video_s20t6_40_120_180_205.mp4
|   | x | - | project_video_s20t6_40_120_180_225.mp4
| 8 | - | - | project_video_s20t6_40_120_180_255.mp4
|   |   | x | project_video_s20t6_40_120_200_205.mp4
|   |   | x | project_video_s20t6_40_120_200_225.mp4
|   |   | x | project_video_s20t6_40_120_200_255.mp4
|   | x | - | project_video_s20t6_40_80_160_205.mp4
| - | - | - | project_video_s20t6_40_80_160_225.mp4
| - | - | - | project_video_s20t6_40_80_160_255.mp4
|   |   | x | project_video_s20t6_40_80_180_205.mp4
|   | x | - | project_video_s20t6_40_80_180_225.mp4
| - | - | - | project_video_s20t6_40_80_180_255.mp4
|   |   | x | project_video_s20t6_40_80_200_205.mp4
|   |   | x | project_video_s20t6_40_80_200_225.mp4
|   |   | x | project_video_s20t6_40_80_200_255.mp4
