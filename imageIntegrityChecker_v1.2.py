import os
import rawpy
from PIL import Image
import logging
from datetime import datetime
import sys

def setup_logging():
    logger = logging.getLogger()        
    logger.setLevel(logging.DEBUG)

    # Get the current datetime and for the timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("%d-%m-%y_%H:%M:%S")

    info_handler = logging.FileHandler(f'logs/cr2_info_{timestamp}.log')
    info_handler.setLevel(logging.INFO)
    error_handler = logging.FileHandler(f'logs/cr2_error_{timestamp}.log')
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)


def check_image_headers(file_path):
    try:
        with Image.open(file_path) as img:
            print(f"[5] Format: {img.format} | Mode: {img.mode} | Size: {img.size}")
            logging.info(f"[5] Format: {img.format} | Mode: {img.mode} | Size: {img.size}")
            return True

    except IOError:
        print(f"[5] Image Cannot be Open: {file_path}")
        logging.info(f"[5] Image Cannot be Open: {file_path}")
        return False

def check_cr2_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            print(f"[1] File Location: {filepath}")
            logging.info(f"[1] File Location: {filepath}")


            if filename.lower().endswith(('.cr2', '.arw', '.raf', '.srw')):
                print(f"[2] Loading the RAW File: {filename}")
                logging.info(f"[2] Loading the RAW File: {filename}")

                try:
                    with rawpy.imread(filepath) as raw:
                        print(f"[3] File is Readable: {filename}")
                        logging.info(f"[3] File is Readable: {filename}")

                except (IOError, EOFError) as e:
                    print(f"[3] File is Corrupted or Unreadable: {filename}")  
                    logging.info(f"[3] File is Corrupted or Unreadable: {filename}")
                except rawpy._rawpy.LibRawFileUnsupportedError as e:
                    print(f"[3] File Format is Unsupported or not a RAW File: {filename}")    
                    logging.info(f"[3] File Format is Unsupported or not a RAW File: {filename}")
                except Exception as e:
                    print(f"[3] Unexpected error with raw File: {filename}")
                    logging.info(f"[3] Unexpected error with raw File: {filename}")
                


            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.psd', '.cr2', '.pdf')):
                print(f"[4] Loading the Image: {filename}")
                logging.info(f"[4] Loading the Image: {filename}")

                try:
                    if check_image_headers(filepath):
                        print("[6] Header/Footer Check Passed")
                        logging.info("[6] Header/Footer Check Passed")
                    else:
                        print("[6] Header/Footer Check Failed or File Cannot be Opened")
                        logging.error("[6] Header/Footer Check Failed or File Cannot be Opened")

                except Exception as e:
                    print(f"[6] Exception while checking image: {e}")
                    logging.error(f"[6] Exception while checking image: {e}")


# Initialize logging
setup_logging()

# directory = '/xxx/xxxx/xxxxx/'
# check_cr2_files(directory)

message   =  "***  File Validator Script  ***"
print(message)
print("")
print("")
print("Example format for Windows Machine:      E:\Search\wetransfer\corruptions")
print("Example format for Linux\ MAC Machines:  /home/xxx/wetransfer/corruptions")
print("")
directory =  input("Enter the Directory Path: ")
check_cr2_files(directory)

sys.exit(0)
