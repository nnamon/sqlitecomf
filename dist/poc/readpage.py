PAGE_SIZE = 1024

import pprint

def main():
    data = file("testdb").read()
    no_of_pages = len(data)/PAGE_SIZE
    pages = []
    for i in range(1, no_of_pages+1):
        pages.append(data[PAGE_SIZE*(i-1):PAGE_SIZE*i])
    for i in pages:
        print "Dumping page: "
        print read_page([ord(j) for j in i]) 

def read_page(bl):
    # Create page dictionary
    page = {}

    # Set the page header offset
    fst_pgb = "SQLite format 3\x00" == "".join(map(chr, bl[:16]))
    phos = (100 if fst_pgb else 0)

    # Read header
    pg_hdr = parse_page_header(bl[phos:phos+8])
    pg_hdr['offset'] = phos
    page['hdr'] = pg_hdr

    # Read cell pointer array
    previous_cell = PAGE_SIZE
    ca_begin = phos + 8
    ca_end = phos + 8 + (phos+8+pg_hdr['number_of_cells']*2)
    cell_array = bl[ca_begin: ca_end]
    p_cell = []
    for i in range(0, pg_hdr['number_of_cells']*2, 2):
        current_offset = tbl(cell_array[i:i+2])
        cell_size = previous_cell-current_offset
        p_cell.append((current_offset, cell_size))
        previous_cell = current_offset
    
    page['cptr_array'] = p_cell

    # Read cells
    cells = []
    for i in p_cell:
        offset, length = i
        cells.append(bl[offset:offset+length])
    page['cells'] = cells
    
    # Return the page dictionary
    return page
    
def parse_page_header(bl):
    if len(bl) != 8:
        return None
    pg_hdr = {}
    pg_hdr['type'] = bl[0]
    pg_hdr['first_freeblock_offset'] = tbl(bl[1:3])
    pg_hdr['number_of_cells'] = tbl(bl[3:5])

    c_off = tbl(bl[5:7])
    pg_hdr['cells_offset'] = (65536 if not c_off else c_off)
    pg_hdr['number_of_freebytes'] = bl[7]
    return pg_hdr
    
def tbl(bl):
    total = 0
    for i in range(len(bl)):
        total += bl[::-1][i] << (i*8)
    return total
                                 

if __name__ == "__main__":
    main()
