import inspect
import os
import shutil

__all__ = ['FileOperations']


class FileOperations:
    """
    Cleanup operations to be performed, primarily for tmp directory
    Bare minimum assertions is implemented to ensure that the params are of the expected data type
    """

    @classmethod
    def assert_type(cls, item_name, item, expected=str):
        """
        Raises an assertion error if the data type does not match.
        This error message is not handled inside this class & therefore would be propagated to the calling scope
        :param item_name: the name of the target data item
        :param item: the actual data item
        :param expected: the expected data type; by default this is str
        :return: assertion error if failed
        """
        caller = inspect.stack()[1][3]
        assert type(item) is expected, '{} received {} as {}:{}'.format(caller, item_name, type(item), str(item))

    @classmethod
    def remove_directory(cls, directory):
        """
        remove directory if it exists
        :param directory: the directory to check
        :return: deletion response True/False
        """
        cls.assert_type('directory', directory)
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        except Exception as e:
            print('Error deleting directory {} : {}'.format(directory, e))
            return False
        return True

    @classmethod
    def create_directory(cls, directory):
        """
        Creates the target directory if it does not exist
        :param directory: the target directory path
        :return: Creation status True/False
        """
        cls.assert_type('directory', directory)
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print('Error creating directory {} : {}'.format(directory, e))
            return False
        return True

    @classmethod
    def recreate_directory(cls, directory):
        """
        Recreates the target directory -- deletes if exists & creates again
        :param directory: the target directory path
        :return: recreation status True/False
        """
        cls.assert_type('directory', directory)
        try:
            cls.remove_directory(directory)
            os.makedirs(directory)
        except Exception as e:
            print('Error recreating directory {} : {}'.format(directory, e))
            return False
        return True

    @classmethod
    def remove_file(cls, path):
        """
        Deletes the target file if it exists
        :param path: path to file to be removed
        :return: deletion station True/False
        """
        cls.assert_type('path', path)
        try:
            if os.path.exists(path) and os.path.isfile(path):
                os.remove(path)
        except Exception as e:
            print('Error deleting file {} : {}'.format(path, e))
            return False
        return True

    @classmethod
    def make_zip(cls, source, destination, filename):
        """
        Zips a directory to a file
        :param source: the source directory to be zipped
        :param destination: the location to store the zip file at
        :param filename: the name with the file is to be stored (do not add .zip to the name)
        :return: the path of the zip file if created else None
        """
        cls.assert_type('source', source)
        cls.assert_type('destination', destination)
        cls.assert_type('filename', filename)
        try:
            base_name = os.path.join(destination, filename)
            cls.remove_file(base_name + '.zip')
            cls.create_directory(source)
            cls.create_directory(destination)
            shutil.make_archive(base_name=base_name, format='zip', root_dir=source)
            zip_path = '{}.zip'.format(base_name)
        except Exception as e:
            print('Error creating zip {}.zip of {} at {} : {}'.format(filename, source, destination, e))
            return None
        return zip_path

    @classmethod
    def create_parent_directory(cls, path):
        cls.assert_type('path', path)
        try:
            parent_directory = os.path.dirname(path)
            if not os.path.exists(parent_directory):
                cls.create_directory(parent_directory)
        except Exception as e:
            print('Error creating parent directory of {} : {}'.format(path, e))
            return False
        return True
