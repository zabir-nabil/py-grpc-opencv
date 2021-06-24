import sys
sys.path.append("/home/grpc/src") # export is better

import grpc
from concurrent import futures
import time
import argparse
import numpy as np
import cv2

import src.image_processing as ip
# import the generated classes
from src import image_pb2_grpc, image_pb2


# based on .proto service
class ImageProcedureServicer(image_pb2_grpc.NLImageServiceServicer):

    def RotateImage(self, request, context):
        response = image_pb2.NLImage()

        # we don't need the meta data for color, shape
        img_data = request.image.data
        img = cv2.imdecode(np.fromstring(img_data, dtype='uint8'), 1)
        #print(img.shape)
        #print(img.shape)
        #cv2.imwrite("out.jpg", img)
        # get the rotation flag
        rot_flag = "NONE"
        
        # we are doing all grpc related conversion here
        if request.rotation == image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG:
            rot_flag = "NINETY_DEG"
        elif request.rotation == image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG:
            rot_flag = "ONE_EIGHTY_DEG"
        elif request.rotation == image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG:
            rot_flag = "TWO_SEVENTY_DEG"
        #print(rot_flag)

        img = ip.rotate(img, rot_flag)
        #print(img.shape)
        response.data = cv2.imencode('.jpg', img)[1].tobytes()
        # set the other args
        response.color = request.image.color
        response.width = request.image.width 
        response.height = request.image.height
        #print(response)
        return response

    def MeanFilter(self, request, context):
        response = image_pb2.NLImage()

        # we don't need the meta data for color, shape
        img = cv2.imdecode(np.fromstring(request.data, dtype='uint8'), 1)
        #print(img.shape)
        #print(img.shape)
        #cv2.imwrite("out.jpg", img)
        img = ip.mean(img)
        #print(img.shape)
        response.data = cv2.imencode('.jpg', img)[1].tobytes()
        # set the other args
        response.color = request.color
        response.width = request.width 
        response.height = request.height
        return response

# argument parsing
my_parser = argparse.ArgumentParser(description='gRPC server args')
my_parser.add_argument('--port', default=50054, type=int, help="Server listening port")
my_parser.add_argument('--host', default='127.0.0.1', type=str, help="Server listening host")

args = my_parser.parse_args()

host = args.host
port = args.port

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))
# add the defined class to the server
image_pb2_grpc.add_NLImageServiceServicer_to_server(
        ImageProcedureServicer(), server)

# listen on port
print(f'Starting server. Listening on port {port} for {host}.')
server.add_insecure_port(f'{host}:{port}')
server.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    server.stop(0)