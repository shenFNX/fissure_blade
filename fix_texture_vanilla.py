import zlib
import struct

def write_png(buf, width, height):
    png_sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('!I', width) + struct.pack('!I', height) + b'\x08\x06\x00\x00\x00'
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('!I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('!I', ihdr_crc)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'
        for x in range(width):
            pixel = buf[y * width + x]
            raw_data += struct.pack('BBBB', *pixel)
    idat_data = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + idat_data)
    idat = struct.pack('!I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('!I', idat_crc)
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data)
    iend = struct.pack('!I', len(iend_data)) + b'IEND' + iend_data + struct.pack('!I', iend_crc)
    return png_sig + ihdr + idat + iend

def main():
    width, height = 16, 16
    pixels = [(0, 0, 0, 0)] * (width * height)
    
    # 调色板 - 严格匹配原版质感但换色
    VOID_DARK = (30, 0, 50, 255)    # 边缘
    VOID_MED = (75, 0, 130, 255)     # 剑身主色
    VOID_LIGHT = (130, 50, 200, 255) # 剑身高光
    FISSURE = (0, 255, 255, 255)     # 青色裂缝
    WHITE = (240, 255, 255, 255)     # 裂缝核心
    
    BROWN_DARK = (40, 25, 15, 255)   # 深褐把手
    BROWN_MED = (70, 45, 30, 255)
    
    def p(x, y, color): pixels[y * 16 + x] = color

    # 按照原版钻石剑像素坐标绘制
    # 剑身主轴 (右上)
    for i in range(10):
        x, y = 14-i, 1+i
        p(x, y, VOID_MED)
        p(x+1, y, VOID_DARK)
        p(x, y-1, VOID_DARK)
    
    # 剑刃边缘
    p(15, 0, VOID_DARK); p(14, 0, VOID_DARK); p(15, 1, VOID_DARK)
    
    # 剑身高光 (原版钻石剑亮边位置)
    for i in range(8):
        p(13-i, i+1, VOID_LIGHT)

    # 护手 (Guard) - 钻石剑那个横向结构
    p(4, 11, VOID_DARK); p(5, 11, VOID_MED); p(6, 11, VOID_DARK)
    p(3, 10, VOID_DARK); p(4, 10, VOID_MED); p(5, 10, VOID_MED); p(6, 10, VOID_DARK)
    p(3, 9, VOID_DARK); p(4, 9, VOID_DARK)
    # 另一侧护手
    p(10, 5, VOID_DARK); p(10, 4, VOID_MED); p(10, 3, VOID_DARK)
    p(11, 4, VOID_DARK); p(11, 5, VOID_MED); p(11, 6, VOID_DARK)

    # 把手 (Handle)
    p(0, 15, BROWN_DARK); p(1, 15, BROWN_DARK); p(0, 14, BROWN_DARK)
    p(1, 14, BROWN_MED); p(2, 14, BROWN_DARK)
    p(1, 13, BROWN_DARK); p(2, 13, BROWN_MED); p(3, 13, BROWN_DARK)
    p(2, 12, BROWN_DARK); p(3, 12, BROWN_MED); p(4, 12, BROWN_DARK)

    # 核心：青白色裂缝 (贯穿剑身)
    p(12, 2, WHITE); p(11, 3, FISSURE)
    p(9, 5, WHITE); p(8, 6, FISSURE)
    p(6, 8, WHITE); p(5, 9, FISSURE)

    output_path = r"src\main\resources\assets\fissure_blade\textures\item\fissure_blade.png"
    with open(output_path, 'wb') as f:
        f.write(write_png(pixels, 16, 16))

if __name__ == "__main__":
    main()
