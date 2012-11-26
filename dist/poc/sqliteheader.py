def main():
    dump_header("testdb")

def dump_header(filename):
    data = file(filename, 'rb').read()
    header = data[:100]
    
    header_lt = [(0, 16, 'Header string'),
                 (16, 2, 'Database page size'),
                 (18, 1, 'File format write version'),
                 (19, 1, 'File format read version'),
                 (20, 1, 'Reserved space'),
                 (21, 1, 'Maximum embedded payload fraction'),
                 (22, 1, 'Minimum embedded payload fraction'),
                 (23, 1, 'Leaf payload fraction'),
                 (24, 4, 'File change counter'),
                 (28, 4, 'In-header database size'),
                 (32, 4, 'Page number of first freelist trunk page'),
                 (36, 4, 'Total number of freelist pages'),
                 (40, 4, 'Schema cookie'),
                 (44, 4, 'Schema format number'),
                 (48, 4, 'Default page cache size'),
                 (52, 4, 'Page number of largest root b-tree'),
                 (56, 4, 'Database text encoding'),
                 (60, 4, 'User version'),
                 (64, 4, 'Incremental-vacuum mode'),
                 (68, 24, 'Reserved for expansion'),
                 (92, 4, 'Version-valid-for number'),
                 (96, 4, 'SQLite version number')]

    print "Parsing header from SQLite file: %s." % filename
    for i in header_lt:
        rep = ""
        c = 0
        for j in header[i[0]:i[0]+i[1]]:
            if c == 4:
                rep += "\n" + " " * 42
                c = 0
            c += 1
            rep += "0x%02x " % ord(j)
        if i[0] == 0:
            rep = "%s\n%s(%s)" % (rep, " "*42, header[i[0]:i[0]+i[1]])
        print "%40s: %s" % (i[2], rep)
    

                 

if __name__ == "__main__":
    main()
