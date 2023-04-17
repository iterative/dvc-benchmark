"""
Tests for modifications to an existing dataset.
"""
import glob
import os
import random
import shutil


def test_partial_add(bench_dvc, tmp_dir, dvc, dataset, remote):
    # Move some files to create a partial dataset
    os.makedirs("partial-copy")
    for f in glob.glob("*", root_dir=dataset, recursive=True):
        if random.random() > 0.5:
            shutil.move(dataset / f, tmp_dir / "partial-copy" / f)

    # Add/push partial dataset
    dvc.add(str(dataset))
    dvc.push()

    # Add more files to the dataset
    shutil.copytree("partial-copy", dataset, dirs_exist_ok=True)

    # Benchmark operations for adding files to a dataset
    bench_dvc("add", dataset, name="partial-add")
    bench_dvc("push", name="partial-add")
    bench_dvc("gc", "-f", "-w", name="noop")
    bench_dvc("gc", "-f", "-w", "-c", name="cloud-noop")


def test_partial_remove(bench_dvc, tmp_dir, dvc, dataset, remote):
    # Add/push full dataset
    dvc.add(str(dataset))
    dvc.push()

    # Remove some files
    for f in glob.glob("*", root_dir=dataset, recursive=True):
        if random.random() > 0.5:
            if os.path.isfile(dataset / f):
                os.remove(dataset / f)
            elif os.path.isdir(dataset / f):
                shutil.rmtree(dataset / f)

    # Benchmark operations for removing files from dataset
    bench_dvc("add", dataset)
    bench_dvc("push")
    bench_dvc("gc", "-f", "-w")
    bench_dvc("gc", "-f", "-w", "-c", name="cloud")
