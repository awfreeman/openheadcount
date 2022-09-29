# OpenHeadCount
A web application for counting the number of people that enter and exit a business. It uses the MobilenetSSD pretrained neural network to detect the position of people within a frame of video, and uses position tracking to determine when a person crosses the user-defined threshold for being inside the business. 

## Running
In order to run OpenHeadCount, you will need Python 3 and a number of dependencies, which can be installed with the following command:
```bash
pip install opencv-python numpy flask pandas scipy bcrypt imutils
```

After installing the dependencies, use the following command to start OpenHeadCount:
```bash
python server.py
```
This will use the development server included with Flask. For production use, use a WSGI-compliant web server of your choice. 
