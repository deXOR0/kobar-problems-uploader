from dotenv import load_dotenv
from better_terminal import *
import os
import requests
import json
import shutil

load_dotenv()

UPLOAD_DIR = 'upload_here'
UPLOADED_DIR = 'uploaded'
BASE_URL = os.getenv('BASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

def init():
    print('Looking for upload directory...')
    if os.path.exists(UPLOAD_DIR):
        success('Upload directory found!')
    else:
        warning('Upload directory not found!')
        print('Creating upload directory...')
        os.mkdir(UPLOAD_DIR)
        success('Upload directory created!')
    
    print('Looking for uploaded directory...')
    if os.path.exists(UPLOADED_DIR):
        success('Uploaded directory found!')
    else:
        warning('Uploaded directory not found!')
        print('Creating uploaded directory...')
        os.mkdir(UPLOADED_DIR)
        success('Uploaded directory created!')

def load_files_to_upload():
    global UPLOAD_DIR

    files = os.listdir(UPLOAD_DIR)

    if (file_count := len(files)) >= 1:
        success(f'Found {file_count} file(s) ready to upload')
        return files
    else:
        error('Upload directory is empty. Please make sure to provide at least one file to be uploaded!')
        raise Exception('Upload directory empty exception')

if __name__ == '__main__': 

    init()

    files_to_upload = load_files_to_upload()

    url = f'{BASE_URL}/problems'

    for f in files_to_upload:
        with open(os.path.join(UPLOAD_DIR, f), encoding='utf-8') as _file:
            print(f'Uploading {f}...')
            data = json.load(_file)
            data['secretKey'] = SECRET_KEY
            response = requests.post(url, json = data)
            success('Success!\n')
            success(response.text)
            shutil.move(os.path.join(UPLOAD_DIR, f), os.path.join(UPLOADED_DIR, f))
    
    success('All files have been successfully uploaded')