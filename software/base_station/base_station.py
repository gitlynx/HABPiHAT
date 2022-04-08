#!/usr/bin/env python3

"""
    This program connects to a Direwolf instance via KISS protocol.
    It captures the received packets and converts them into http POST
    to send them to a given list of targets.

    References used:
     - https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
"""

import argparse
import queue
from threading import Thread
import helpers.direwolf_interface as direwolf_io

message_queue = queue.Queue()

def push_message(line:str):
    """
        Direwolf read callback function
    """
    message_queue.put(line)


def pop_message():
    data = message_queue.get(timeout=1)
    if data is not None:
        print(data)

def base_station(host: str=None, port: str=None):
    """
        Set up a connection to Direwolf and start processing received messages
        Post them to the given list of targets
    """
    modem = direwolf_io.Direwolf(host, port, "ON0NOK-11", "ON4NOK")
    modem.install_read_callback(push_message)

    """
        Process receives messages
    """
    while True:
        pop_message()


def argumentparsing():
    '''
        Parse commandline arguments and return an argument namespace
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Direwolf host name (or IP)", type=str)
    parser.add_argument("port", help="Direworl IP port", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    
    arg_namespace = argumentparsing()

    if arg_namespace.host and arg_namespace.port:
        print(f"Client to {arg_namespace.host} {arg_namespace.port}")
        base_station(arg_namespace.host, arg_namespace.port)
    else:
        print("Not all required parameters given")
        pass        
