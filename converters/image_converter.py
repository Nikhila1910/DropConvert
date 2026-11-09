
from pathlib import Path
from PIL import Image


def convert_image(input_path, output_format, output_folder):
    """
    Convert a PNG or JPG image into another image format.
    """

    input_path = Path(input_path)
    output_folder = Path(output_folder)

    # Check whether the input file exists
    if not input_path.is_file():
        raise FileNotFoundError("The selected image does not exist.")

    # Allow only PNG and JPG output
    output_format = output_format.upper()

    if output_format not in ["PNG", "JPG"]:
        raise ValueError("Unsupported output format.")

    # Open the image
    with Image.open(input_path) as image:

        # Convert JPG to RGB because JPG doesn't support transparency
        if output_format == "JPG":
            if image.mode in ("RGBA", "LA") or "transparency" in image.info:
                image = image.convert("RGBA")
                background = Image.new("RGB", image.size, "white")
                background.paste(image, mask=image.getchannel("A"))
                image = background
            else:
                image = image.convert("RGB")

        # Create the output filename
        extension = ".jpg" if output_format == "JPG" else ".png"
        output_path = output_folder / f"{input_path.stem}_converted{extension}"

        # Save the converted image
        pillow_format = "JPEG" if output_format == "JPG" else "PNG"
        image.save(output_path, format=pillow_format)

    return output_path
