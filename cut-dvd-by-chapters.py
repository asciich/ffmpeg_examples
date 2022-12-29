#!/usr/bin/env python

import os
import logging
import json
import subprocess
from typing import Dict
from datetime import timedelta

IFO_PATH="VTS_07_0.IFO"
VIDEO_STREAM="dvd.mp4"

def check_file_exists(filename: str) -> bool:
    if not os.path.isfile(filename):
        logging.error(f"{filename} does not exist or is not a file!")
        os.exit(1)

    return True

def get_media_info_json() -> Dict:
    media_info_str = subprocess.check_output(["mediainfo", "--output=JSON", IFO_PATH]).decode()
    media_info = json.loads(media_info_str)
    return media_info

def get_main_menu_info() -> Dict:
    for track in get_media_info_json()["media"]["track"]:
        if track["@type"] != "Menu":
            continue

        if track["@typeorder"] != "1":
            continue

        return track

    raise Exception("Menu 1 not found!")

def get_general_info() -> Dict:
    for track in get_media_info_json()["media"]["track"]:
        if track["@type"] != "General":
            continue

        return track

    raise Exception("General not found!")

def get_total_video_lenght() -> float:
    return float(get_general_info()["Duration"])

def seconds_to_timestring(seconds) -> str:
    return str(timedelta(seconds=seconds))

def get_total_video_length_str() -> str:
    return seconds_to_timestring(seconds=get_total_video_lenght())

def convert_extra_timestring_to_timestring(timestring: str) -> str:
    """
    convert "_00_00_00_000" to "00:00:00.000"
    """
    timestring = timestring[1:]
    timestring = timestring.replace("_", ":", 2)
    timestring = timestring.replace("_", ".")
    return timestring

def timestring_to_seconds(timestring: str) -> float:
    splitted = timestring.split(":")
    assert len(splitted) == 3
    return float(float(splitted[0]) * 60 * 60 + float(splitted[1]) * 60 + float(splitted[2]))
    
def get_chapters_with_start_and_end_timestamp() -> Dict:
    chapters = {}

    main_menu_info = get_main_menu_info()
    extra_dict = main_menu_info["extra"]

    chapter_title = ""
    chapter_start = ""
    for timestring,title in extra_dict.items():
        if not timestring.startswith("_"):
            chapter_title = ""
            chapter_start = ""
            chapter_end = ""
            continue 

        timestring = convert_extra_timestring_to_timestring(timestring)
        if chapter_title != "":
            chapters[chapter_title] = {
                "start": chapter_start,
                "end": timestring,
                "duration": seconds_to_timestring(timestring_to_seconds(timestring) - timestring_to_seconds(chapter_start))
            }

        chapter_title = title
        chapter_start = timestring

    return chapters

def split_main_video_in_chapters():
    logging.info("Going to split main video in chapters.")
    
    chapters = get_chapters_with_start_and_end_timestamp()
    logging.info(f"Found {len(chapters)} chapters:")

    for chapter,times in chapters.items():
        chapter_title = chapter
        chapter_start = times["start"]
        chapter_end = times["end"]
        chapter_duration = times["duration"]

        logging.info(f"Chapter '{chapter_title}' from {chapter_start} to {chapter_end} with a duration of {chapter_duration}.")

        ffmpeg_cut_command = [
            "ffmpeg", 
            "-ss", chapter_start,
            "-i", "dvd.mp4",
            "-t", chapter_duration,
            "-c:v", "copy",
            "-c:a", "copy",
            chapter_title.lower().replace(" ", "_") + ".mp4"
        ]

        logging.info(f"Extract command: {ffmpeg_cut_command}")

        subprocess.check_call(ffmpeg_cut_command)

def main():
    logging.getLogger().setLevel(logging.INFO)

    for filename in [IFO_PATH, VIDEO_STREAM]:
        assert check_file_exists(filename)

    split_main_video_in_chapters()

main()