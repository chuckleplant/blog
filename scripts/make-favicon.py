from PIL import Image
import argparse
import os

def generate_favicons(image_path, output_dir):
    # Favicon sizes
    sizes = [
        16, 32, 48, 57, 60, 72, 76, 96, 120, 
        144, 152, 180, 192, 196
    ]

    # Open the image using PIL
    with Image.open(image_path) as img:
        # Validate the aspect ratio
        width, height = img.size
        if width != height:
            raise ValueError("Image is not square!")

        # Resize and save in each size
        for size in sizes:
            output_file_path = os.path.join(output_dir, f"favicon-{size}x{size}.png")
            img_resized = img.resize((size, size), Image.ANTIALIAS)
            img_resized.save(output_file_path)
            print(f"Saved to {output_file_path}")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate favicons in multiple sizes from a square image.")
    parser.add_argument("image_path", type=str, help="Path to the square image.")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output directory for favicons relative to where the script is called from. (default: current directory)")
    
    args = parser.parse_args()

    # Convert the output directory to an absolute path based on the current working directory
    output_path = os.path.join(os.getcwd(), args.output)

    # Ensure output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Generate favicons
    generate_favicons(args.image_path, output_path)
