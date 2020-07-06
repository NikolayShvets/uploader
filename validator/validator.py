from werkzeug.datastructures import FileStorage
from logger.logger import Logger
from logger.custom_exceptions import *
from config import *


class Validator:
    @staticmethod
    @Logger.info_log(session=None)
    def get_file_extension(filename):
        return os.path.splitext(filename)[1]

    @staticmethod
    @Logger.info_log(session=None)
    def allowed_file(filename):
        if filename is None or filename == "":
            raise InvalidFileName()

        if not "." in filename:
            raise NonExtensionFile()

        ext = Validator.get_file_extension(filename)

        if ext.upper() in ALLOWED_EXTENSIONS.keys():
            return True
        else:
            raise InvalidFileExtension()

    @staticmethod
    @Logger.info_log(session=None)
    def convert_file_to_df(file: FileStorage):
        if Validator.allowed_file(file.filename):
            try:
                file_bytes = file.stream.read(MAX_FILE_SIZE)
                if len(file_bytes) == MAX_FILE_SIZE:
                    raise FileTooLarge()
                df = ALLOWED_EXTENSIONS[Validator.get_file_extension(file.filename)](file.filename)
                df = df.dropna(how="all").dropna(axis=1, how="all")
                df = df.reset_index(drop=True)
                return df
            except:
                FileReadError()

