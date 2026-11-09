# DropConvert

**A local-first desktop file conversion application with a modern radial interface.**

DropConvert is a desktop application designed to make file conversion simple and intuitive. Its goal is to bring multiple file conversion capabilities into one interface, allowing users to select files, choose an output format, and save converted files locally.

The project is being developed with Python and PySide6, with a focus on usability, modular architecture, and reliable conversion workflows.

## Project Preview

*Screenshots of the application will be added here.*

## Features

### Currently implemented
- Custom radial-style desktop interface.
- Interactive output format selection.
- File selection and drag-and-drop interaction.
- Image conversion using Pillow.
- PNG and JPG conversion.
- Local output file saving.
- Basic automated conversion testing.

### Planned features
- Support for additional image formats such as WebP, BMP, TIFF, and GIF.
- PDF conversion utilities.
- Word document conversion.
- Excel and CSV conversion.
- PowerPoint document conversion.
- Improved conversion progress and error handling.
- Additional UI animations and visual refinements.

*Planned features will be marked as implemented only after development and testing.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| PySide6 | Desktop graphical interface |
| Pillow | Image processing and conversion |
| pytest | Automated testing |
| Git and GitHub | Version control and collaboration |

## Project Architecture

```text
DropConvert/
│
├── app/
│   └── radial_menu.py
│
├── converters/
│   └── image_converter.py
│
├── tests/
│   └── test_image_converter.py
│
├── assets/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Architecture overview

- **app/** – Contains the desktop interface and radial menu components.
- **converters/** – Contains file conversion logic, separated from the interface.
- **tests/** – Contains automated tests for conversion functionality.
- **assets/** – Reserved for application resources and visual assets.
- **main.py** – Application entry point.
- **requirements.txt** – Python dependencies.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nikhila1910/DropConvert.git
cd DropConvert
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Start DropConvert using:

```bash
python main.py
```

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

## Development Roadmap

- [x] Initial project setup
- [x] Radial interface prototype
- [x] Initial image conversion engine
- [x] Initial image conversion test
- [ ] Expand image format support
- [ ] Implement PDF conversion workflows
- [ ] Implement Word document conversion
- [ ] Implement Excel and CSV conversion
- [ ] Implement PowerPoint conversion
- [ ] Improve application feedback and error handling
- [ ] Add application screenshots
- [ ] Package the application for desktop distribution

## Project Goals

DropConvert aims to become a convenient desktop utility that combines multiple file conversion workflows in a single, easy-to-use application.

The project prioritizes:

- Modular and maintainable code.
- Reliable conversion results.
- Simple user interactions.
- Local file processing.
- Continuous testing and improvement.

## Author

**Nikhila Kallakuntla**

GitHub: [@Nikhila1910](https://github.com/Nikhila1910)

---

*DropConvert is an actively developed personal software engineering project.*