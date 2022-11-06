#!/bin/env python3

# Assume the length of the key is 6 (we don't know the key)
key = "A" * 6 
cmd = "myname=SEEDManual&uid=1001&lstcmd=1" 
message = key + ":" + cmd

padding_size = 64 - int(len(message) % 64)
if padding_size <= 8:
    padding_size += 64
padding = bytearray(0x00 for i in range(padding_size))
padding[0:1] = b'\x80'
padding[-8:] = (len(message)*8).to_bytes(8,byteorder='big')

# URL encode the padding (put a "%" in front each hex number)
padding_URL_encoded = ''
for i in range(padding_size):
    padding_URL_encoded += "%" + '{:02x}'.format(padding[i])
print(message + padding_URL_encoded)


