#!/usr/bin/env python3

from signal import signal, SIGINT
from email import message_from_binary_file, policy
from glob import glob
from argparse import ArgumentParser
from os import makedirs, path
from re import sub
from base64 import b64decode
from quopri import decodestring

def signal_handler(signal, frame):
    exit()

def sanitize_filename(filename):
    illegal_chars = r'[/\\|\[\]\{\}:<>+=;,?!*"~#$%&@\']'
    return sub(illegal_chars, '_', filename)

# extract .eml from email
def get_attached_email(attachment):
    cte = attachment["Content-Transfer-Encoding"]
    data = attachment.get_content().as_string()
    if cte == "base64":
        data = b64decode(data).decode()
    elif cte == "quoted-printable":
        data = decodestring(data).decode()
    return bytes(data, encoding="utf-8")

def save_attachment(save_location, attachment):
    data = attachment.get_payload(decode=True) if not attachment.get_content_type() == "message/rfc822" else get_attached_email(attachment)
    filename = sanitize_filename(attachment.get_filename())
    makedirs(save_location, exist_ok=True)
    with open(f"{save_location}/{filename}", "wb") as f:
        f.write(data)

def get_attachments(msg):
    if msg.is_multipart():
        return [item for item in msg.iter_attachments()]
    elif msg.is_attachment() or msg.get_content_disposition() == "inline":
        return [msg]

def get_eml_files(eml_files_args):
    eml_files = []
    for arg in eml_files_args:
        eml_files.extend(glob(arg))
    return eml_files

def parse_arguments():
    parser = ArgumentParser(description="extract attachments from .eml files")
    parser.add_argument("eml_files", type=str, nargs="+", help="path to .eml file(s)")
    parser.add_argument("-o", "--organize", action="store_true", dest="organize", help="organize attachments into subfolders based on .eml filename")
    return parser.parse_args()

def main():
    signal(SIGINT, signal_handler)
    args = parse_arguments()
    eml_files = get_eml_files(args.eml_files)
    for eml_file in eml_files:
        with open(eml_file, "rb") as f:
            msg = message_from_binary_file(f, policy=policy.default)
        attachments = get_attachments(msg)
        if attachments:
            try:
                save_location = "attachments" if not args.organize else f"attachments/{path.basename(eml_file).split('.')[0]}"
                for attachment in attachments:
                    save_attachment(save_location, attachment)
                print(f"{len(attachments)} ATTACHMENT(S): {path.basename(eml_file)}")
            except:
                print(f"ERROR: {path.basename(eml_file)}")
        else:
            print(f"NO ATTACHMENTS: {path.basename(eml_file)}")

if __name__ == "__main__":
    main()
