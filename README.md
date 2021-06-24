# py-grpc-opencv
Python gRPC server, client with opencv (image manipulation boilerplate)


#### Solution:

1. Install a fresh Ubuntu 18.04 installation. (I used `docker pull ubuntu:18.04` from [docker-hub](https://hub.docker.com/layers/ubuntu/library/ubuntu/18.04/images/sha256-c60266b67f58fafc30703315f617a8fcccaffc48ef5534ca5f67a9ba3aceb3b8?context=explore))
2. Make sure, **you are the root** (to avoid sudo), and make the scripts executable by running (in the same folder):
    ```
    chmod +x setup
    chmod +x build
    ```
3. To install all the dependencies, run `./setup`
4. To build the source code, run `./build`
5. Now, for running the server, we can try:
    ```
    python3 server.py
    ```
    **Arguments:**
    ```
    '--port', default=50054, type=int, help="Server listening port"
    '--host', default='127.0.0.1', type=str, help="Server listening host"
    ```
6.  For running the client, we can try:
    ```
    python3 client.py
    ```
    **Arguments:**
    ```
	'--port', default=50054, type=int, help="Client listening port"

	'--host', default='127.0.0.1', type=str, help="Client listening host"

	'--input', default='src/bar.jpg', type=str, help="Input image path"

	'--output', default='out.jpg', type=str, help="Output image path"

	'--rotate', default="NONE", type=str, help="Rotation degree", options: ["NINETY_DEG",          "ONE_EIGHTY_DEG", "TWO_SEVENTY_DEG", "NONE"]

	'--mean', action='store_true', help="Mean filter"
    ```

#### Using docker:

Run the commands sequentially.
```
apt update
apt install docker.io
docker pull ubuntu:18.04
docker build -it --net=host ubuntu:18.04 bash
apt install git
git clone https://github.com/zabir-nabil/py-grpc-opencv.git
cd py-grpc-opencv
```
Now, start from 1.

