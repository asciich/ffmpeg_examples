# FFMPEG cheatsheet

## General

* Some common parameters

```
-y  Automatically overwrite output file if exists. (Do not ask)
```

## Single image handling

* Extract first frame as JPG
```
ffmpeg -i in.mp4 -vframes 1 -q:v 2 output.jpg
```

* Extract frame at given time (in this example after 5 seconds = 00:00:05) as JPG
```
ffmpeg -ss 00:00:05 -i in.mp4 -vframes 1 -q:v 2 output.jpg
```

## 360 degree image handling
**See next chapter for 360 degree video handling**

The [samsung_gear_360_in.jpg](example_images/samsung_gear_360_in.jpg) image is used as example image.

![Alt text](example_images/samsung_gear_360_in.jpg?raw=true "samsung_gear_360_in")

## 360 degree video handling
**See prevous chapter for 360 degree image hangdling**

## Sources

* [FFMPEG Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)