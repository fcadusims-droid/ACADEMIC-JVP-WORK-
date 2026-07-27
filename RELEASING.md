# Releasing and obtaining a DOI

The software is packaged (`pyproject.toml`), tested in CI, and citable
(`CITATION.cff`). To mint a DOI so it can be cited independently of the papers:

1. **Enable Zenodo for the repository.** Sign in to <https://zenodo.org> with GitHub,
   open *Settings → GitHub*, and toggle this repository **on**. Zenodo then watches
   for releases.
2. **Cut a GitHub release.** Tag `v0.1.0` and publish. Zenodo archives the tagged
   snapshot and mints a DOI; `.zenodo.json` in the repository root supplies the
   metadata (title, authors, licence, keywords), so nothing needs entering by hand.
3. **Record the DOI.** Add the returned DOI to `CITATION.cff` as
   `doi: 10.5281/zenodo.XXXXXXX`, to the README badge, and to each paper's data
   availability statement. Zenodo also issues a *concept DOI* that always resolves to
   the newest version — prefer that one in the papers.
4. **Re-release on substantive change.** Each new tag gets its own version DOI under
   the same concept DOI, so results in the papers stay pinned to the exact snapshot
   that produced them.

Steps 1 and 2 require repository-owner credentials and are therefore left to the
author; everything they depend on is already in place.
