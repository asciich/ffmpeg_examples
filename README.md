# FFMPEG cheatsheet

## General

* Some common parameters

    ```
    -y  Automatically overwrite output file if exists. (Do not ask)
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
    Results in:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_left_fisheye.jpg" height="150" />

* Extract right fisheye to single image:

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:0:0" samsung_gear_360_right_fisheye.jpg
    ```
    Results in:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_right_fisheye.jpg" height="150" />

* Equirectangular projection of left fisheye projection

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:0:0,v360=input=fisheye:output=e:ih_fov=191.5:iv_fov=191.5" samsung_gear_360_left_equirectangular.jpg
    ```
    Results in:

    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_left_equirectangular.jpg" height="150" />

* Equirectangular projection of right fisheye projection

    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "crop=ih:iw/2:iw/2:0,v360=input=fisheye:output=e:ih_fov=191.5:iv_fov=191.5" samsung_gear_360_right_equirectangular.jpg
    ```
    Results in:

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
    Results in:
    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_equirectangular.jpg" height="150" />

    For 180 degree yaw rotation use:
    ```
    ffmpeg -i samsung_gear_360_in.jpg -filter_complex "v360=input=dfisheye:output=e:ih_fov=191.5:iv_fov=191.5:yaw=180" samsung_gear_360_equirectangular_yaw180.jpg
    ```
    <img src="https://raw.githubusercontent.com/asciich/ffmpeg_examples/main/example_images/samsung_gear_360_equirectangular_yaw180.jpg" height="150" />





## 360 degree video handling
**See prevous chapter for 360 degree image hangdling**

## Sources

* [FFMPEG Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)