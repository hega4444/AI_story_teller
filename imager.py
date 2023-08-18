from bing_image_downloader import downloader
from PIL import Image
import os
import sys

class ImageDownload():

    def __init__(self, search) -> None:

        #this class searches for an image and download to local disk
        #deactivate the standar stdout
        sys.stdout = open(os.devnull, "w")  # deactivate log in stdout
        downloader.download(search, limit=1,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
        # Restore the original stdout
        sys.stdout = sys.__stdout__

        #Find and retrieve the file name:

        # Specify the folder path
        folder_path = 'dataset/' + search + '/'

        # Get a list of all files in the folder
        file_list = os.listdir(folder_path)

        # Get the name of the most recently created or modified file
        most_recent_file = file_list[0]
        
        self._path = "dataset/" + search + '/' + most_recent_file
    
    @property
    def path(self):
        return self._path


if __name__ == '__main__':
    img = ImageDownload('star trek q')

    image = Image.open(img.path)
    image.show()