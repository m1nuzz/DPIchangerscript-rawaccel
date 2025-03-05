# RawAccel DPI Changer

## Description
A simple Flask-based web application to change DPI settings in RawAccel's settings.json file with an easy-to-use web interface.

## Prerequisites
- Python 3.7 or higher
- Windows OS (due to firewall configuration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/m1nuzz/DPIchangerscript-rawaccel
```

2. Run the Start Script
Simply double-click `start.bat` or run it from the command line. This script will:
- Create a virtual environment
- Update pip
- Install required dependencies
- Start the Flask application

## How to Use

1. First Launch:
   - When you first run the application, you'll be prompted to enter the path to your RawAccel folder (e.g., `C:\rawaccel`)
   - The path will be saved for future use

2. Changing DPI:
   - After setting the RawAccel folder path, you can enter a new DPI value
   - The application will automatically update the `settings.json` file and run `writer.exe`

3. Changing RawAccel Folder:
   - Click on "Change RawAccel Folder" to reset and specify a new path

## Features
- Simple web interface
- Automatic RawAccel settings modification
- Firewall rule for local server access

## Notes
- Requires internet access during first setup to install dependencies
- Web interface runs on `http://localhost:5000`
- Tested on Windows

## Troubleshooting
- Ensure you have Python 3.7+ installed
- Check that the RawAccel folder path is correct
- Verify that `settings.json` and `writer.exe` exist in the specified folder

## License
This project is open-source. Check the repository for specific license details.
