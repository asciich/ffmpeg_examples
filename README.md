# FFMPEG cheatsheet

## General

* Some common parameters

    ```
    -y  Automatically overwrite output file if exists. (Do not ask)
    ```

## Video handling

### Extract part of video

Use ```-ss``` to set the start time, ```-t``` to set the duration:

```
ffmpeg -ss 00:00:10 -i in.mp4 -t 00:00:20 -c:v copy out.mp4
```

### Reduce video file size (same resolution)

Using H.265 codec (or H.264 if faster encoding time is needed) to significantly reduce video file size without lowering the quality noticeably.
Resulting file size should be less than 35% of original file size.

* Reduce file size by using H.265 codec (slower encoding but smaller video than H.254)
    ```
    ffmpeg -i in.mp4 -c:v libx265 -pix_fmt yuv420p -crf 24 out.mp4
    ```

* Reduce file size even more and speed up H.265 encoding with minimal quality reduction:
    ```
    ffmpeg -i in.mp4 -c:v libx265 -pix_fmt yuv420p -crf 24 -preset ultrafast out.mp4
    ```

* Reduce file size by using H.264 codec (faster encoding than H.265 but bigger files)
    ```
    ffmpeg -i in.mp4 -c:v libx264 -pix_fmt yuv420p -crf 24 out.mp4
    ```


## Single image handling

* Extract first frame from video as JPG
    ```
    ffmpeg -i in.mp4 -vframes 1 -q:v 2 output.jpg
    ```

* Extract frame at given time (in this example after 5 seconds = 00:00:05) from video as JPG
    ```
    ffmpeg -ss 00:00:05 -i in.mp4 -vframes 1 -q:v 2 output.jpg
    ```

## 360 degree image handling
**See next chapter for 360 degree video handling**

The [samsung_gear_360_in.jpg](example_images/samsung_gear_360_in.jpg) image is used as example image:

<img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_in.jpg" height="150" />

* Extract left fisheye to single image:

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:0:0" samsung_gear_360_left_fisheye.jpg
    ```
    Result:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_left_fisheye.jpg" height="150" />

* Extract right fisheye to single image:

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:0:0" samsung_gear_360_right_fisheye.jpg
    ```
    Result:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_right_fisheye.jpg" height="150" />

