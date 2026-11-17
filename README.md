# Experimental ELAN 04f3:0c4d fingerprint support

Build a libfprint SIFT matcher integration for the ELAN **04f3:0c4d, revision 0187** tap reader on **Fedora 44 x86_64**. This is an experimental source release, not a validated authentication product or an official libfprint/Fedora package.

## What is known

On one Lenovo XiaoXinAir 14ALC 2021, enrollment and persistence across an isolated fprintd restart worked. That run accepted one genuine probe (score 39) and rejected three other-finger probes (scores 2, 0, 4; threshold 8). A subsequent normal system enrollment accepted **only 2 of 5 genuine verification attempts**, with one retry-scan. These small observations do not establish false-accept or false-reject rates. Multiple users, other fingers, reboot/resume, and SELinux enforcing operation remain unvalidated.

The release build excludes virtual drivers and keeps the threshold and template format unchanged. It has not had hardware validation. Revision 2410, other revisions, other Fedora releases, and other architectures are outside this release's scope. The upstream reference project targeting another revision does not establish compatibility here.

## Build without root

Install build dependencies on Fedora:

```fish
sudo dnf install gcc gcc-c++ meson ninja-build git python3 tar gzip glib2-devel libgusb-devel pixman-devel gobject-introspection-devel opencv-devel fprintd policycoreutils
python3 build.py
```

Run from this directory. The archive is bundled; the build does not fetch source or run tests. `source-manifest.json` records the source/patch hashes and provenance. Hashes detect accidental changes, not the authenticity of an untrusted download. Review the source before running the root installer.

The script creates `work/` and `out/`, refusing to overwrite either. Use a fresh checkout for a rebuild. Only the library target is compiled. `out/` contains the library, a manager pinned to its SHA-256, and build metadata. Compiler/dependency versions may change the binary hash; bit-for-bit reproducibility is not claimed.

## Install deliberately

Keep password authentication available. Check the reader's revision with `lsusb -v -d 04f3:0c4d` if usbutils is installed. The installer also checks USB sysfs and refuses a missing, ambiguous, or unsupported reader before activation.

```fish
sudo /usr/bin/python3 -I out/manage.py install
```

Installation restarts fprintd, so do not run it during another fingerprint operation. It installs a root-owned versioned library under `/usr/local/lib/elan-fprint/`, a hash-pinned rollback manager, and a scoped fprintd service override. It checks the daemon's actual mapped library and attempts rollback if activation fails. It preserves package libraries, `/usr/local/lib64`, PAM/authselect settings, and existing enrollments. It restores standard SELinux labels without disabling enforcement; successful installation does not prove operation under enforcing policy.

The installer refuses conflicting overrides. If a previous experimental version is installed, use that version's recorded rollback command first; the new installer does not overwrite it. An interrupted installation may require inspecting the printed recovery command and root-owned state before proceeding.

This build includes only the ELAN driver, so other fingerprint readers are unavailable to fprintd while the override is active. SIFT templates are incompatible with ordinary libfprint matching. Existing baseline templates may need re-enrollment; enrollment can replace the selected finger's template. Preserve any templates you need before doing so.

Enroll as your normal user, without sudo:

```fish
fprintd-enroll -f right-index-finger
```

Press briefly and lift fully between prompts. The underlying stitched-image driver may still display swipe wording. Use a different `-f` value to enroll another finger, such as `left-index-finger` or `right-thumb`. Adding fingers does not establish recognition reliability.

This installer does not enable fingerprint login in PAM. Desktop/login configuration is a separate administrator decision after evaluating the experimental matcher.

## Rollback and status

Save the exact rollback command printed during installation. The installed copy remains usable if this checkout is removed. From an unchanged build directory:

```fish
sudo /usr/bin/python3 -I out/manage.py status
sudo /usr/bin/python3 -I out/manage.py rollback
```

Rollback removes only the unchanged override owned by this build and restores the service's prior active/inactive state. It retains versioned files, recovery snapshots, and fingerprints. Baseline libfprint cannot use SIFT enrollments; enroll again with the restored driver if it supports your device. A modified override is left in place for manual inspection.

## Sharing and reporting

Publish only this source directory or its prepared source archive. Exclude `work/`, `out/`, logs, raw fingerprint images, descriptor arrays, and `/var/lib/fprint`. Never attach biometric templates to an issue. Useful reports include Fedora version, USB ID/revision, build hash, whether SELinux is enforcing, and sanitized status messages. Do not publish personal usernames or serial numbers.

The source archive includes existing upstream/integration test sources through the source and patches; this release workflow neither adds tests nor builds or runs their executables. The build result is not evidence of authentication accuracy. Before describing a future release as stable, recognition and false acceptance need evaluation across users and environments.

## Source and license

See [NOTICE.md](NOTICE.md), [COPYING](COPYING), and [source-manifest.json](source-manifest.json). The patch series applies in numbered order to the bundled libfprint 1.94.100 source. All integration sources are supplied as patches. Public releases should retain those sources, licenses, and provenance alongside any distributed binaries.
