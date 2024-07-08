"""Host API required Work Files tool"""
import os
import nuke
import shutil
### Starts Alkemy-X Override ###
# Add custom autosave logic to work with rolling autosaves
import glob
import time
### Ends Alkemy-X Override ###
from .utils import is_headless


def file_extensions():
    return [".nk"]


def has_unsaved_changes():
    return nuke.root().modified()


def save_file(filepath):
    path = filepath.replace("\\", "/")
    nuke.scriptSaveAs(path, overwrite=1)
    nuke.Root()["name"].setValue(path)
    nuke.Root()["project_directory"].setValue(os.path.dirname(path))
    nuke.Root().setModified(False)

### Starts Alkemy-X Override ###
# Add custom autosave logic to work with rolling autosaves
def getAutoSaveFiles(filename):
    date_file_list = []
    files = glob.glob(filename + '[1-9]')
    files.extend( glob.glob(filename) )

    for file in files:
        # retrieves the stats for the current file as a tuple
        # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
        # the tuple element mtime at index 8 is the last-modified-date
        stats = os.stat(file)
        # create tuple (year yyyy, month(1-12), day(1-31), hour(0-23), minute(0-59), second(0-59),
        # weekday(0-6, 0 is monday), Julian day(1-366), daylight flag(-1,0 or 1)) from seconds since epoch
        # note:  this tuple can be sorted properly by date and time
        lastmod_date = time.localtime(stats[8])
        # create list of tuples ready for sorting by date
        date_file_tuple = lastmod_date, file
        date_file_list.append(date_file_tuple)

    date_file_list.sort()
    return [ filename for _, filename in date_file_list ]
### Ends Alkemy-X Override ###


def open_file(filepath):

    def read_script(nuke_script):
        nuke.scriptClear()
        ### Starts Alkemy-X Override ###
        try:
            nuke.scriptReadFile(nuke_script)
        except RuntimeError as e:
            nuke.tprint("AYON Error: There was an error loading script:")
            nuke.tprint(str(e))
            pass
        ### Ends Alkemy-X Override ###
        nuke.Root()["name"].setValue(nuke_script)
        nuke.Root()["project_directory"].setValue(os.path.dirname(nuke_script))
        nuke.Root().setModified(False)

    filepath = filepath.replace("\\", "/")

    # To remain in the same window, we have to clear the script and read
    # in the contents of the workfile.
    # Nuke Preferences can be read after the script is read.
    read_script(filepath)
    
    ### Starts Alkemy-X Override ###
    # Comment out as we believe we are getting weird things with autosaves
    # overwriting files so we want to reduce that being possible
    # if not is_headless():
    #     autosave = nuke.toNode("preferences")["AutoSaveName"].evaluate()
    #     autosave_files = getAutoSaveFiles(autosave)
    #     autosave_prmpt = "Autosave detected.\n" \
    #                      "Would you like to load the autosave file?"  # noqa
    #     if autosave_files and os.path.isfile(autosave_files[-1]):
    #         lastmod_date = time.ctime(os.path.getmtime(filepath))
    #         autosave_date = time.ctime(os.path.getmtime(autosave))
    #         if autosave_date > lastmod_date and nuke.ask(autosave_prmpt):
    #             try:
    #                 # Overwrite the filepath with autosave
    #                 # shutil.copy(autosave, filepath)
    #                 # Now read the (auto-saved) script again
    #                 read_script(autosave)
    #             except shutil.Error as err:
    #                 nuke.message(
    #                     "Detected autosave file could not be used.\n{}"

    #                     .format(err))
    ### Ends Alkemy-X Override ###

    return True


def current_file():
    current_file = nuke.root().name()

    # Unsaved current file
    if current_file == 'Root':
        return None

    return os.path.normpath(current_file).replace("\\", "/")


def work_root(session):

    work_dir = session["AYON_WORKDIR"]
    scene_dir = session.get("AVALON_SCENEDIR")
    if scene_dir:
        path = os.path.join(work_dir, scene_dir)
    else:
        path = work_dir

    return os.path.normpath(path).replace("\\", "/")
