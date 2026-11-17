# Experimental source candidate — 2026-11-17

This candidate packages the existing revision-0187 SIFT/persistence integration.

Changes from the private diagnostic workspace:

- Bundled checksum-pinned libfprint source and the ordered integration patches.
- Standalone build restricted to the ELAN driver, with the virtual-device exception disabled.
- Per-build hash-pinned installer with Fedora 44 x86_64 and exact USB revision preflight.
- User-independent installation instructions, scoped rollback, licensing, and privacy guidance.
- Separate public source archive excluding diagnostics, logs, enrollments, and built artifacts.

The source candidate compiled successfully on the development host. The ELF has
SONAME `libfprint-2.so.2` and no RPATH/RUNPATH. The build generated no test
executables and no tests were run. This candidate's installer and hardware
behavior have not been exercised. The installed development driver was unchanged.

The threshold, feature matcher, capture protocol, and serialized template format
remain unchanged. Recognition improvements are not claimed: the latest reported
system run matched 2/5 genuine attempts. Public distribution should remain marked
experimental until the outstanding reliability and authentication accuracy work
is completed.
