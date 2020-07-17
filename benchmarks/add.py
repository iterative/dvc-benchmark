import logging
import os
import shutil

from benchmarks.base import BaseBench, init_dvc

logger = logging.getLogger(__name__)


class Add(BaseBench):
    repeat = 3

    params = ["copy", "symlink", "hardlink"]
    param_names = ["link_type"]

    def setup(self, link_type):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = os.path.join(
            os.environ["ASV_CONF_DIR"], "data", "cats_dogs"
        )
        shutil.copytree(dataset_path, "data")
        self.dvc("config", "cache.type", link_type, "--quiet")

    def time_cats_dogs(self, link_type):
        self.dvc("add", "data", "--quiet")
