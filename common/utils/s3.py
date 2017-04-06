from ssl import CertificateError
from urllib.request import urlretrieve

import boto
from boto.s3.key import Key
from django.conf import settings

__all__ = ['S3Operations']


class S3Operations:
    """
    The operations that are to be performed on the s3 storage
    """
    bucket_name = settings.BUCKET_NAME
    access_key_id = settings.AWS_ACCESS_KEY_ID
    secret_access_key = settings.AWS_SECRET_ACCESS_KEY

    # Public urls will be of the format https://seller.payments.s3.amazonaws.com/DUMMY/Dummy_POD_Image.png
    public_url_format = 'https://{}.s3.amazonaws.com/{}'

    @classmethod
    def get_s3_conn(cls, access_key_id=None, secret_access_key=None, **kwargs):
        """
        Ge the s3 connection object
        :param access_key_id: access key id to use. default is the key id specified in settings
        :param secret_access_key: secret key for the access key id. default is the secret key specified in settings
        :return: the s3 connection object
        """
        access_key_id = access_key_id or cls.access_key_id
        secret_access_key = secret_access_key or cls.secret_access_key
        return boto.connect_s3(access_key_id, secret_access_key, **kwargs)

    @classmethod
    def get_s3_bucket(cls, bucket_name=None, **kwargs):
        """
        Get the s3 bucket for the specified params
        :param bucket_name: the bucket name. default is the bucket name defined in settings
        :return: the bucket object
        """
        bucket_name = bucket_name or cls.bucket_name

        conn = cls.get_s3_conn(**kwargs)
        try:
            bucket = conn.get_bucket(bucket_name)
        except CertificateError:
            conn = cls.get_s3_conn(is_secure=False, **kwargs)
            bucket = conn.get_bucket(bucket_name)

        return bucket

    @classmethod
    def push_via_file_path(cls, file_path, filename, s3_dir, mode='public', **kwargs):
        """
        push a local file to s3
        :param file_path: the local path of the file
        :param filename: the name of the file stored locally
        :param s3_dir: the s3 directory to which the file is to be pushed
        :param mode: the mode of file storage public/private
        :return: the s3 key and url of the file
        """
        try:
            bucket = cls.get_s3_bucket(**kwargs)

            key_obj = Key(bucket)
            key_obj.key = "{}/{}".format(s3_dir, filename)
            key_obj.set_contents_from_filename(file_path)

            if mode == 'public':
                key_obj.make_public()
                url = key_obj.generate_url(expires_in=0, query_auth=False)
            else:
                url = cls.generate_private_url(key_name=key_obj.key, **kwargs)

            return key_obj.key, url
        except Exception as e:
            print("error pushing file to s3 : {}".format(e))
            return None, None

    @classmethod
    def push_via_file_object(cls, file_obj, filename, s3_dir, mode='private', **kwargs):
        """
        push file object to s3 directory
        :param file_obj: the StringIO like file object to be pushed to s3
        :param filename: the name to store the object with
        :param s3_dir: the s3 directory to puch the object to
        :param mode: private or public url to be generated
        :return: the s3 key and the url generated for the file
        """
        try:
            # point to the beginning of the file
            file_obj.seek(0)

            bucket = cls.get_s3_bucket(**kwargs)

            key_obj = Key(bucket)
            key_obj.key = "{}/{}".format(s3_dir, filename)
            key_obj.set_contents_from_file(file_obj)

            if mode == 'public':
                key_obj.make_public()
                url = key_obj.generate_url(expires_in=0, query_auth=False)
            else:
                url = cls.generate_private_url(key_name=key_obj.key, **kwargs)

            return key_obj.key, url
        except Exception as e:
            print("error pushing file object to s3 : {}".format(e))
            return None, None

    @classmethod
    def generate_public_url(cls, key_name, bucket_name=None):
        """
        generate a public s3 url for the specified s3 key
        :param key_name: the target s3 key
        :param bucket_name: the bucket name. default is the bucket name defined in settings
        :return: the public url for the s3 key
        """
        bucket_name = bucket_name or cls.bucket_name
        return cls.public_url_format.format(bucket_name, key_name)

    @classmethod
    def generate_private_url(cls, key_name, **kwargs):
        """
        generate a private s3 url for the specified s3 key
        :param key_name: the target s3 key
        :return: the private url for the s3 key
        """
        if key_name is None or key_name == '':
            return None

        conn = cls.get_s3_conn(**kwargs)

        try:
            key_url = conn.generate_url(604800, 'GET', cls.bucket_name, key_name)
        except CertificateError:
            conn = cls.get_s3_conn(is_secure=False, **kwargs)
            key_url = conn.generate_url(604800, 'GET', cls.bucket_name, key_name)

        return key_url

    @classmethod
    def fetch_file(cls, key_name, file_path, key_type='public', **kwargs):
        """
        fetch file from s3 & save to local storage
        :param key_name: the key to be fetched from s3
        :param file_path: the local path to store the file
        :param key_type: whether the key is a 'public' key or 'private' key
        :return: True if successfully downloaded else False
        """
        try:
            if key_type == 'public':
                url = cls.generate_public_url(key_name)
            else:
                url = cls.generate_private_url(key_name, **kwargs)

            urlretrieve(url, file_path)
        except Exception as e:
            print("error downloading s3 key {} to {} : {}".format(key_name, file_path, e))
            return False
        return True
