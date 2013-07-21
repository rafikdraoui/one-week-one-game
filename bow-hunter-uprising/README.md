# Exquisite Bow Hunter Uprising

Your home is occupied by the British Empire. You, an exquisite bow hunter, have
had enough.

### Original Plan

Capture webcam stream using `getUserMedia`, send video frames through
websockets to a (python) websocket server that will run a feature detection
algorithm on each frame using [OpenCV][] and send back to the browser the
coordinates of the mass center of the colored region, which will be used as the
coordinates for the crosshair on the canvas.

Hopefully this is fast enough. I have seen pure javascript implementations that
run purely in the browser, but they seem to be good only for face detection
(hand/fist detection is spotty).

### Scaled Down Plan

Turns out that sending images from the browser to the server and drawing on the
canvas is too slow, so instead the game will happen purely in python, using
OpenCV to show the video with the crosshair and enemy drawings on top of it.


### How to play

Make sure that you have [OpenCv][] installed. On OS X, the easiest way is to
use [Homebrew][]:

```
brew tap homebrew/science
brew install opencv
```

Find an object that is not too shiny and has a color distinct from the
background. Find the range of HSV values for this color (maybe with the help of
`get_color.py`) and set those values as `MIN_T` and `MAX_T` in `game.py`.

To start the game, run `python game.py`. To control the crosshair, move the
object in front of a webcam. To shoot, press the space bar.


[OpenCV]: http://opencv.org/
[Homebrew]: http://brew.sh/
