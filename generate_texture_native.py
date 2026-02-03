import zlib
import struct
import os

def write_png(buf, width, height):
    # Reverse the rows to match PNG top-to-bottom if needed, but my logic is usually top-left origin.
    # buf is a list of (r,g,b,a) tuples
    
    # Signature
    png_sig = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    # Width, Height, Bit depth (8), Color Type (6=RGBA), Compression (0), Filter (0), Interlace (0)
    ihdr_data = struct.pack('!I', width) + struct.pack('!I', height) + b'\x08\x06\x00\x00\x00'
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('!I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('!I', ihdr_crc)
    
    # IDAT
    # Filter type 0 (None) for each scanline
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00' # Filter byte
        for x in range(width):
            pixel = buf[y * width + x]
            raw_data += struct.pack('BBBB', *pixel)
            
    idat_data = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + idat_data)
    idat = struct.pack('!I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('!I', idat_crc)
    
    # IEND
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data)
    iend = struct.pack('!I', len(iend_data)) + b'IEND' + iend_data + struct.pack('!I', iend_crc)
    
    return png_sig + ihdr + idat + iend

def main():
    width, height = 16, 16
    pixels = [(0, 0, 0, 0)] * (width * height)
    
    # Colors
    void_purple = (75, 0, 130, 255)
    void_light = (138, 43, 226, 255)
    crack_cyan = (0, 255, 255, 255)
    crack_white = (240, 255, 255, 255)
    handle_brown = (101, 67, 33, 255)
    
    # Draw (x,y) from top-left (0,0)
    def p(x, y, color):
        if 0 <= x < width and 0 <= y < height:
            pixels[y * width + x] = color
            
    # Handle (Bottom Left)
    p(2, 13, handle_brown)
    p(3, 12, handle_brown)
    p(4, 11, handle_brown)
    
    # Guard
    p(5, 10, void_purple)
    p(4, 10, void_purple)
    p(6, 11, void_purple)
    
    # Blade (Diagonal up-right)
    for i in range(0, 8):
        base_x, base_y = 6 + i, 9 - i
        # Core crack
        p(base_x, base_y, crack_white if i % 3 == 0 else crack_cyan)
        # Blade edges
        p(base_x - 1, base_y, void_purple)
        p(base_x, base_y + 1, void_purple)
        # Blade body
        p(base_x + 1, base_y, void_light)
        p(base_x, base_y - 1, void_light)

    output_path = r"src\main\resources\assets\fissure_blade\textures\item\fissure_blade.png"
    with open(output_path, 'wb') as f:
        f.write(write_png(pixels, width, height))
    print(f"Texture generated at {output_path}")

if __name__ == "__main__":
    main()
