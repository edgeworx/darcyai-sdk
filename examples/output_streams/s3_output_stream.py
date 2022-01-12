import boto3

from darcyai_engine.output.output_stream import OutputStream
from darcyai_engine.utils import validate_not_none, validate_type


class S3Stream(OutputStream):
    """
    A stream that writes data to a AWS S3 bucket.

    """
    def __init__(self,
                 bucket:str,
                 aws_access_key_id:str,
                 aws_secret_access_key:str,
                 aws_region:str):
        super().__init__()

        validate_not_none(bucket, "bucket is required")
        validate_type(bucket, str, "bucket must be a string")

        validate_not_none(aws_access_key_id, "aws_access_key_id is required")
        validate_type(aws_access_key_id, str, "aws_access_key_id must be a string")

        validate_not_none(aws_secret_access_key, "aws_secret_access_key is required")
        validate_type(aws_secret_access_key, str, "aws_secret_access_key must be a string")

        validate_not_none(aws_region, "aws_region is required")
        validate_type(aws_region, str, "aws_region must be a string")

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

        s3 = session.resource('s3')
        self.__bucket = s3.Bucket(bucket)


    def write(self, data:tuple) -> None:
        """
        Writes data to the stream.

        Arguments:
            data (tuple[str, Any]) -- A tuple of the form (key, data)
                where key is the key to write to and data is the data to write.

        Returns:
            None
        """
        if data is None:
            return

        validate_type(data, tuple, "data must be a tuple")
        validate_type(data[0], str, "data[0] must be a string")

        key = data[0]
        value = data[1]
        self.__bucket.put_object(Key=key, Body=value)


    def close(self) -> None:
        """
        Closes the output stream.

        Arguments:
            None

        Returns:
            None
        """
        pass
