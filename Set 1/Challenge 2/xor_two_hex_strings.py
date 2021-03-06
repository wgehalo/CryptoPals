import binascii


def xor_hex(a, b):
    if len(a) != len(b):
        print('Inputs must be the same length.')
        return 0

    a_bytes = bytes.fromhex(a)
    b_bytes = bytes.fromhex(b)

    result = bytearray()
    for idx in range(0, len(a_bytes)):
        result.append(a_bytes[idx] ^ b_bytes[idx])
    return result


new_value = xor_hex('1c0111001f010100061a024b53535009181c',
                    '686974207468652062756c6c277320657965')

print(binascii.hexlify(new_value))
