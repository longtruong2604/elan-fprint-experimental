#!/usr/bin/python3
# SPDX-License-Identifier: LGPL-2.1-or-later
"""Build an isolated, ELAN-only library and its hash-pinned deployment manager."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
OUT = ROOT / "out"


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    if os.geteuid() == 0:
        raise RuntimeError("Build as your normal user; sudo is only for installation")
    if WORK.exists() or OUT.exists():
        raise RuntimeError("work/ or out/ already exists; use a fresh checkout for a new build")
    manifest = json.loads((ROOT / "source-manifest.json").read_text())
    for name, expected in manifest["sha256"].items():
        path = ROOT / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Source integrity mismatch: {name}")
    WORK.mkdir(mode=0o700)
    source = WORK / "libfprint-v1.94.100"
    run("tar", "--extract", "--gzip", "--no-same-owner", "--no-same-permissions",
        "--file", str(ROOT / "sources/libfprint-v1.94.100.tar.gz"), "--directory", str(WORK))
    for name in manifest["patches"]:
        run("git", "-C", str(source), "apply", "--whitespace=nowarn", str(ROOT / name))
    build = WORK / "build"
    options = ["--buildtype=release", "--libdir=lib64", "-Ddrivers=elan",
               "-Dexperimental-sift-test=false", "-Dinstalled-tests=false",
               "-Dintrospection=true", "-Dudev_rules=disabled", "-Dudev_hwdb=disabled",
               "-Ddoc=false", "-Dgtk-examples=false"]
    run("meson", "setup", str(build), str(source), *options)
    # Build only the library target; neither build nor run test executables.
    run("ninja", "-C", str(build), "libfprint/libfprint-2.so.2.0.0")
    OUT.mkdir(mode=0o700)
    library = OUT / "libfprint-2.so.2.0.0"
    shutil.copyfile(build / "libfprint/libfprint-2.so.2.0.0", library)
    digest = hashlib.sha256(library.read_bytes()).hexdigest()
    template = (ROOT / "manage.py.in").read_text()
    if template.count("@LIBRARY_SHA256@") != 1:
        raise RuntimeError("Installer template must contain exactly one library hash placeholder")
    (OUT / "manage.py").write_text(template.replace("@LIBRARY_SHA256@", digest))
    (OUT / "build.json").write_text(json.dumps({
        "status": "experimental-unvalidated-build", "library_sha256": digest,
        "options": options, "source_manifest": manifest,
        "tests_run": False, "hardware_validation": "not performed for this build",
    }, indent=2) + "\n")
    print("Built out/libfprint-2.so.2.0.0 and out/manage.py. Nothing installed.")
    print("Installation and rollback instructions: README.md")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Build stopped: {error}", file=sys.stderr)
        sys.exit(1)
