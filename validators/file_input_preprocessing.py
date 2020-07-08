from werkzeug.datastructures import FileStorage
from .config import *
from .dataframe_cleaner import Cleaner
import os
from datetime import datetime
import openpyxl
from app.logger.logger import Logger


class InputValidator(Cleaner):
    @Logger.info_log(session=None)
    def __init__(self, fs: FileStorage) -> None:
        """
        Конструктор
        :param fs:
        """
        self.target_file = fs
        self.local_file_name = ""

    @Logger.info_log(session=None)
    def save_file(self) -> None:
        """
        Собриает локальное имя файла и путь до него. По полученному пути сохраняет файл.
        :return:
        """

        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ext = self._get_file_extension()

        # Вычислим хэш чтобы обеспечить уникальность имен сохраняемых файлов
        file_hash = hash(self.target_file.filename + dt)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        self.local_file_name = f"{UPLOAD_FOLDER}/{file_hash}{ext}"
        self.target_file.save(self.local_file_name, MAX_FILE_SIZE)

    @Logger.info_log(session=None)
    def _get_file_extension(self) -> str:
        """
        Возвращет расширение файла (.xlsx, .csv, ...)
        :return:
        """
        return os.path.splitext(self.target_file.filename)[1]

    @Logger.info_log(session=None)
    def allowed_file(self) -> bool:
        """
        Определяет, является ли имя файла допустимым.
        :return: True или Exception
        """

        if self.target_file.filename is None or self.target_file.filename == "":
            raise ValueError("File name is empty!")

        if not "." in self.target_file.filename:
            raise ValueError("File extension is missing!")

        ext = self._get_file_extension()
        if ext.upper() in ALLOWED_EXTENSIONS.keys():
            return True
        else:
            raise ValueError("File is not allowed!")

    @Logger.info_log(session=None)
    def _is_password_protected(self) -> bool:
        """
        Проверяет наличие пароля у excel файла
        :return:
        """

        try:
            wb = openpyxl.load_workbook(filename=self.local_file_name)
            return False if wb.security.lockStructure is None else True
        except:
            raise RuntimeError

    @Logger.info_log(session=None)
    def convert_file_to_df(self) -> pd.DataFrame:
        """

        :return:
        """
        if self.allowed_file():
            if not self._is_password_protected():
                ext = self._get_file_extension().upper()
                df = ALLOWED_EXTENSIONS[ext](self.local_file_name)
                df = self.drop_duplicate_cols_by_name(df)
                df = self.drop_duplicate_rows(df)
                df = self.drop_unnamed_columns(df)
                df = self.drop_thrash_columns(df, trash_content)
                return df
            else:
                raise RuntimeError

class OututValidator():
    # TODO: конвертурует датафрейм в определенный формат файла в соответсвтии с переданным флагом
    # проверить что дф, что не нан, проверит что не пустой, проверить размер

    def __init__(self, df: pd.DataFrame):
        pass
