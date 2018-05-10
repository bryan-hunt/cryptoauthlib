from cryptoauthlib import *
import binascii

ATCA_SUCCESS = 0x00

def get_info():

    # Initialize the library
    assert atcab_init() == ATCA_SUCCESS

    # Request the Revision Number
    info = bytearray(4)
    assert atcab_info(info) == ATCA_SUCCESS
    print("\n Revision number", binascii.hexlify(info))

    # Request the Serial Number
    serial_number = bytearray(9)
    assert atcab_read_serial_number(serial_number) == ATCA_SUCCESS
    print("\n Serial number", binascii.hexlify(serial_number))

    # Free the library
    atcab_release()
    
if __name__ == '__main__':
    get_info()