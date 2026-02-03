import zlib
import struct
import os

def write_png(buf, width, height):
    # Signature
    png_sig = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    ihdr_data = struct.pack('!I', width) + struct.pack('!I', height) + b'\x08\x06\x00\x00\x00'
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('!I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('!I', ihdr_crc)
    
    # IDAT
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
    
    # Palette
    # Outline (Dark Void)
    O = (20, 0, 40, 255) 
    # Blade Base (Void Purple)
    B = (70, 0, 110, 255)
    # Blade Highlight (Lighter Purple)
    L = (110, 20, 160, 255)
    # Crack/Core (Cyan/White)
    C = (0, 255, 255, 255)
    W = (220, 255, 255, 255)
    # Handle (Wood)
    H = (101, 67, 33, 255)
    # Guard (Dark Metal)
    G = (50, 50, 60, 255)

    # 16x16 Grid logic (Top-Left is 0,0)
    # Mimicking a classic sword shape diagonal
    
    # Handle
    pixels[15 * 16 + 1] = H
    pixels[14 * 16 + 2] = H
    pixels[13 * 16 + 3] = H
    
    # Guard (Cross)
    pixels[12 * 16 + 4] = G
    pixels[13 * 16 + 3] = G # Overlap handle slightly for depth
    pixels[11 * 16 + 5] = G
    pixels[13 * 16 + 2] = G
    pixels[10 * 16 + 5] = G
    
    # Blade Outline (The sword edge)
    # Left side
    pixels[11 * 16 + 4] = O
    pixels[10 * 16 + 4] = O
    pixels[9 * 16 + 5] = O
    pixels[8 * 16 + 6] = O
    pixels[7 * 16 + 7] = O
    pixels[6 * 16 + 8] = O
    pixels[5 * 16 + 9] = O
    pixels[4 * 16 + 10] = O
    pixels[3 * 16 + 11] = O
    
    # Right side
    pixels[12 * 16 + 5] = O
    pixels[11 * 16 + 6] = O
    pixels[10 * 16 + 7] = O
    pixels[9 * 16 + 8] = O
    pixels[8 * 16 + 9] = O
    pixels[7 * 16 + 10] = O
    pixels[6 * 16 + 11] = O
    pixels[5 * 16 + 12] = O
    pixels[4 * 16 + 13] = O
    
    # Tip
    pixels[2 * 16 + 12] = O
    pixels[1 * 16 + 13] = O
    pixels[0 * 16 + 14] = O
    pixels[0 * 16 + 15] = O
    pixels[1 * 16 + 15] = O # Tip shadow
    
    # Blade Inner (The color)
    # Main body
    pixels[10 * 16 + 5] = B
    pixels[9 * 16 + 6] = B
    pixels[8 * 16 + 7] = B
    pixels[7 * 16 + 8] = B
    pixels[6 * 16 + 9] = B
    pixels[5 * 16 + 10] = B
    pixels[4 * 16 + 11] = B
    pixels[3 * 16 + 12] = B
    
    pixels[10 * 16 + 6] = L
    pixels[9 * 16 + 7] = L
    pixels[8 * 16 + 8] = L
    pixels[7 * 16 + 9] = L
    pixels[6 * 16 + 10] = L
    pixels[5 * 16 + 11] = L
    pixels[4 * 16 + 12] = L
    pixels[3 * 16 + 13] = L
    
    # The Fissure (Crack) - replacing some inner pixels
    pixels[9 * 16 + 6] = C
    pixels[8 * 16 + 7] = W
    pixels[7 * 16 + 8] = C
    pixels[5 * 16 + 10] = C
    pixels[4 * 16 + 11] = W
    pixels[2 * 16 + 13] = C # Near tip

    output_path = r"src\main\resources\assets\fissure_blade\textures\item\fissure_blade.png"
    with open(output_path, 'wb') as f:
        f.write(write_png(pixels, width, height))
    print(f"Texture regenerated at {output_path}")

if __name__ == "__main__":
    main()
