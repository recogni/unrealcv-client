#!/usr/bin/env python

'''
RecogniCV
=========

    Interact with the UnrealCV plugin installed on the UE4 engine.

TODO: Usage

'''
import argparse
import select
import sys
import socket
import struct
import math
import ctypes


################################################################################
#
#   Constants.
#
MAGIC_NUMBER = ctypes.c_uint32(0x9E2B83C1).value


################################################################################
#
#   Decorators.
#
def static_counter(counter_name):
    def decorate(func):
        setattr(func, counter_name, 0)
        return func
    return decorate


################################################################################
#
#   Helper functions.
#
#   Send and receive based on the current UnrealCV plugin's expected payload.
#   Eventually we will modify this to speak our own protocol for whatever
#   plugin we develop / modify.
#
#   The current payload to send is the magic number 0x9E2B83C1, followed by 4
#   bytes of size followed by `size` bytes of payload.  This send method does
#   not worry about the contents of the payload, but just sends it.  It is the
#   responsibility of the caller to increment any auto-id's that the server
#   might need to keep track of requests.
#
@static_counter("counter")
def send(socket, msg):
    msg = "%d:%s" % (send.counter, msg)
    fout = socket.makefile('wb', -1)
    try:
        fout.write(struct.pack("I", MAGIC_NUMBER))
        fout.write(struct.pack("I", len(msg)))
        fout.write(msg.encode("UTF-8"))
        fout.flush()
        fout.close()
        send.counter += 1
    except Exception as e:
        print "Unable to send payload to socket"
        return


def receive(socket):
    fin = socket.makefile('rb', 0)
    try:
        magic = fin.read(4)
        if struct.unpack("I", magic)[0] != MAGIC_NUMBER:
            print "Malformed packet, bad magic number!"
            return None
    except Exception as e:
        print "Failed to read magic number"
        return None

    paysz = struct.unpack("I", fin.read(4))[0]
    payld = b""
    szleft = paysz
    while szleft > 0:
        data = fin.read(szleft)
        if not data:
            return None
        payld += data
        szleft -= len(data)
    fin.close()
    return payld.decode("UTF-8")


################################################################################
#
#   Program entry-point.
#
def main():
    parser = argparse.ArgumentParser(description="RecogniCV UE4 plugin client")
    parser.add_argument("-s", "--server", help="server to connect to", default="localhost")
    parser.add_argument("-p", "--port", help="port to connect to", default=9000)
    args = parser.parse_args()

    hostport = (args.server, int(args.port))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(hostport)
        print "Connected to server at %s:%d" % hostport
    except socket.error, e:
        print "Unable to connec to server at %s:%d" % hostport
        sys.exit(1)

    while True:
        try:
            sys.stdout.write(": >")
            sys.stdout.flush()

            # Select on any input / output
            read_ready, write_ready, err = select.select([0, s], [], [])
            for i in read_ready:
                if i == 0:
                    data = sys.stdin.readline().strip()
                    if data:
                        send(s, data)
                elif i == s:
                    data = receive(s)
                    if not data:
                        print "Socket closed, client closing ..."
                        return
                    else:
                        sys.stdout.write("RX: " + data + "\n")
                        sys.stdout.flush()

        except KeyboardInterrupt:
            print "Got keyboard interrupt, shutting down ..."
            s.close()
            return

################################################################################

if __name__ == "__main__":
    main()

################################################################################
