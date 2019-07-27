# live-face
Required:
```
Python 3, openCV, Flask restful, pillow
```
run on MAC OR PC:
```
python __init__.py
```
run on Pi:
```
sudo -s
export DISPLAY=:0
modprobe bcm2835-v4l2
python __init__.py
```
Data example:
```
GET:
http://127.0.0.1:5000/data-users
```


Data Gathering:

```
POST:
http://127.0.0.1:5000/live-face-data-set
{
    "id": 1
}
```

Trainer:

```
GET:
http://127.0.0.1:5000/live-face-training
```

Turn on Recognizer:

```
POST:
http://127.0.0.1:5000/live-face-recognition
```

Turn off Camera:

```
POST:
http://127.0.0.1:5000/live-face-off-camera
```
