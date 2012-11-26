def main():
    vals = [[0x2B], 
            [0x8C, 0xA0, 0x6F], 
            [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
             0xFF, 0xFF, 0xFF, 0xFF, 0x01],
            [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
             0xFF, 0xFD, 0xCD, 0x56],
            [68, 1, 6, 23, 21],
            [1, 6, 23, 21]]

    print "Signed test:"
    for i in vals:
        res = decode_varint(i)
        print "%s: %d (%d bytes)" % (", ".join(map(hex, i)), res[0], res[1])

def decode_varint(bl):
    def twos_comp(val, bits):
        if( (val&(1<<(bits-1))) != 0 ):
            val = val - (1<<bits)
        return val

    bit_set = 0
    mask = 0
    no_of_bytes = 0
    for i in range(9):
        no_of_bytes += 1
        if i != 8:
            to_add = (bl[i] & 0b01111111)
            bit_set = (bit_set << 7) + to_add
            if not bl[i] & (1 << 7):
                break
        else:
            bit_set = bl[i] + (bit_set << 8)

    return (twos_comp(bit_set, 64), no_of_bytes)
            

if __name__ == "__main__":
    main()
