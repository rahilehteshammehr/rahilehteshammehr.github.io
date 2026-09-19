# Content and assets

The website and public CV combine two user-supplied sources: the active, uncommented content of `main.tex`, and the LinkedIn export `Profile.pdf` supplied on 19 September 2026. The original résumé stays unchanged on the authoring computer and is excluded from both Git and site output. The LinkedIn export remains in the user's Downloads folder and is not published.

## LinkedIn updates

- Current experimental research in thin films and two-dimensional materials, including hands-on fabrication and characterization, is described in the export's summary. No start date, supervisor, specific techniques, or results were supplied; these are not invented.
- University chess team membership is dated November 2022–present, superseding the older résumé's Summer 2024 start. The 2025 Iranian National Inter-University Chess Championship team silver is added alongside the earlier awards.
- Chess instruction at Shahmate chess school is dated March 2023–July 2026. Certified-instructor status comes from the summary; the export does not identify the certifying body. The earlier private tutoring record is retained separately because the sources do not establish that the roles are identical.
- Education is presented as 2022–expected 2027. LinkedIn gives January 2022–2027; the original résumé gives September 2022–expected June 2027. Months are omitted pending confirmation.
- The earlier laser–tissue research is retained with “Started June 2024”; its end date and ongoing status are not confirmed by the new export.
- Older GPA, coursework, projects, skills, service, and awards remain résumé-sourced; their absence from LinkedIn is not evidence that they should be removed.

The site presents two undergraduate research entries and four academic projects. Descriptions add no numerical results, publications, project repositories, or fabricated figures.

The supplied `1785190497275.jpeg` is copied unchanged to `assets/images/rahil-ehtesham-mehr.jpeg` and displayed in the existing circular profile frame. The LinkedIn URL is supplied by the user, linked in the sidebar, public PDF, and structured profile metadata. Live LinkedIn retrieval was blocked; all content updates rely on the supplied export.

## Editing

- `_data/profile.json`: introductory paragraphs, interests, personal paragraph, shared name/email/affiliation/location, LinkedIn URL, portrait path, and graduation label. Both the website and PDF use this contact information.
- `_data/cv.json`: education, awards, teaching, skills, languages, courses, and service.
- `_projects/*.md`: research/project metadata and detail text; summaries appear on the site and in the PDF. Supervisor fields are optional.
- `_config.yml`: site title, sidebar role, FIDE link, fallback portrait/alt text, deployment settings.
- `_pages/*.md`: page composition and text.
- `_data/navigation.yml`: the navigation items.
- `_posts/*.md`: Beyond Physics stories, including gallery metadata and captions.

## Chess story sources — 19 September 2026

The first Beyond Physics post synthesizes the four official pages supplied by the user:

- [Region 1 championships](https://sport.sharif.ir/chess-region-1-championship-girls-boys-1402): 10–12 Dey 1402 (31 December 2023–2 January 2024); Rahil won board 3 gold in standard chess. The women’s team finished second in standard and rapid and third in blitz, qualifying for the national Olympiad.
- [2024 national Olympiad](https://sport.sharif.ir/16th-sports-cultural-olympiad-1403-isfahan): explicitly names Rahil, Sara Orooji, and Fatemeh Mehrabi and records second place in women’s standard team chess. Women’s events were hosted by Isfahan University of Technology in August 2024.
- [Host university gallery](https://olympiad16.iut.ac.ir/fa/node/1714): photographs of the women’s chess medal ceremony. The page’s changing calendar/header date is not treated as the event date.
- [Sharif recognition ceremony](https://sport.sharif.ir/w/-100): 20 Khordad 1404 (10 June 2025), honoring the 16th Olympiad medalists. This ceremony is not evidence of a separate 2025 competition result; the existing CV’s 2025 award remains based on the supplied LinkedIn export.

The user confirmed the numbered photos 1, 2, 3, 4, 8, 9, 16, and 17 for this post. These are copied unchanged into `assets/images/chess/`. Captions describe the group/event without guessing which person is Rahil. Every image links to its original source page; `docs/chess-photo-sources.json` preserves exact original asset URLs and selection numbers. All 25 extracted candidates and raw page downloads remain excluded under `.cache/chess/`.

The story is a retrospective in the site’s existing first-person voice, with an explicit 2023–2025 event period. The filename uses the last documented event date for sorting. No personal emotions, game scores, or medal categories beyond the official reports are invented.

In auto mode, the public PDF is derived from the same site data. The `_data/cv_pdf.json` setting can instead select an owner-supplied compiled PDF from `cv-source/`. It excludes private reference email addresses and commented-out LaTeX content. Prepare the selected PDF with `npm run cv`; normal builds and the Pages workflow do this automatically. Auto mode needs `npm run setup:cv` once per computer. `scripts/build_cv.py` only generates the intermediate automatic source; `scripts/prepare_cv.py` selects and publishes the output. It is a typeset adaptation, not a compiled copy of `main.tex`.

## Outstanding owner inputs

- Exact education months, current research start date/supervisor, and the earlier laser–tissue role's ongoing status.
- The CMB supervisor's name is spelled “Baharm Mashhoon” in the original résumé; that spelling remains pending confirmation.
- The source transfer repository is `theablemo/rahilwebsite`. Rahil’s final hosting repository and any custom domain remain to be configured. No Scholar profile or publication has been invented.
- The unfinished May 2026 news announcement was removed because its supervisor and date were unconfirmed. Add it back only with confirmed details.

The FIDE link comes from the résumé. A numeric current rating is omitted because it can change.
