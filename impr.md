### Documentation

#### Project Structure

```
root/
    setup
    build
    reqs.txt
    server.py
    client.py
    src/
        __init__.py
        image_processing.py
        bar.jpg
        image.proto
```
#### Breakdown
* `setup` script is a bash script, it contains all the installation commands.
* `reqs.txt` is specifically for python dependencies for pip (opencv, grpc, etc.)
* `build` will generate the `image_pb2.py` and `image_pb2_grpc.py` files for grpc using `protoc`.
* I separated the generated code from `server`, `client` code and kept it inside `src` folder.
* I wrote all the image processing tasks inside `image_processing.py` **Note:** I implemented the mean filter from scratch to meet the exact definition provided, so it is not very optimized and maybe slow for a large image.
* Some usages for running the server:
	````
	python3 server.py --port 50054 --host localhost
	````
* Some usages for running the client:
	````
	python3 client.py --port 50054 --host localhost --input src/bar.jpg --output out.jpg --rotate NINETY_DEG --mean
	````

### 6 A. Limitations
* We could have caught many potential errors with `try-except` clause to make the code more robust.
* We are closing server using `KeyboardInterrupt`.
* We didn't use any proxy server in front of our simple `server.py`.
* It's already hard to catch error using grpc, we didn't use any logging system, so catching any client error like `_InactiveRpcError ` would be really hard.
* We didn't use timeouts or handle network errors.
* Another limitation is we can't easily integrate load balancers with gRPC (it's just not very common).
* I wrote a `mean()` implementation using loops without using any image processing library.

### 6 B. Improvements
* We can use `try-except` to catch many errors.
* We can use a proxy for grpc services.
* We can implement timeouts and handle network errors.
* We can add a logging system to our service to better understand the errors (if they happen).
* We can write mean with `opencv` to speedup the operation.
* We can write a `Dockerfile` for all the installation and building.
* We can write `docker-compose` to integrate the server and client under the same network.
