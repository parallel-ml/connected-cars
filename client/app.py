import asyncio
import base64
import multiprocessing as mp
import os
import struct
from concurrent.futures.process import ProcessPoolExecutor

import requests
import websockets
from rplidar import RPLidar as Lidar

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel

LIDAR_DEVICE = os.environ.get("SLAM_LIDAR_DEVICE", "/dev/ttyUSB0")
MIN_SAMPLES = int(os.environ.get("SLAM_MIN_SAMPLES", "200"))
SERVER_URL = os.environ.get("SLAM_SERVER_URL", "ws://localhost:80")

MAP_SIZE_PIXELS = int(os.environ.get("SLAM_MAP_SIZE_PIXELS", "500"))
MAP_SIZE_METERS = int(os.environ.get("SLAM_MAP_SIZE_METERS", "10"))
MAP_BYTES_SIZE = int(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
STRUCT_FORMAT = f"<fff{MAP_BYTES_SIZE}s"

async def send_info(x, y, theta, mapbytes):
    async with websockets.connect(SERVER_URL) as websocket:
        packed = struct.pack(STRUCT_FORMAT, x, y, theta, mapbytes)
        websocket.send(packed)

def send_info_process(x, y, theta, mapbytes):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_info(x, y, theta, mapbytes))

def main():
    with ProcessPoolExecutor(5) as executor:
        event_loop = asyncio.get_event_loop()

        # Connect to Lidar unit
        lidar = Lidar(LIDAR_DEVICE)

        # Create an RMHC SLAM object with a laser model and optional robot model
        slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

        # Initialize an empty trajectory
        trajectory = []

        # Initialize empty map
        mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

        # Create an iterator to collect scan data from the RPLidar
        iterator = lidar.iter_scans()

        # We will use these to store previous scan in case current scan is inadequate
        previous_distances = None
        previous_angles = None

        # First scan is crap, so ignore it
        next(iterator)

        while True:
            # Extract (quality, angle, distance) triples from current scan
            items = [item for item in next(iterator)]

            # Extract distances and angles from triples
            distances = [item[2] for item in items]
            angles = [item[1] for item in items]

            # Update SLAM with current Lidar scan and scan angles if adequate
            if len(distances) > MIN_SAMPLES:
                slam.update(distances, scan_angles_degrees=angles)
                previous_distances = distances.copy()
                previous_angles = angles.copy()

            # If not adequate, use previous
            elif previous_distances is not None:
                slam.update(previous_distances, scan_angles_degrees=previous_angles)

            # Get current robot position
            x, y, theta = slam.getpos()

            # Get current map bytes as grayscale
            slam.getmap(mapbytes)

            mp.Process(target=send_info_process,args=(x,y,theta,mapbytes)).start()

        # Shut down the lidar connection
        lidar.stop()
        lidar.disconnect()


if __name__ == "__main__":
    main()
