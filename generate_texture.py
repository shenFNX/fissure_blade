from PIL import Image, ImageDraw
import os

def create_fissure_blade_texture():
    # 16x16 image, RGBA mode
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    pixels = img.load()

    # Colors
    void_purple = (75, 0, 130, 255)  # Deep Indigo/Purple
    void_dark = (48, 25, 52, 255)    # Darker purple
    crack_cyan = (0, 255, 255, 255)  # Bright Cyan
    crack_white = (240, 255, 255, 255) # Azure/White
    handle_brown = (101, 67, 33, 255) # Dark Brown
    handle_highlight = (139, 69, 19, 255) # Saddle Brown

    # Draw Handle (Bottom Left)
    # Simple diagonal handle
    for i in range(5):
        pixels[i+2, i+2] = handle_brown
        if i > 0 and i < 4:
             pixels[i+2, i+3] = handle_highlight
    
    # Draw Guard (Crossguard area)
    pixels[6, 6] = void_dark
    pixels[5, 7] = void_dark
    pixels[7, 5] = void_dark

    # Draw Blade (Extending to Top Right)
    for i in range(7, 14):
        # Blade body
        pixels[i, i] = crack_cyan # The core crack
        pixels[i-1, i] = void_purple
        pixels[i, i-1] = void_purple
        pixels[i-1, i-1] = void_dark
        pixels[i+1, i+1] = void_purple # Outline/Edge
        
        # Add some variation/thickness
        if i < 13:
             pixels[i+1, i] = void_purple
             pixels[i, i+1] = void_purple

    # Refine the crack (make it jagged/glowing)
    pixels[8, 8] = crack_white
    pixels[10, 10] = crack_white
    pixels[12, 12] = crack_white
    
    # Tip
    pixels[14, 14] = void_purple
    pixels[15, 15] = void_dark

    # Save
    output_path = r"E:\Mymods\src\main\resources\assets\fissure_blade\textures\item\fissure_blade.png"
    img.save(output_path)
    print(f"Texture saved to {output_path}")

if __name__ == "__main__":
    try:
        create_fissure_blade_texture()
    except Exception as e:
        print(f"Error: {e}")
