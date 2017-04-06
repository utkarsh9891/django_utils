import mimetypes
import os
from io import BytesIO
from wsgiref.util import FileWrapper

import requests
from django.http import HttpResponse

from common.utils.file_ops import FileOperations as FOps
from common.utils.exception import ExceptionLogger

__all__ = ['HttpOperations']


class HttpOperations:
    """
    Custom operations to be performed to for downloading or uploading files
    """

    # temp file download path -- /tmp/temp_download/<filename>
    temp_file_download_path_format = '/tmp/temp_download/{}'

    @classmethod
    def downloadable_file(cls, file_path, download_name):
        """
        Create a HttpResponse object of the local file for downloading
        :param file_path: the target file to be downloaded
        :param download_name: the filename with which the target file will be downloaded
        :return: the HttpResponse object of the file if success else None
        """
        try:
            wrapper = FileWrapper(open(file_path, 'rb'))
            content_type = mimetypes.guess_type(file_path)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(file_path)
            response['Content-Disposition'] = "attachment; filename={}".format(download_name)
        except:
            ExceptionLogger.print_exception()
            return None

        return response

    @classmethod
    def retrieve_image(cls, url):
        """
        fetch an image from the url specified
        :param url: the url of the image to be retrieved
        :return: the StringIO object of the image
        """
        try:
            response = requests.get(url)
            image = None
            if response.status_code == 200:
                image = BytesIO(response.content)
        except:
            ExceptionLogger.print_exception()
            return None

        return image

    @classmethod
    def download_to_temp(cls, file_url, download_name):
        """
        Download files locally to temp directory & return the downloaded file path
        :param file_url: the url from which to retrieve the file
        :param download_name: the name with which to save the file
        :return: the path of the downloaded file
        """
        try:
            file_path = cls.temp_file_download_path_format.format(download_name)
            FOps.remove_file(file_path)
            FOps.create_parent_directory(file_path)
            file_resp = requests.get(file_url)
            with open(file_path, 'wb') as file_obj:
                file_obj.write(file_resp.content)

            return file_path
        except:
            ExceptionLogger.print_exception()
            return None
