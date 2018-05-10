from cryptoauthlib import *
import binascii

ATCA_SUCCESS = 0x00

# Defualt ECC608 configuration
CONFIG_608 = bytearray([
    0x01, 0x23, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x04, 0x05, 0x06, 0x07, 0xEE, 0x01, 0x01, 0x00,
    0xC0, 0x00, 0xA1, 0x00, 0xAF, 0x2F, 0xC4, 0x44, 0x87, 0x20, 0xC4, 0xF4, 0x8F, 0x0F, 0x0F, 0x0F,
    0x9F, 0x8F, 0x83, 0x64, 0xC4, 0x44, 0xC4, 0x64, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F,
    0x0F, 0x0F, 0x0F, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
    0x00, 0x00, 0x00, 0x00, 0xFF, 0x84, 0x03, 0xBC, 0x09, 0x69, 0x76, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0x40, 0x00, 0x00, 0x00, 0x00,
    0x33, 0x00, 0x1C, 0x00, 0x13, 0x00, 0x1C, 0x00, 0x3C, 0x00, 0x3E, 0x00, 0x1C, 0x00, 0x33, 0x00,
    0x1C, 0x00, 0x1C, 0x00, 0x38, 0x10, 0x30, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0x32, 0x00, 0x30, 0x00
])

# Slot 4 IO Encryption key
SLOT_4_KEY = bytearray([
    0x37, 0x80, 0xe6, 0x3d, 0x49, 0x68, 0xad, 0xe5,
    0xd8, 0x22, 0xc0, 0x13, 0xfc, 0xc3, 0x23, 0x84,
    0x5d, 0x1b, 0x56, 0x9f, 0xe7, 0x05, 0xb6, 0x00,
    0x06, 0xfe, 0xec, 0x14, 0x5a, 0x0d, 0xb1, 0xe3
])

def main():
    load_cryptoauthlib()
    # Loading cryptoauthlib(python specific)
    atcab_init()
    # Initialize the stack

    info = bytearray(4)
    assert atcab_info(info) == ATCA_SUCCESS
    print("\n Revision number", binascii.hexlify(info))

    serial_number = bytearray(9)
    assert atcab_read_serial_number(serial_number) == ATCA_SUCCESS
    print("\n Serial number", binascii.hexlify(serial_number))

    is_locked = bytearray(1)
    assert atcab_is_locked(0x01, is_locked) == ATCA_SUCCESS

    if (is_locked[0] == True):
        print("\n Data zone locked")
        same_config = bytearray(1)
        assert atcab_cmp_config_zone(CONFIG_608, same_config) == ATCA_SUCCESS

        if (same_config[0] == True):
            print(" Use case configuration detected")
        else:
            print(" Device does not have the required config to run the example")
            quit()
    else:
        print("\n Config zone not locked")
        print(" Loading Use-case configuration")
        # Load test configuration and lock it
        assert atcab_write_config_zone(CONFIG_608) == ATCA_SUCCESS
        # Locking config zone
        assert atcab_lock_config_zone() == ATCA_SUCCESS
        # Locking data zone
        assert atcab_lock_data_zone() == ATCA_SUCCESS
        print(" Use-case Configuration written and locked")

    config_data = bytearray(128)
    assert atcab_read_config_zone(config_data) == ATCA_SUCCESS
    print("\n Current configuration:\n", binascii.hexlify(config_data))

    assert atcab_is_locked(0x00, is_locked) == ATCA_SUCCESS
    print(" Config zone lock status:", is_locked[0])

    assert atcab_is_locked(0x01, is_locked) == ATCA_SUCCESS
    print(" Data zone lock status:", is_locked[0])

    # Writing IO protection key. This key is used to encrypt the PMS which
    # is read out of the device.
    assert atcab_write_zone(2, 4, 0, 0, SLOT_4_KEY, 32) == ATCA_SUCCESS

    tempkey_alice = 0xFFFF
    key_id_bob = 0x02

    # Generating Alice's private key in tempkey and public key from tempkey
    pub_alice = bytearray(64)
    assert atcab_genkey(tempkey_alice, pub_alice) == ATCA_SUCCESS
    print("\n Alice's public key :\n", binascii.hexlify(pub_alice))

    # Generating Bob's Private Key in Slot and getting the associated Public Key
    pub_bob = bytearray(64)
    assert atcab_genkey(key_id_bob, pub_bob) == ATCA_SUCCESS
    print(" Bob's slot {} public key :\n".format(key_id_bob), binascii.hexlify(pub_bob))

    # Generating Alice PMS with bob public key
    pms_alice = bytearray(32)
    assert atcab_ecdh_tempkey(pub_bob, pms_alice) == ATCA_SUCCESS
    print("\n Alice's PMS :\n", binascii.hexlify(pms_alice))

    # Generating Bob PMS with Alice public key
    pms_bob = bytearray(32)
    assert atcab_ecdh_ioenc(key_id_bob, pub_alice, pms_bob, SLOT_4_KEY) == ATCA_SUCCESS
    print(" Bob's PMS :\n", binascii.hexlify(pms_bob))

    assert atcab_release() == ATCA_SUCCESS
main()