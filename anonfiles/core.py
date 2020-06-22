from .api import *
from filehandling import join_path, abs_main_dir, file_size
from omnitools import randstr
import time
import os
import subprocess


__ALL__ = ["basefiles", "anonfiles", "bayfiles", "forumfiles"]


class basefiles(object):
    def __init__(self, item: str, db: str, big_item_split_parts: int = -1,
                 split: bool = False, split_size: int = 1024*1024*4000,
                 host: str = None, mirror: bool = False,
                 _7z_exe: str = r"C:\Program Files\7-Zip\7z.exe",
                 temp_dir: str = None,
                 token_anonfiles: str = "", token_bayfiles: str = "") -> None:
        self.instance = "["+type(self).__name__+"] "
        self.urls = []
        if not temp_dir:
            temp_dir = os.environ["TEMP"]
        if not os.path.isabs(db):
            db = join_path(abs_main_dir(2), db)
        if not os.path.isabs(item):
            item = join_path(abs_main_dir(2), item)
        p(self.instance+f"<started> {item}")
        files = self.check_size(item, big_item_split_parts, split, split_size, _7z_exe, temp_dir)
        self.upload(files, db, host, mirror, token_anonfiles, token_bayfiles)
        p(self.instance+f"<ended> {item}")

    def check_size(self, item: str, big_item_split_parts: int,
                   split: bool, split_size: int,
                   _7z_exe: str,
                   temp_dir: str) -> list:
        if os.path.isfile(item) and not split:
            files = [item]
        else:
            basename = os.path.basename(item)+".zip"
            temp = randstr(2 ** 3)+"_"+str(int(time.time()))
            dest = join_path(temp_dir, temp, basename)
            fs = file_size(item)
            if big_item_split_parts > 1:
                if fs >= (big_item_split_parts-1)**2+1:
                    import math
                    split_size = math.ceil(fs/big_item_split_parts)
                else:
                    raise Exception(f"{item} is too small ({fs}B) to split into {big_item_split_parts} parts")
            cmd = [_7z_exe, "a", "-tzip", f"-v{split_size}b", "-mx=0", dest, item]
            if os.path.isdir(item):
                cmd.append("-r")
            p(self.instance+f"<zipping> {item}", cmd)
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            process.communicate()
            files = [join_path(temp_dir, temp, file) for file in os.listdir(join_path(temp_dir, temp))]
            p(self.instance+f"<zipped> {item} has {len(files)} parts", files)
        return files

    def upload(self, files: list, db: str, host: str, mirror: bool, token_anonfiles: str, token_bayfiles: str):
        for file in files:
            if not mirror:
                try:
                    self.urls.append(globals()[host](db=db, token=token_anonfiles).upload(filename=file))
                except Exception as e:
                    p(self.instance+f"<upload> {file} failed to upload", e)
            else:
                try:
                    self.urls.append(AnonFiles(db=db, token=token_anonfiles).upload(filename=file))
                except Exception as e:
                    p(self.instance+f"<upload> {file} failed to upload", e)
                try:
                    self.urls.append(BayFiles(db=db, token=token_bayfiles).upload(filename=file))
                except Exception as e:
                    p(self.instance+f"<upload> {file} failed to upload", e)
                try:
                    self.urls.append(ForumFiles(db=db).upload(filename=file))
                except Exception as e:
                    p(self.instance+f"<upload> {file} failed to upload", e)


class anonfiles(basefiles):
    def __init__(self, item: str, db: str, big_item_split_parts: int = -1,
                 split: bool = False, split_size: int = 1024*1024*4000,
                 _7z_exe: str = r"C:\Program Files\7-Zip\7z.exe",
                 temp_dir: str = None,
                 token: str = "") -> None:
        host = "AnonFiles"
        mirror = False
        super().__init__(
            item, db, big_item_split_parts,
            split, split_size,
            host, mirror, _7z_exe,
            temp_dir,
            token_anonfiles=token
        )


class bayfiles(basefiles):
    def __init__(self, item: str, db: str, big_item_split_parts: int = -1,
                 split: bool = False, split_size: int = 1024*1024*4000,
                 _7z_exe: str = r"C:\Program Files\7-Zip\7z.exe",
                 temp_dir: str = None,
                 token: str = "") -> None:
        host = "BayFiles"
        mirror = False
        super().__init__(
            item, db, big_item_split_parts,
            split, split_size,
            host, mirror, _7z_exe,
            temp_dir,
            token_bayfiles=token
        )


class forumfiles(basefiles):
    def __init__(self, item: str, db: str, big_item_split_parts: int = -1,
                 split: bool = False, split_size: int = 1024*1024*4000,
                 _7z_exe: str = r"C:\Program Files\7-Zip\7z.exe",
                 temp_dir: str = None) -> None:
        host = "ForumFiles"
        mirror = False
        super().__init__(
            item, db, big_item_split_parts,
            split, split_size,
            host, mirror, _7z_exe,
            temp_dir
        )

