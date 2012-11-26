def main():
    test = [32, 1, 4, 1, 1, 65, 1, 2, 84, 104, 105, 
             115, 32, 105, 115, 32, 97, 32, 115, 116, 
             114, 105, 110, 103, 32, 102, 111, 114, 32, 
             67, 79, 77, 70, 46]
    badtest = "BADDATA" * 10
    print decode_tleaf_cell(test)
    try:
        print decode_tleaf_cell([ord(i) for i in badtest])
    except Exception:
        print "Bad t-leaf cell."


def decode_tleaf_cell(bl):
    def pop_vstack(vbl):
        """Pops off a varint off the stack and 
        returns a tuple of the value and the 
        remainder."""
        value, vlen = decode_varint(vbl)
        return (value, vbl[vlen:])

    def pop_vstack_rec(st, vbl):
        type_table = {}
        type_table[0] = lambda b: (None, vbl)
        type_table[1] = lambda b: (twos_comp(b[0], 8), vbl[1:])
        type_table[2] = lambda b: (twos_compl(b[:2], 16), vbl[2:])
        type_table[3] = lambda b: (twos_compl(b[:3], 24), vbl[3:])
        type_table[4] = lambda b: (twos_compl(b[:4], 32), vbl[4:])
        type_table[5] = lambda b: (twos_compl(b[:6], 48), vbl[6:])        
        type_table[6] = lambda b: (twos_compl(b[:8], 64), vbl[8:])
        type_table[7] = None # Will throw error. Not implemented.
        type_table[8] = lambda b: (0, vbl)
        type_table[9] = lambda b: (1, vbl)
        type_table[10] = None
        type_table[11] = None

        if st < 12:
            return type_table[st](vbl)
        elif st % 2 == 0:
            pass # handle blob
        else:
            str_len = (st-13)/2
            return ("".join(map(chr, vbl[:str_len])), vbl[str_len:])
        
    
    payload_len, bl = pop_vstack(bl)
    rowid, bl = pop_vstack(bl)
    overflow_page_no = bl[payload_len:] or None

    pstack = bl[:payload_len]
    payload_hdr_len, pstack = pop_vstack(pstack)
    payload_hdr_st = []
    for i in range(payload_hdr_len-1):
        res, pstack = pop_vstack(pstack)
        payload_hdr_st.append(res)

    cell = {'payload_len': payload_len, 
            'rowid': rowid,
            'payload_hdr_len': payload_hdr_len,
            'payload_hdr_st': payload_hdr_st,
            'payload': []
            }
    for i in payload_hdr_st:
        res, pstack = pop_vstack_rec(i, pstack)
        cell['payload'].append((res, i))

    return cell

def twos_comp(val, bits):
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val

def twos_compl(bl, bits):
    total = 0
    for i in range(len(bl)):
        total += bl[::-1][i] << (i*8)
    return twos_comp(total, bits)

def decode_varint(bl):

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
