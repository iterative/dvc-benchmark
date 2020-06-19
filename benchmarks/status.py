import os
import shutil

from benchmarks.base import BaseBench, random_data_dir
from benchmarks.fixtures import DVC, Git, TmpDir
from dvc.ignore import DvcIgnore
from dvc.main import main


class DVCStatusBench(BaseBench):
    repeat = (1, 1, 60.0)
    number = 10
    warmup_time = 0

    fixtures = [TmpDir, Git, DVC]

    def setup(self):
        super().setup()
        dataset_path = random_data_dir(10000, 10)
        os.makedirs(os.path.join(self.params["TmpDir"], "data"))
        assert main(["add", "data", "--quiet"]) == 0
        shutil.copytree(dataset_path, "data/data")
        # calculating md5
        assert main(["status", "--quiet"]) == 1

    def time_status(self):
        assert main(["status", "--quiet"]) == 1


class DVCIgnoreBench(DVCStatusBench):
    @staticmethod
    def add_ignore_rules(path, number):
        with open(os.path.join(path, DvcIgnore.DVCIGNORE_FILE), "w",) as f_w:
            for i in range(number):
                f_w.write("{}\n".format(i))

    def setup(self):
        super().setup()
        self.add_ignore_rules(self.params["TmpDir"], 30)
