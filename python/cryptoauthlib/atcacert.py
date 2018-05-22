from ctypes import Structure, c_int, c_uint8, c_uint16, c_char, POINTER
from .atcab import get_cryptoauthlib


class atcacert_device_loc_t(Structure):
    _fields_ = [
        ('zone', c_int),  # Zone in the device.
        ('slot', c_uint8),  # Slot within the data zone. Only applies if zone is DEVZONE_DATA.
        ('is_genkey', c_uint8),  # If true, use GenKey command to get the contents instead of Read.
        ('offset', c_uint16),  # Byte offset in the zone.
        ('count', c_uint16)  # Byte count.
    ]


class atcacert_cert_loc_t(Structure):
    _fields_ = [('offset', c_uint16), ('count', c_uint16)]


class atcacert_cert_element_t(Structure):
    _fields_ = [
        ('id', c_char * 16),  # ID identifying this element.
        ('device_loc', atcacert_device_loc_t),  # Location in the device for the element.
        ('cert_loc', atcacert_cert_loc_t)  # Location in the certificate template for the element.
    ]


class atcacert_def_t(Structure):
    _fields_ = [
        ('type', c_int),  # Certificate type.
        ('template_id', c_uint8),       # ID for the this certificate definition (4-bit value).
        ('chain_id', c_uint8),          # ID for the certificate chain this definition is a part of (4-bit value).
        ('private_key_slot', c_uint8),   #If this is a device certificate template, this is the device slot for the device private key.
        ('sn_source', c_int),  # Where the certificate serial number comes from (4-bit value).
        ('cert_sn_dev_loc', atcacert_device_loc_t), # Only applies when sn_source is SNSRC_STORED or SNSRC_STORED_DYNAMIC. Describes where to get the certificate serial number on the device.
        ('issue_date_format', c_int),  # Format of the issue date in the certificate.
        ('expire_date_format', c_int),  # format of the expire date in the certificate.
        ('tbs_cert_loc', atcacert_cert_loc_t),  # Location in the certificate for the TBS (to be signed) portion.
        ('expire_years', c_uint8),  # Number of years the certificate is valid for (5-bit value). 0 means no expiration.
        ('public_key_dev_loc', atcacert_device_loc_t),  # Where on the device the public key can be found.
        ('comp_cert_dev_loc', atcacert_device_loc_t),  #Where on the device the compressed cert can be found.
        ('std_cert_elements', atcacert_cert_loc_t * 8),  # Where in the certificate template the standard cert elements are inserted.
        ('cert_elements', POINTER(atcacert_cert_element_t)),  # Additional certificate elements outside of the standard certificate contents.
        ('cert_elements_count', c_uint8),  # Number of additional certificate elements in cert_elements.
        ('cert_template', POINTER(c_uint8)),  #Pointer to the actual certificate template data.
        ('cert_template_size', c_uint16)  # Size of the certificate template in cert_template in bytes.
    ]

