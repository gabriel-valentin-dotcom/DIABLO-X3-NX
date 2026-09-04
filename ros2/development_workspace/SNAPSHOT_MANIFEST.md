# Snapshot Manifest

> This manifest records the **historical 2026-08-19 Batch 1 source snapshot**. A later current integration selection is documented separately in [`CURRENT_SOURCE_2026-09-04.md`](CURRENT_SOURCE_2026-09-04.md).

## Source archive

- Date: **2026-08-19**
- Archive: `DIABLO_diablo_ws_src_2026-08-19.tar.gz`
- SHA-256: `c20ce23fe55cd328dc3485beed217fb3e45c201e9df069f5d56fc9f9f76b40a7`
- Source root: `diablo_ws/src`

The archive hash records the private source snapshot used as the basis for public review. The archive itself is not published because it also contains excluded third-party, historical and private-development material.

## Batch 1 — published packages

- `diablo_safety`
- `diablo_tracker`
- `diablo_nx_bringup`

Batch 1 contains **20 source/package files** across these three reviewed ROS 2 packages.

The package-level `README.md` files and source-navigation documents added later in the public repository are explanatory GitHub documentation. They are **not counted as original files from the 2026-08-19 source archive** and do not alter the archived source snapshot.

## Later current integration source

The 2026-08-19 snapshot is intentionally preserved as development history. It has not been silently rewritten to match the later robot workspace.

A second review from the current NX `diablo_ws/src` workspace was published on **2026-09-04** with selected Camera/perception, FOLLOW manager, AUTO, safety and INTERACT/runtime source. Its archive hash, included files and publication boundaries are recorded in [`CURRENT_SOURCE_2026-09-04.md`](CURRENT_SOURCE_2026-09-04.md).

## Excluded from Batch 1

The following categories were deliberately kept out of this first publication batch:

- third-party/vendor repositories such as RealSense ROS and SLLIDAR ROS 2
- DDTRobot interface packages that belong to the upstream DIABLO ROS 2 project
- backup and historical source variants
- temporary diagnostics and generated runtime material
- generic test boilerplate not needed to understand this batch
- older personal/prototype interaction material
- larger active DIABLO packages not part of the original Batch 1 review

## Publication-safety edits

The real source is preserved as closely as practical. Limited publication-safety edits were made where needed:

- private maintainer contact information replaced by a project-safe placeholder
- private NX home-directory deployment paths generalized
- private local network/SSH identifiers generalized when encountered in reviewed material

No synthetic implementation was substituted for missing code.
