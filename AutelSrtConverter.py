# -*- coding: utf-8 -*-
""" Convert the Autel srt file to dji format for photogrammetry use.
Author: Cheng-Wei Sun
Initial release: 2024-09-14
"""
from pathlib import Path
import re
from dataclasses import dataclass
import logging
import argparse
# Third-party
import srt


@dataclass
class DjiMini2SrtMessage():
    """Assistant class to export the SRT message of DJI mini 2.
    Sample massage:
    F/2.8, SS 1667.11, ISO 100, EV 0, DZOOM 1.000, GPS (120.3534, 23.1201, 26), D 499.16m, H 98.00m, H.S 4.81m/s, V.S 0.10m/s 
    """
    f_step:float = 0. #aperture 
    ss:float = 0. # shutter speed
    iso:int = 0
    ev:float = 0. 
    dzoom:float = 0.
    gps_lon:float = 0.
    gps_lat:float = 0.
    gps_sats:int = 0
    home_distance:float = 0.
    altitude:float = 0.
    horizontal_speed:float = 0.
    vertical_speed:float = 0.
    def toSrtMessage(self):
        """Export to SRT message."""
        return f"""F/{str(self.f_step)}, SS {str(self.ss)}, ISO {str(self.iso)}, EV {str(self.ev)}, DZOOM {str(self.dzoom)}, GPS ({str(self.gps_lon)}, {str(self.gps_lat)}, {str(self.gps_sats)}), D {str(self.home_distance)}m, H {str(self.altitude)}m, H.S {str(self.horizontal_speed)}m/s, V.S {str(self.vertical_speed)}m/s """

# re patterns
GPS_pattern = re.compile(r"GPS\((?P<ew>[EW]):\s+(?P<lon>\d+\.\d+)\,\s+(?P<ns>[NS]):\s+(?P<lat>\d+\.\d+),\s+(?P<alt>\d+.\d+)m\)")
Camera_pattern = re.compile(r"ISO:(?P<iso>\d+)\s+SHUTTER:(?P<shutter>\d+\.?\d*)\s+EV:(?P<ev>\d+\.\d+)\s+F\-NUM:(?P<f_num>\d+\.\d+)")

def convertAutelSrtToDji(pathOfAutelSrt:Path)->Path:
    """Convert the Autel Srt file to DJI format for photogrammetry.
    Input:
        pathOfAutelSrt:Path The input path of the Autel-format srt file.
    Output:
        outputPath:Path The output srt file located in the same directory of the pathOfAutelSrt with the suffix '.a2d.srt'. 
    """
    AutelSrtPath:Path = Path(pathOfAutelSrt)
    # Read all content and parse the srt content
    with open(AutelSrtPath,"rt") as autelSrtFile:
        autelSrtString = autelSrtFile.read()
    AutelSrtGenerator = srt.parse(autelSrtString)

    # Process the srt
    autelSubs:list[srt.Subtitle] = []
    for a_sub in AutelSrtGenerator:
        # Try to extract the gps and camera data
        GPS_match = re.search(GPS_pattern,a_sub.content)
        Camera_match = re.search(Camera_pattern,a_sub.content)
        
        # If not match, continue.
        if not GPS_match or not Camera_match:
            logging.error(f"The format does not match. Contents:{a_sub.content}")
            continue        
        else:
            GPS_match_dict = GPS_match.groupdict()
            Camera_match_dict = Camera_match.groupdict()
            gps_lon=0.
            gps_lat=0.
            if GPS_match_dict["ew"] == "W":
                gps_lon = -float(GPS_match_dict["lon"])
            else:
                gps_lon = float(GPS_match_dict["lon"])
            if GPS_match_dict["ns"] == "S":
                gps_lat = -float(GPS_match_dict["lat"])
            else:
                gps_lat = float(GPS_match_dict["lat"])
            djiFormatMsg = DjiMini2SrtMessage(
                f_step=float(Camera_match_dict["f_num"]),
                ss=float(Camera_match_dict["shutter"]),
                iso=int(Camera_match_dict["iso"]),
                ev=float(Camera_match_dict["ev"]),
                gps_lon=gps_lon,
                gps_lat=gps_lat,
                altitude=float(GPS_match_dict["alt"])
                )
            # Replace content of the subtitle
            a_sub.content = djiFormatMsg.toSrtMessage()
            autelSubs.append(a_sub)
    # print(srt.compose(autelSubs))
    # Save the file
    outputPath:Path = AutelSrtPath.with_suffix(".a2d.srt")
    with open(outputPath,"wt",encoding="utf-8") as fOut:
        fOut.write(srt.compose(autelSubs))
    return outputPath

def main():
    parser = argparse.ArgumentParser(description='Convert Autel Srt file to DJI format')
    parser.add_argument('inputSrt', type=Path, help='Path to the input Autel Srt file')
    args = parser.parse_args()

    inputSrt = args.inputSrt
    newSrt = convertAutelSrtToDji(inputSrt)
    print(f"Conversion complete. Output file: {newSrt}")

if __name__ == "__main__":
    main()
