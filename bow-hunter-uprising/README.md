# Exquisite Bow Hunter Uprising

### Plan

Capture webcam stream using `getUserMedia`, send video frames through
websockets to a (python) websocket server that will run a feature detection
algorithm on each frame using [OpenCV][] and send back to the browser the
coordinates of the mass center of the colored region, which will be used as the
coordinates for the crosshair on the canvas.

Hopefully this is fast enough. I have seen pure javascript implementations that
run purely in the browser, but they seem to be good only for face detection
(hand/fist detection is spotty).


### What's done:

- Detecting center coordinates of colored regions of a jpeg image (see
  `get_centers.py`).


[OpenCV]: http://opencv.org/
