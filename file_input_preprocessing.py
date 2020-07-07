from werkzeug.datastructures import FileStorage
from allowed_extension import *
import os
import openpyxl


class InputValidator:
    def __init__(self, fs: FileStorage):
        """

        :param fs:
        """
        self.target_file = fs
        self.file_bytes = self.target_file.stream.read(MAX_FILE_SIZE)
        if len(self.file_bytes) == MAX_FILE_SIZE:
            raise ValueError("File is too large!")

    def get_file_extension(self) -> str:
        """

        :return:
        """
        return os.path.splitext(self.target_file.filename)[1]

    def allowed_file(self) -> bool:
        """

        :return:
        """
        if self.target_file.filename is None or self.target_file.filename == "":
            return False
        if not "." in self.target_file.filename:
            raise False
        ext = self.get_file_extension()
        return True if ext.upper() in ALLOWED_EXTENSIONS.keys() else False

    def is_password_protected(self) -> bool:
        """

        :return:
        """
        wb = openpyxl.load_workbook(filename=self.target_file.filename)
        return False if wb.security.lockStructure is None else True

    def convert_file_to_df(self) -> pd.DataFrame:
        """

        :return:
        """
        if isinstance(self.target_file, FileStorage):
            if self.allowed_file():
                if not self.is_password_protected():
                    ext = self.get_file_extension().upper()
                    df = ALLOWED_EXTENSIONS[ext](self.target_file.filename)
                    df.dropna(axis="index", how="all", inplace=True).\
                        dropna(axis="columns", how="all", inplace=True)\
                        .reset_index(inplace=True)
                    return df
                else:
                    raise RuntimeError("Uploading file is password protected!")
        else:
            return pd.DataFrame({})
