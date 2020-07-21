
from pathlib import Path
import os

from config.cfg import cfg
from drivers.kindlefile import KindleFile


files = {}


def type_to_class(t: str) -> type:
    if t == 'kindle':
        return KindleFile

    return None


def update_files():
    type_folders = os.listdir(Path(cfg.paths.sources))

    for folder in type_folders:
        if not folder.startswith('.') and Path(cfg.paths.sources).joinpath(folder).is_dir():
            source_paths = os.listdir(Path(cfg.paths.sources).joinpath(folder))
            file_class = type_to_class(folder)

            if file_class:
                if not (folder in files):
                    files[folder] = {}

                for path in source_paths:
                    if not (path in files[folder]):
                        files[folder][path] = file_class(Path(f"{folder}/{path}"))

    for folder in files:
        for path in files[folder]:
            files[folder][path].run_tick(force=True)


if __name__ == '__main__':
    update_files()
