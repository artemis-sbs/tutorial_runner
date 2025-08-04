"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""

import argparse
import math

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

from multiprocessing import shared_memory
shm_a = shared_memory.SharedMemory(name="art_test")


client = None
count = 0
def print_volume_handler(unused_addr, args, volume):
    global count
    print("[{0}] ~ {1}".format(args[0], volume))
    print("addr: {0}".format(unused_addr))
    if client is not None:
        n = shm_a.buf[0]
        t = shm_a.buf[1] / 50.0 # make float
        
        print(f"Sending data /fred {n} {t}")
        
        client.send_message("/fred",f"test {count} {n} {t}")
        count += 1




def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
        shm_a.buf[5] = int(abs(volume) * 50.0)
        shm_a.buf[6] = 1
        t = shm_a.buf[5]
        print(f"Setting throttle {t}")
    except ValueError:
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    client = SimpleUDPClient("127.0.0.1", 5004)

    dispatcher = Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/volume", print_volume_handler, "Volume")
    dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
