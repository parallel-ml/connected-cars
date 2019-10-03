import asyncio
import base64
import os
import struct

import websockets

from roboviz import MapVisualizer

MAP_SIZE_PIXELS = int(os.environ.get("SLAM_MAP_SIZE_PIXELS", "500"))
MAP_SIZE_METERS = int(os.environ.get("SLAM_MAP_SIZE_METERS", "10"))
MAP_BYTES_SIZE = int(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
STRUCT_FORMAT = f"<fff{MAP_BYTES_SIZE}s"

# Set up a SLAM display
viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, "SLAM")

async def data_handler(websocket, path):
    data = await websocket.recv()
    while data:
        x, y, theta, mapbytes_str = struct.unpack(STRUCT_FORMAT, data)
        mapbytes = bytearray(mapbytes_str)

        if not viz.display(x, y, theta, mapbytes):
            exit(0)
        data = await websocket.recv()


if __name__ == "__main__":
    start_server = websockets.serve(data_handler, host="0.0.0.0")
    asyncio.run(start_server)
