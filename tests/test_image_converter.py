
from PIL import Image
import pytest

from converters.image_converter import convert_image


def test_png_to_jpg(tmp_path):
    input_file = tmp_path / "sample.png"
    image = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    image.save(input_file)

    output_file = convert_image(input_file, "JPG", tmp_path)

    assert output_file.exists()
    assert output_file.suffix == ".jpg"

    with Image.open(output_file) as converted:
        assert converted.format == "JPEG"
        assert converted.size == (100, 100)


def test_jpg_to_png(tmp_path):
    input_file = tmp_path / "sample.jpg"
    image = Image.new("RGB", (100, 100), (0, 255, 0))
    image.save(input_file)

    output_file = convert_image(input_file, "PNG", tmp_path)

    assert output_file.exists()
    assert output_file.suffix == ".png"

    with Image.open(output_file) as converted:
        assert converted.format == "PNG"
        assert converted.size == (100, 100)


def test_unsupported_format(tmp_path):
    input_file = tmp_path / "sample.png"
    Image.new("RGB", (50, 50)).save(input_file)

    with pytest.raises(ValueError, match="Unsupported output format"):
        convert_image(input_file, "PDF", tmp_path)


def test_missing_input_file(tmp_path):
    input_file = tmp_path / "missing.png"

    with pytest.raises(FileNotFoundError):
        convert_image(input_file, "JPG", tmp_path)


def test_output_is_a_valid_image(tmp_path):
    input_file = tmp_path / "sample.png"
    Image.new("RGB", (80, 60), (0, 0, 255)).save(input_file)

    output_file = convert_image(input_file, "JPG", tmp_path)

    with Image.open(output_file) as converted:
        converted.verify()
