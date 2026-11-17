# Source provenance and license notices

- Base: libfprint 1.94.100, source archive extracted from Fedora's `libfprint-1.94.100-1.fc44.src.rpm`. Archive URL and SHA-256 are recorded in `source-manifest.json`. The Fedora spec applied no additional patches. The original source archive includes its copyright and license notices. libfprint is predominantly LGPL-2.1-or-later; its NBIS subtree contains NIST public-domain code and associated notices. Preserve those notices.
- SIFT reference: https://github.com/andresgarcia0313/libfprint-tod-elan-04f3-0c4d at commit `bc4d6a594cefea17a55e739c752495ea5a52d0ab`, specifically `src/elan0c4d-sift.cpp` and its header. The source and attribution are retained by the integration patch. Its LGPL-2.1-or-later license is copied to `licenses/elan-sift-LICENSE`.
- Local changes: metadata-only observation instrumentation; opt-in, revision-restricted SIFT integration; bounded versioned template persistence; and standalone build/deployment tooling. The local additions are distributed under LGPL-2.1-or-later. Existing third-party file notices govern those files.
- OpenCV and other dynamically linked dependencies are supplied by the host distribution and retain their respective licenses. They are not bundled here.

The original reference's observations about matching are not measurements of this adaptation. This package reuses its feature/matching algorithm, not its complete capture pipeline. No endorsement by the reference author, libfprint maintainers, Fedora, Lenovo, or ELAN is implied.

The installation manager is derived from the local diagnostic deployment manager. The public variant adds Fedora/device preflight, a generated per-build hash, and user-independent paths. The source package does not include private diagnostic policy helpers or user biometric data.
