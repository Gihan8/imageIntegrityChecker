import os
import rawpy
from PIL import Image
import logging


def setup_logging():
    logger = logging.getLogger()        
    logger.setLevel(logging.DEBUG)

    info_handler = logging.FileHandler('logs/cr2_info.log')
    info_handler.setLevel(logging.INFO)
    error_handler = logging.FileHandler('logs/cr2_error.log')
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)


def check_image_headers(directory):
    try:
        with Image.open(directory) as img:
            print(f"File Location: {directory}")
            print(f"Format: {img.format} | Mode: {img.mode} | Size: {img.size}")
            logging.info(f"File Location: {directory}")
            logging.info(f"Format: {img.format} | Mode: {img.mode} | Size: {img.size}")
            return True
  
    except IOError:
           print(f"File Cannot be Open: {directory}")
           logging.error(f"File Cannot be Open: {directory}")
           return False


def check_cr2_files(directory):
    """
    Check All CR2 files in the given directory for corruption.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        logging.error(f"Directory not found: {directory}")
        return

    for filename in os.listdir(directory):

        # rawpy supported extensions
        if filename.lower().endswith(('.cr2', '.arw', '.raf', '.srw')):
            filepath = os.path.join(directory, filename)
            try:
                with rawpy.imread(filepath):
                    print(f"File is Readable: {filename}")
                    logging.info(f"File is Readable: {filename}")

            except (IOError, EOFError) as e:
                print(f"File is Corrupted or Unreadable: {filename}")
                logging.error(f"File is Corrupted or Unreadable: {filename} - {e}")
            except rawpy._rawpy.LibRawFileUnsupportedError as e:
                print(f"File Format is Unsupported or not a RAW File: {filename}")
                logging.error(f"File Format is Unsupported or not a RAW File: {filename} - {e}")
            except Exception as e:
                print(f"Unexpected error with File: {filename}")
                logging.error(f"Unexpected error with File: {filename}: - {e}")
                

        # PIL import image supported extensions
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.psd', '.cr2', '.pdf')):
            file_path = os.path.join(directory, filename)
            try:
                if check_image_headers(file_path):
                    print("Header/Footer Check Passed")
                    logging.info("Header/Footer Passed")
                else:
                    print("Header/Footer Check Failed or File Cannot be Opened")
                    logging.error("Header/Footer Check Failed or File Cannot be Opened")

            except Exception as e:
                print(f"Unexpected error with File: {filename}: - {e}")
                logging.error(f"Unexpected error with File: {filename}: - {e}")


# Initialize logging
setup_logging()

# Replace '/path/to/your/directory' with the path to the directory containing your CR2 files
## check_cr2_files('/home/max/wetransfer/corruptions')
message   =  "***  File Validator Script  ***"
print(message)
print("")
print("")
print("Example format for Windows Machine:      E:\Search\wetransfer\corruptions")
print("Example format for Linux\ MAC Machines:  /home/max/wetransfer/corruptions")
print("")
directory =  input("Enter the Directory Path: ")
check_cr2_files(directory)

