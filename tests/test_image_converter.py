
from PIL import Image

from converters.image_converter import convert_image


def test_png_to_jpg(tmp_path):

    # Create a sample PNG image
    input_file = tmp_path / "sample.png"
    output_folder = tmp_path

    image = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    image.save(input_file)

    # Convert PNG to JPG
    output_file = convert_image(
        input_file,
        "JPG",
        output_folder
    )

    # Check that the output exists
    assert output_file.exists()
    assert output_file.suffix == ".jpg"

    # Check that the output is actually a JPEG image
    with Image.open(output_file) as converted:
        assert converted.format == "JPEG"
