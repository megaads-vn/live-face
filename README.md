# live-face
run:
```
python __init__.py
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

Data example:
```
GET:
http://127.0.0.1:5000/data-users
```
