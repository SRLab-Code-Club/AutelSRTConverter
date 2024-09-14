# Summary
 Convert the Autel srt file to dji format for photogrammetry use.
   
# Purpose  
During shooting a video footage for field investigation, the GPS track is helpful to review the video data. Some power user might want to extract some frames from the video and build a model using photogrammetry tools. Some popular drones have an embedded subtitle track or external  subtitle file which records the position and/or orientation of the camera. Some commercial photogrammetry software (e.g. Metashape) already support the feature to geotag the frames based on the subtitle file but only with specific format (e.g. DJI format). This project aims to convert the subtitle from Autel format into the DJI format so user can have better inital parameters in photogrammetry processing.  
  
# Dependencies  
* [srt](https://pypi.org/project/srt/) (MIT License)  
  
# Tested drone
* Autel EVO Nano+  
  
# How to use  
## Pre-processing  
Using the ffmpeg to extract the srt file from the video footage using the command:  
`ffmpeg -txt_format txt -i /Path/to/Video.mp4 /Path/to/Video.srt`  
## Run this program
`python AutelSrtConverter.py /Path/to/Video.srt`  
## After executing the script  
The output file will be named as '/Path/to/Video.a2d.srt' in case of conflicting with pre-existed srt file. To use in the photogrammetry softwate, rename the file to the same name as the video footage (e.g. if the name of video is 'DroneVideo.mp4', name the srt file as 'DroneVideo.srt').
  
# Some other details    
Since the field is not 1-to-1 from different format, only the necessary information will be transfered. More format might be support in the future with the help of the community,  
## Source format
**Autel Nano+**    
Example Content: 
```
HOME(E: 120.000000, N: 20.000000) 2000-00-00 12:00:01
GPS(E: 120.000001, N: 20.000001, 001.01m) 
ISO:100 SHUTTER:30 EV:0.0 F-NUM:2.8 
F.PRY (-1.0°, 1.0°, 100.1°), G.PRY (0.0°, 0.0°, 100.2°)
```
## Target format  
**DJI Mini 2**  
Example content: 
```
F/2.8, SS 1000.10, ISO 100, EV 0, DZOOM 1.000, GPS (120.0001, 20.0001, 26), D 30m, H 10.00m, H.S 2m/s, V.S 0.10m/s 
```

# Author
[Cheng-Wei Sun](https://github.com/lcabon258) 

Initial release: 2024-09-14

