import struct
import zlib
import base64

def write_png(buf, width, height):
    # Reverse the vertical line order
    width_byte_4 = width * 4
    raw_data = b''.join(b'\x00' + buf[span:span + width_byte_4]
                        for span in range((height - 1) * width_byte_4, -1, - width_byte_4))

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (struct.pack("!I", len(data)) +
                chunk_head +
                struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

    return b"".join([
        b"\x89PNG\r\n\x1a\n",
        png_pack(b"IHDR", struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b"IDAT", zlib.compress(raw_data, 9)),
        png_pack(b"IEND", b"")
    ])

# Generate 192x192 Blue/Black icon
width, height = 192, 192
buffer = bytearray(width * height * 4)
for y in range(height):
    for x in range(width):
        idx = (y * width + x) * 4
        # simple border
        if x < 10 or x > width-10 or y < 10 or y > height-10:
             buffer[idx:idx+4] = b'\x3b\x82\xf6\xff' # Blue
        else:
             buffer[idx:idx+4] = b'\x0f\x17\x2a\xff' # Dark
with open('icon-192.png', 'wb') as f:
    f.write(write_png(buffer, width, height))

# Generate 512x512
width, height = 512, 512
buffer = bytearray(width * height * 4)
for y in range(height):
    for x in range(width):
        idx = (y * width + x) * 4
        if x < 20 or x > width-20 or y < 20 or y > height-20:
             buffer[idx:idx+4] = b'\x3b\x82\xf6\xff' # Blue
        else:
             buffer[idx:idx+4] = b'\x0f\x17\x2a\xff' # Dark
with open('icon-512.png', 'wb') as f:
    f.write(write_png(buffer, width, height))
