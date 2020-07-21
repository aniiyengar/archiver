
import errno
import io
import json
import os
from packaging import version
from pathlib import Path
import time

from config.cfg import cfg
from .mtime import get_mtime

class BaseFile():

    def __init__(self, path: Path):
        self.path = path

        self.file_type: str = self.path.parts[0]
        self.file_name: str = self.path.parts[1]

        self.source_path: Path = Path(cfg.paths.sources).joinpath(self.path)
        self.exp_path: Path = Path(cfg.paths.exp).joinpath(self.path).with_suffix('.json')

        self.data = None
        self.dirty: bool = False
        self._check_dirty()


    def _check_dirty(self):
        if self.data is None:
            self.dirty = True
            return

        if not self.source_path.exists():
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    str(self.source_path))

        if not self.exp_path.exists():
            self.dirty = True
            return

        if get_mtime(self.source_path) > get_mtime(self.exp_path):
            self.dirty = True
            return

        if self.exp_path.exists():
            with self.exp_path.open() as f:
                if version.parse(json.load(f)['version']) < version.parse(cfg.version):
                    self.dirty = True
                    return

        self.dirty = False


    def _save_archive(self):
        type_folder = Path(cfg.paths.exp).joinpath(self.file_type)
        if not type_folder.exists():
            os.mkdir(type_folder)

        with self.exp_path.open('w+') as f:
            json.dump(self.data, f)


    def run_tick(self, force=False):
        self._check_dirty()
        if self.dirty or force:
            with self.source_path.open() as f:
                data = self.compile(f)
                if data:
                    self.data = {
                        'version': cfg.version,
                        'path': str(self.path),
                        'type': self.file_type,
                        'name': self.file_name,
                        'data': data,
                    }
                    self._save_archive()
                    self._check_dirty()


    def get_data(self):
        if self.dirty:
            self.run_tick()
        return self.data


    def compile(self, file: io.FileIO) -> object:
        raise NotImplementedError
