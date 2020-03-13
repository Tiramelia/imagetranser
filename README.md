# imagetranser
Imagetranser is a simple program for adding a transgender pride flag to images.

## usage
```
usage: imagetranser [-h] {merge,frame,color} ...

Adding trans flag to images in various ways.

positional arguments:
  {merge,frame,color}  For more help type imagetranser.py command -h
    merge              Merges image with a transgender flag.
    frame              Adds a transgender flag frame.
    color              Change a color within a specified range and turn it
                       into a transgender flag (used mostly for changing the
                       background).

optional arguments:
  -h, --help           show this help message and exit
  ```
### merge
```
usage: imagetranser merge [-h] file

positional arguments:
  file        Path to the image file.
```
### frame
```
usage: imagetranser frame [-h] [-w [width]] file

positional arguments:
  file                  Path to the image file.

optional arguments:
  -h, --help            show this help message and exit
  -w [width], --width [width]
                        Width of the frame.
```
### color
```
usage: imagetranser color [-h] [-t [threshold]] [-c [colorhex]] file

positional arguments:
  file                  Path to the image file.

optional arguments:
  -h, --help            show this help message and exit
  -t [threshold], --threshold [threshold]
                        Color threshold.
  -c [colorhex], --colorhex [colorhex]
                        Color hex e.g ff00ff (without #)
```
