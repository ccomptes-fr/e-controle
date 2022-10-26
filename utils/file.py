import datetime
import glob
import os
import pathlib
import shutil

from django.conf import settings


def get_last_file_metadata_in_control_folder(reference_code):
    """
    In a control folder (reference_code), get number of files, last file dt by modification time and last file name
    if the control folder has no file, return the modification time of control folder as dt and control path
    """
    if reference_code and reference_code.strip():
        control_dir_path = os.path.join(settings.MEDIA_ROOT, reference_code)

        if os.path.exists(control_dir_path):
            files = glob.glob(control_dir_path + "/**/*.*", recursive=True)
            nb_files = len(files)
            if nb_files > 0:
                latest_file = max(files, key=os.path.getmtime)
                latest_file_path = pathlib.Path(latest_file)
                last_modification_ts = latest_file_path.stat().st_mtime
                return nb_files, datetime.datetime.fromtimestamp(last_modification_ts), latest_file_path
            else:
                # no file, return control folder modification date
                return nb_files, datetime.datetime.fromtimestamp(pathlib.Path(control_dir_path).stat().st_mtime), control_dir_path


def delete_control_folder(reference_code):
    """
    Delete a control folder (reference_code)

    :param reference_code: control directory.
    """
    if reference_code and reference_code.strip():
        control_dir_path = os.path.join(settings.MEDIA_ROOT, reference_code)

        if os.path.exists(control_dir_path):
            shutil.rmtree(control_dir_path)
