import os


ASSIST = bool(os.getenv("NUKEASSIST"))

# List of extensions for all video media formats, not image sequences
VIDEO_FILE_EXTENSIONS = [".avi", ".mov", ".m4v", ".mp4", ".m4a", ".m4p", ".m4b", ".m4r", ".mpg", ".mpeg", ".mxf", ".r3d"]
LOADER_CATEGORY_COLORS = {
    "latest": "0x4ecd25ff",
    "outdated": "0xd84f20ff",
    "invalid": "0xff0000ff",
    "not_found": "0xffff00ff",
}
