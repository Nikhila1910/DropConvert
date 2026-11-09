
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QLabel,
)

from app.radial_menu import RadialMenu
from converters.image_converter import convert_image


class DropConvertWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DropConvert")
        self.setFixedSize(620, 720)

        self.current_file = None

        # Main radial interface
        self.radial_menu = RadialMenu(self)

        self.radial_menu.file_dropped.connect(
            self.handle_file_drop
        )

        self.radial_menu.format_selected.connect(
            self.handle_format_selection
        )

        # Application title
        self.title = QLabel("DropConvert")

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 27px;
                font-weight: bold;
                background: transparent;
                padding-top: 15px;
            }
        """)

        self.subtitle = QLabel(
            "Drop. Choose. Convert."
        )

        self.subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle.setStyleSheet("""
            QLabel {
                color: #B8D6E8;
                font-size: 12px;
                background: transparent;
            }
        """)

        self.status = QLabel(
            "Drop a PNG or JPG image into the centre circle"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status.setWordWrap(True)

        self.status.setStyleSheet("""
            QLabel {
                color: #C8DDED;
                font-size: 12px;
                background: transparent;
                padding: 10px;
            }
        """)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.radial_menu, 1)
        layout.addWidget(self.status)

        container = QWidget()
        container.setLayout(layout)

        container.setStyleSheet("""
            QWidget {
                background-color: #102D42;
            }
        """)

        self.setCentralWidget(container)

    # Handle file dropped into the centre
    def handle_file_drop(self, file_path):

        file_path = Path(file_path)

        if not file_path.is_file():

            self.current_file = None

            self.status.setText(
                "Please drop a file, not a folder."
            )

            self.radial_menu.current_file = None
            self.radial_menu.update()
            return

        extension = file_path.suffix.lower()

        if extension not in [".png", ".jpg", ".jpeg"]:

            self.current_file = None

            self.status.setText(
                "Currently supported: PNG, JPG and JPEG."
            )

            self.radial_menu.current_file = None
            self.radial_menu.update()
            return

        self.current_file = file_path

        self.status.setText(
            f"Selected: {file_path.name} — "
            "Click a format or drag from the centre to it."
        )

    # Handle selected output format
    def handle_format_selection(self, selected_format):

        if self.current_file is None:
            return

        extension = (
            ".jpg" if selected_format == "JPG" else ".png"
        )

        suggested_name = (
            self.current_file.stem
            + "_converted"
            + extension
        )

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Converted Image",
            str(
                self.current_file.parent / suggested_name
            ),
            "JPEG Image (*.jpg);;PNG Image (*.png)"
        )

        if not output_path:
            return

        output_path = Path(output_path).with_suffix(extension)

        try:

            generated_path = convert_image(
                self.current_file,
                selected_format,
                output_path.parent
            )

            if generated_path != output_path:
                generated_path.replace(output_path)

            self.status.setText(
                f"Successfully converted to {selected_format}: "
                f"{output_path.name}"
            )

            QMessageBox.information(
                self,
                "Conversion Complete",
                f"Your image was converted successfully!\n\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Conversion Failed",
                str(error)
            )


def main():

    app = QApplication(sys.argv)

    window = DropConvertWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
