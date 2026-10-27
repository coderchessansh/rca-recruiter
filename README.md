# RCA Recruiter — Candidate List Builder

A small read-only helper that builds a list of public managers and curators from the SCA Scratch studio for RCA to review.

**It does not automatically invite, follow, message, or comment on anyone.** Review the list and invite people manually and respectfully.

## What it does

- Reads the public roster using Scratch's public API.
- Collects studio managers and curators.
- Removes duplicate usernames.
- Excludes the studio host when the API identifies the host.
- Writes the list to `rca_candidates.txt`.

Default studio: [SCA studio roster](https://scratch.mit.edu/studios/35469041/curators/)

## Run locally

Requires Python 3.10 or newer. No extra packages are required.

```bash
python recruiter.py
```

The script creates `rca_candidates.txt` in the current directory.

To use a different studio ID, set the `SCRATCH_STUDIO_ID` environment variable before running the script.

## Run on GitHub

1. Open the repository's **Actions** tab.
2. Select **Build RCA candidate list**.
3. Click **Run workflow**.
4. Open the completed run and download the `rca-candidates` artifact.

The workflow also runs when `recruiter.py` or its workflow file is changed.

## Notes

- This relies on Scratch's public API and may need changes if the API changes.
- The script does not automate recruitment actions.
- Be transparent that RCA is a separate community, and respect anyone who declines an invitation.
