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

[
    {'id': 1, "name": "Ha"},
    {'id': 2, "name": "Tung"},
    {'id': 3, "name": "Phu"},
    {'id': 4, "name": "Tuan"},
    {'id': 5, "name": "Bach"},
    {'id': 6, "name": "Quan"},
    {'id': 7, "name": "Lap"},
    {'id': 8, "name": "Diem"},
    {'id': 9, "name": "Zippy"},
    {'id': 10, "name": "Tuyen"},
    {'id': 11, "name": "Tien Anh"}
]
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
