import os
import sys
from utils import download_RAVDESS
import logging

logging.basicConfig(filename="runtime.log", \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d-%b-%y %H:%M:%S', \
					level=logging.DEBUG, filemode="a")


if __name__=="__main__":
	RAVDESS_URL = "https://zenodo.org/record/1188976"
	logging.debug("\nCalling from train.py, to retrieve the required urls from {}.".format(RAVDESS_URL))
	urls = download_RAVDESS.RAVDESS_urls(RAVDESS_URL)
	logging.debug("\nRequired urls are retrieved.")
	logging.debug("\nDownloading the files from the urls.")
	download_RAVDESS.download_zip(urls)
	logging.debug("\nFinished Downloading the zipfiles. Moving to unzipping the zipfiles.")
	download_RAVDESS.unzip_audio_files()
	logging.debug("\nFinished unzipping.")
