import zlib
import struct
import os

def write_png(buf, width, height):
    # PNG Signature
    png_sig = b'\x89PNG\r\n\x1a\n'
    
    # IHDR Chunk
    # Width, Height, Bit depth (8), Color Type (6=Truecolor with Alpha), Compression (0), Filter (0), Interlace (0)
    ihdr_data = struct.pack('!I', width) + struct.pack('!I', height) + b'\x08\x06\x00\x00\x00'
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('!I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('!I', ihdr_crc)
    
    # IDAT Chunk
    # Filter type 0 (None) for each scanline
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00' # Filter type 0
        for x in range(width):
            pixel = buf[y * width + x]
            raw_data += struct.pack('BBBB', *pixel)
            
    idat_data = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + idat_data)
    idat = struct.pack('!I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('!I', idat_crc)
    
    # IEND Chunk
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data)
    iend = struct.pack('!I', len(iend_data)) + b'IEND' + iend_data + struct.pack('!I', iend_crc)
    
    return png_sig + ihdr + idat + iend

def main():
    width, height = 16, 16
    # Initialize with full transparency
    pixels = [(0, 0, 0, 0)] * (width * height)
    
    # Helper to set pixel at x,y (0,0 is top-left)
    def p(x, y, r, g, b, a=255):
        if 0 <= x < width and 0 <= y < height:
            pixels[y * width + x] = (r, g, b, a)

    # Colors
    OUTLINE = (35, 0, 55)      # Dark Void Purple
    BLADE = (100, 20, 160)     # Vivid Purple
    HIGHLIGHT = (140, 60, 200) # Light Purple
    CRACK_CYAN = (0, 255, 255) # Cyan
    CRACK_WHITE = (220, 255, 255) # White-ish Cyan
    HANDLE_DARK = (60, 40, 20) # Dark Brown
    HANDLE_LIGHT = (100, 70, 40) # Light Brown
    GUARD = (50, 40, 60)       # Dark Metal

    # --- DRAWING THE SWORD ---
    
    # 1. Handle (Bottom-Left)
    p(1, 14, *HANDLE_DARK); p(2, 13, *HANDLE_DARK); p(3, 12, *HANDLE_DARK)
    p(2, 14, *HANDLE_LIGHT); p(3, 13, *HANDLE_LIGHT)
    
    # 2. Guard (Crossguard)
    p(2, 11, *GUARD); p(3, 11, *GUARD); p(4, 11, *GUARD)
    p(3, 10, *GUARD); p(4, 10, *GUARD); p(5, 10, *GUARD); p(6, 10, *GUARD)
    p(4, 9, *GUARD); p(5, 9, *GUARD)
    # Lower guard bit
    p(1, 12, *GUARD) 
    
    # 3. Blade Outline
    # Right edge
    for i in range(9): p(5+i, 8-i, *OUTLINE)
    # Left edge
    for i in range(8): p(4+i, 7-i, *OUTLINE)
    # Tip
    p(13, 0, *OUTLINE); p(14, 0, *OUTLINE); p(14, 1, *OUTLINE); p(13, 1, *OUTLINE)

    # 4. Blade Body (Purple)
    for i in range(7):
        p(5+i, 7-i, *BLADE)
        p(6+i, 7-i, *BLADE) # Thicker part
        p(5+i, 6-i, *HIGHLIGHT) # Highlight edge

    # 5. The Fissure (Crack) - Cyan/White pixels cutting through the blade
    p(6, 8, *CRACK_CYAN)
    p(7, 7, *CRACK_WHITE)
    p(8, 6, *CRACK_CYAN)
    p(10, 4, *CRACK_WHITE)
    p(11, 3, *CRACK_CYAN)
    
    # Write to file
    target_path = r"src\main\resources\assets\fissure_blade\textures\item\fissure_blade.png"
    # Ensure directory exists
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    with open(target_path, 'wb') as f:
        f.write(write_png(pixels, width, height))
    print(f"Generated 16x16 transparent texture at: {target_path}")

if __name__ == "__main__":
    main()
