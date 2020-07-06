from app import app, Resource, session, namespace
from flask import request, redirect, url_for
from app.validator.validator import Validator
from logger.logger import Logger


@app.route("/upload")
class UploadFileManager(Resource):
    @Logger.info_log(session=session)
    @namespace.response(201, "file was successfully converted")
    def index(self):
        file = request.files("file")
        if Validator.convert_file_to_df(file):
            return redirect(url_for("/")), 201
        return redirect(request.url)
