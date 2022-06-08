## Usage
```console
usage: attachments-extractor.py [-h] [-o] eml_files [eml_files ...]

extract attachments from .eml files

positional arguments:
  eml_files       path to .eml file(s)

optional arguments:
  -h, --help      show this help message and exit
  -o, --organize  organize attachments into subfolders based on .eml filename
```
### To use with multiple files
```console
python3 attachments-extractor.py *.eml
```
```console
python3 attachments-extractor.py msg1.eml msg2.eml msg3.eml
```
The script will create a directory named ```attachments``` in the current working directory containing the extracted attachments.
## Requirements
- Python 3.6 or later
