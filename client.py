import sys
sys.path.append("/home/grpc/src")

import grpc

# import the generated classes
from src import image_pb2, image_pb2_grpc

# data encoding
import numpy as np 
import cv2

# arg parsing
import argparse

# argument parsing
my_parser = argparse.ArgumentParser(description='gRPC server args')
my_parser.add_argument('--port', default=50054, type=int, help="Client listening port")
my_parser.add_argument('--host', default='127.0.0.1', type=str, help="Client listening host")
my_parser.add_argument('--input', default='src/bar.jpg', type=str, help="Input image path")
my_parser.add_argument('--output', default='out.jpg', type=str, help="Output image path")
my_parser.add_argument('--rotate', default="NONE", type=str, help="Rotation degree")
my_parser.add_argument('--mean', action='store_true', help="Mean filter")

args = my_parser.parse_args()

host = args.host
port = args.port
inp_path = args.input
out_path = args.output
rot_deg = args.rotate
mean_arg = args.mean 

# print(host, port, inp_path, out_path, rot_deg, mean_arg)

# open a gRPC channel
channel = grpc.insecure_channel(f'{host}:{port}', options=(('grpc.enable_http_proxy', 0),))

# create a stub (client)
stub = image_pb2_grpc.NLImageServiceStub(channel)

# encoding image/numpy array
for _ in range(1): # loop if continuous reading is needed
    # np.random.randint(0,255, (416,416,3), dtype=np.uint8) # dummy rgb image
    frame = cv2.imread(inp_path)
    data = cv2.imencode('.jpg', frame)[1].tobytes()
    # create a valid request message
    image_req = image_pb2.NLImage(color = True, data = data, width = frame.shape[1], height = frame.shape[0])

    if rot_deg != "NONE": # if NONE, we don't need any rotation, so just ignoring
        main_req_obj = image_pb2.NLImageRotateRequest()
        main_req_obj.image.data = image_req.data
        main_req_obj.image.color = image_req.color
        main_req_obj.image.height = image_req.height
        main_req_obj.image.width = image_req.width
        if rot_deg == "NINETY_DEG":
            main_req_obj.rotation = image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG
        elif rot_deg == "ONE_EIGHTY_DEG":
            main_req_obj.rotation = image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG
        elif rot_deg == "TWO_SEVENTY_DEG":
            main_req_obj.rotation = image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG
        else:
            main_req_obj.rotation = image_pb2.NLImageRotateRequest.Rotation.NONE
        
        # finally, call the rotation service
        image_req = stub.RotateImage(main_req_obj)

    # make the call
    if mean_arg == True:
        image_req = stub.MeanFilter(image_req)
    
    # reconstruct the image
    img_data = image_req.data
    img = cv2.imdecode(np.fromstring(img_data, dtype='uint8'), 1)
    cv2.imwrite(out_path, img)

