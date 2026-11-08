# Runtime screenshot capture

The `assets/interface_preview_*.png` images are illustrative previews, not screenshots from a running Streamlit process.

To capture genuine runtime screenshots on a machine with the project dependencies installed:

```bash
pip install -r requirements.txt
pip install playwright
playwright install chromium
python capture_screenshots.py
```

The script launches both Streamlit applications, plays through the complete puzzle sequence using the local fallback path when no Gemini key is configured, and saves four browser screenshots under `screenshots/`:

- `version1_initial.png`
- `version1_playthrough.png`
- `version2_initial.png`
- `version2_playthrough.png`

The script does not require an API key for the local fallback playthrough. If a Gemini key is configured, Version 1 uses Gemini responses and Version 2 uses Gemini only to narrate Python-validated outcomes.
