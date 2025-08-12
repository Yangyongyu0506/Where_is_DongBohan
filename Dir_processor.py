# 此模块用于处理整个目录，找出某种特定的文件格式并返回记录该文件路径的文件

import os
import re
from multiprocessing import Pool
from functools import partial

class DirProcessor:
    __slots__ = ['__root_dir']

    def __init__(self, root_dir: str):
        """
        root_dir: str, the root directory to search for files
        """
        self.__root_dir = root_dir

    def _match_files(self, root, _, filenames, pattern: str, output_file: str):
        with open(output_file, 'a') as output_file:
            for filename in filenames:
                if re.match(pattern, filename):
                    output_file.write(os.path.join(root, filename) + '\n')

    def _match_files_worker(self, pattern: str, output_file: str):
        worker = partial(self._match_files, pattern = pattern, output_file = output_file)
        with Pool(4) as pool:
            _ = pool.starmap_async(worker, os.walk(self.__root_dir))
            _.get()

    def __call__(self, pattern: str, output_file: str = "match_file.txt"):
        """
        pattern: str, the regex pattern to match files
        output_file: str, the file name to write matched file paths
        """
        try:
            os.remove(output_file)
        except:
            pass
        finally:
            pattern_c = re.compile(pattern)
            self._match_files_worker(pattern_c, output_file)

# Example Usage
if __name__ == "__main__":
    dir_processor = DirProcessor("assets/output_faces")
    dir_processor(".*\\.jpg$", "match_file.txt")