import math
import struct
from multiprocessing import Process
from datetime import datetime

import config
from Logger import Logger
from MongoSession import MongoSession

DATA_PACKET_SIZE = config.DATA_PACKET_SIZE

class Session:
    def __init__(self, _eventQueue = None):
        self.dataBuffer = bytearray()
        self.deviceId, self.first, self.databaseSession = None, True, None
        Logger.logWriter.debug(f'Initialize a new session, not yet catch the deviceId')

    def get_packets_from_buffer(self):
        '''
            test packet is consist of 22 bytes.
            [device id][acc_x][acc_y][acc_z][time stamp]
        '''
        records = []

        dataPacketLength = math.trunc(len(self.dataBuffer) / DATA_PACKET_SIZE)
        Logger.logWriter.debug(f'Receive packets[{dataPacketLength}]')

        print( f'Rawdata: {self.dataBuffer}')
        for dataIndex in range(dataPacketLength):
            rawPacket = self.dataBuffer[dataIndex * DATA_PACKET_SIZE: (dataIndex + 1) * DATA_PACKET_SIZE]
            rawPacket = struct.unpack('>ccfffq', rawPacket)
            print( f'\tUnpack a packet: {rawPacket}')

            packet = {
                'dev_id' : rawPacket[0].decode('utf-8') + rawPacket[1].decode('utf-8'),
                'acc' : [ float("{0:.10f}".format(rawPacket[2])),
                          float("{0:.10f}".format(rawPacket[3])),
                          float("{0:.10f}".format(rawPacket[4]))],
                'ts' : rawPacket[5]
            }
            print(f'\t\t-> {packet}')
            records.append(packet)

        self.dataBuffer = self.dataBuffer[dataPacketLength * DATA_PACKET_SIZE:]

        Logger.logWriter.debug(str(records) + '\n')
        return records

    def proc(self, _recvData):
        self.dataBuffer.extend( _recvData)
        packets = self.get_packets_from_buffer()

        if self.first:
            self.first, self.deviceId = False, packets[0]['dev_id']
            self.databaseSession = MongoSession( packets[0]['dev_id'])
            Logger.logWriter.info(f'Set the session[{self.deviceId}]')

        try:
            result = self.databaseSession.add_data_in_collection( packets)
        except :
            # put appropirate error handling in here...
            pass

    def teardown(self):
        self.databaseSession.close()
        Logger.logWriter.info(f'Close session[{self.deviceId}]')