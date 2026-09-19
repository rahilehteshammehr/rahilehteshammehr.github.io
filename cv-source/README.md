# Manual CV source

Put your compiled LaTeX PDF here as `manual.pdf` (or update `manual_file` in `_data/cv_pdf.json`). Do not put it in the generated `files/` destination.

Set `mode` to `manual` in `_data/cv_pdf.json`, then run `npm run validate`. All CV download links use the selected PDF. Set `mode` back to `auto` to use the website-data version again.

This folder is excluded from the website output; only the selected PDF is copied to the public download URL. Your original manual PDF is never modified by the generator. Commit your manual PDF with the source project so deployment can find it. Repository visibility still governs who can access the source files.
