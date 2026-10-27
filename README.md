# RCA Recruiter

A mobile-friendly helper for preparing and tracking RCA's manual Scratch studio invitations.

## Dashboard

The dashboard is in `index.html`. To publish it with GitHub Pages:

1. Open this repository's **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch **main** and folder **/(root)**, then save.
4. Open the Pages URL GitHub shows you.

The dashboard fetches public managers and curators from the SCA studio, lets you search/select usernames, copy selected usernames, and mark invitations as sent. The “invited” marks are saved only in the browser on that device.

**Scratch still requires you to invite each person individually.** The dashboard does not send invitations, messages, follows, or comments automatically.

If the browser blocks Scratch API requests or Scratch rate-limits them, use the Python builder below instead.

## Python candidate list builder

The Python script reads the public roster, deduplicates managers and curators, excludes the host when identifiable, and writes `rca_candidates.txt`.

Default studio: [SCA studio roster](https://scratch.mit.edu/studios/35469041/curators/)

### Run locally

Requires Python 3.10 or newer. No extra packages are required.

```bash
python recruiter.py
```

To use a different studio ID, set the `SCRATCH_STUDIO_ID` environment variable before running the script.

### Run on GitHub Actions

1. Open the repository's **Actions** tab.
2. Select **Build RCA candidate list**.
3. Click **Run workflow**.
4. Open the completed run and download the `rca-candidates` artifact.

The workflow also runs when `recruiter.py` or its workflow file is changed.

## Respectful recruitment

Be clear that RCA is a separate community. Invite people individually, avoid repeated unwanted invitations, and respect anyone who declines.