* Equirectangular projection of left fisheye projection

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:0:0,v360=input=fisheye:output=e:ih_fov=191.5:iv_fov=191.5" samsung_gear_360_left_equirectangular.jpg
    ```
    Result:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_left_equirectangular.jpg" height="150" />

* Equirectangular projection of right fisheye projection

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:iw/2:0,v360=input=fisheye:output=e:ih_fov=191.5:iv_fov=191.5" samsung_gear_360_right_equirectangular.jpg
    ```
    Result:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_right_equirectangular.jpg" height="150" />

    For a 180 degree rotation:
    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:iw/2:0,v360=input=fisheye:output=e:yaw=180:ih_fov=191.5:iv_fov=191.5" samsung_gear_360_right_equirectangular_yaw180.jpg
    ```

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_right_equirectangular_yaw180.jpg" height="150" />

* Equirectangular projection of both fisheye projections:

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "v360=input=dfisheye:output=e:ih_fov=191.5:iv_fov=191.5" samsung_gear_360_equirectangular.jpg
    ```
    Results:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_equirectangular.jpg" height="150" />

    For 180 degree yaw rotation use:
    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "v360=input=dfisheye:output=e:ih_fov=191.5:iv_fov=191.5:yaw=180" samsung_gear_360_equirectangular_yaw180.jpg
    ```
    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_equirectangular_yaw180.jpg" height="150" />

* Equirectangular projection of both fisheye projections with mergemap:

    Source: [http://www.astro-electronic.de/FFmpeg_Book.pdf](http://www.astro-electronic.de/FFmpeg_Book.pdf)

    ```
    # Create mergemap
    H=1920 # Height in px
    FOV=191.5 # FieldOfView angle in degrees
    C=11.5 # Overlap degrees
    ffmpeg -f lavfi -i nullsrc=size=${H}x${H} -vf "format=gray8,geq='clip(128-128/${C}*(180-${FOV}/(${H}/2)*hypot(X-${H}/2,Y-${H}/2)),0,255)',v360=input=fisheye:output=e:ih_fov=${FOV}:iv_fov=${FOV}" -frames 1 -y mergemap.png

    # Transform image
    ffmpeg -i samsung_gear_360_in.jpg -i mergemap.png -filter_complex \
        "[0]format=bgr24[double_fisheye_in];
        [0]format=bgr24[double_fisheye_inx];
        [double_fisheye_in]crop=ih:iw/2:0:0[right_fisheye_in];
        [double_fisheye_inx]crop=ih:iw/2:iw/2:0[left_fisheye_in];
        [right_fisheye_in]v360=input=fisheye:output=e:ih_fov=${FOV}:iv_fov=${FOV}[right_equirectangular_part];
        [left_fisheye_in]v360=input=fisheye:output=e:ih_fov=${FOV}:iv_fov=${FOV}:yaw=180[left_equirectangular_part];
        [1]format=gbrp[mask];
        [right_equirectangular_part][left_equirectangular_part][mask]maskedmerge" \
        -y samsung_gear_360_equirectangular_mergedmask.jpg
    ```

    Result:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_equirectangular_mergedmask.jpg" height="150" />


## 360 degree video handling
**See previous chapter for 360 degree image handling**

This example video is used (created by a Samsung Gear 360 camera):

[![Watch the video](https://img.youtube.com/vi/fqS-aQObaNI/mqdefault.jpg)](https://youtu.be/fqS-aQObaNI)

* Equirectangular projection of both fisheye projections with mergemap:

    Source: [http://www.astro-electronic.de/FFmpeg_Book.pdf](http://www.astro-electronic.de/FFmpeg_Book.pdf)

    ```
    # Create mergemap
    H=1920 # Height in px
    FOV=191.5 # FieldOfView angle in degrees
    C=11.5 # Overlap degrees
    ffmpeg -f lavfi -i nullsrc=size=${H}x${H} -vf "format=gray8,geq='clip(128-128/${C}*(180-${FOV}/(${H}/2)*hypot(X-${H}/2,Y-${H}/2)),0,255)',v360=input=fisheye:output=e:ih_fov=${FOV}:iv_fov=${FOV}" -frames 1 -y mergemap.png

    # Transform image
    ffmpeg -i samsung_gear_360_demo_original.mp4 -i mergemap.png -filter_complex \
        "[0]format=bgr24[double_fisheye_in];
        [0]format=bgr24[double_fisheye_inx];
        [double_fisheye_in]crop=ih:iw/2:0:0[right_fisheye_in];
        [double_fisheye_inx]crop=ih:iw/2:iw/2:0[left_fisheye_in];
        [right_fisheye_in]v360=input=fisheye:output=e:ih_fov=${FOV}:iv_fov=${FOV}[right_equirectangular_part];
        [left_fisheye_in]v360=input=fisheye:output=e:ih_fov=${FOV}:iv_fov=${FOV}:yaw=180[left_equirectangular_part];
        [1]format=gbrp[mask];
        [right_equirectangular_part][left_equirectangular_part][mask]maskedmerge" \
        -c:v libx265  -b:v 40000k -preset ultrafast samsung_gear_360_equirectangular_mergedmask.mp4
    ```

    Result:

    [![Watch the video](https://img.youtube.com/vi/vBUfldo4JuU/mqdefault.jpg)](https://youtu.be/vBUfldo4JuU)

    Result as 360 degree video (correct metadata added before uploading to Youtube):

    [![Watch the video](https://img.youtube.com/vi/fZoOJqdZ18s/mqdefault.jpg)](https://youtu.be/fZoOJqdZ18s)

## Sources

* [FFMPEG Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)
* [http://www.astro-electronic.de/FFmpeg_Book.pdf](http://www.astro-electronic.de/FFmpeg_Book.pdf)
