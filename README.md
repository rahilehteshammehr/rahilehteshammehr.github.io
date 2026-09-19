# Rahil Ehtesham Mehr

A complete Jekyll website based on **Academic Pages**, with About, Research & Projects, six research/project detail pages, a web CV, and a downloadable two-page CV. The profile sidebar and short navigation retain the selected prototype's structure, with light and softened dark themes.

**Start with [Working with the website](docs/EDITING.md)** for the everyday editing workflow, draft previews, content commands, photos, CV updates, and publishing.

```sh
npm run new:post -- "My new story"
npm run new:project -- "My new project"
npm run new:page -- "My new page"
npm run dev:drafts
```

These commands create unpublished drafts. Edit the generated file, then remove `published: false` when ready. `npm run validate` builds and checks the public site.

## Run locally

Requires Ruby 3.2+ (3.3 recommended) and Bundler. Node/npm are convenient command aliases; the site itself has no Node runtime dependencies.

```sh
npm run setup
npm run setup:cv  # once, for auto-generated CVs
npm run dev
```

Open **http://127.0.0.1:4000/**. The server binds to this computer only. Content edits rebuild automatically; restart after editing `_config.yml`.

```sh
npm run build
npm run check
```

You can also use `bundle install`, `bundle exec jekyll serve --host 127.0.0.1 --port 4000`, and `bundle exec jekyll build` directly with a configured Ruby environment; run `npm run cv` before a direct Jekyll build/serve to prepare the selected PDF. The wrapper can use a local Ruby runtime or Homebrew Ruby 3.3, otherwise it uses Ruby from `PATH`. Ignored runtimes and installed dependencies are not included in the repository; install Ruby 3.2+ and Bundler on each new development computer.

## Update content

| Content | File |
| --- | --- |
| Intro, interests, personal paragraph, portrait, email, profile identity | `_data/profile.json` |
| Education, awards, skills, coursework, teaching, service | `_data/cv.json` |
| Research and project descriptions | `_projects/*.md` |
| Beyond Physics posts | `_posts/YYYY-MM-DD-title.md` |
| Homepage sidebar news | `_data/news.yml` |
| Post photographs | `assets/images/` with metadata in each post |
| Site title, sidebar role, FIDE link, fallback portrait/alt text, site URL | `_config.yml` |
| Navigation | `_data/navigation.yml` |
| Layout and palette adjustments | `_sass/_rahil.scss` |

The Markdown/JSON files are the production source. The prototype content file no longer drives the website. Keep `graduation_label` in `_data/profile.json` aligned with the education data when dates change.

### Add or edit a news update

Edit `_data/news.yml` with a short `title`, a quoted `date` in `YYYY-MM` format, and an optional `url`. Omit `url` or leave it empty for plain text. The homepage sidebar shows the three newest updates, with dates displayed as month and year. Internal links should start with `/`; the site's deployment subpath is added automatically.

```yaml
- date: "2026-05"
  title: "Shared an update on my thin-film research."
  url: /research/thin-films-2d-materials/

- date: "2026-04"
  title: "A short update without a link."
```

Copy an entry to add news, or edit its fields to update it; entries are sorted automatically. Only add news with confirmed names and dates.

### Add or edit a post

Posts use the same Markdown-and-front-matter workflow as research projects. They inherit the shared page template, sidebar, navigation, and themes. No HTML, CSS, or navigation edits are needed for routine post editing.

1. Copy `docs/templates/post.md` to `_posts/YYYY-MM-DD-your-title.md`.
2. Change `title` and `summary`, then write the body in Markdown.
3. Save. With `npm run dev` running, the post and Beyond Physics listing rebuild automatically. Otherwise run `npm run build`.

To edit an existing post, open its file in `_posts/`. The index updates automatically and sorts newest first. Keep the filename to keep the URL stable when changing the displayed title. Use unique filename slugs. Future-dated posts stay hidden until a build on or after that date; the site does not rebuild on a schedule. Set `published: false` to keep any post out of normal builds.

### Add photographs

Put images under `assets/images/your-story/` and add a `photos` list above the closing `---` in the post or project:

```yaml
photos:
  - src: /assets/images/your-story/team.jpg
    alt: "Describe what the photograph shows."
    caption: "A caption with the event and date."
  - src: /assets/images/your-story/award.jpg
    alt: "Describe the second photograph."
    caption: "Another caption."
```

The shared gallery appears after the story or project description automatically. Photos open in an on-page carousel with captions, credits, previous/next buttons, arrow-key navigation, touch swipes, and Escape to close. The viewer includes all gallery photos on the page and returns focus to the selected thumbnail when closed. With JavaScript unavailable, image links still work. Add optional `width` and `height` when known to reserve space while loading. For credited photos, add `credit` and `source` (the original page URL); personal photos do not require an external source link.

For galleries between sections, give photos a `group` and place this line where that group belongs:

```liquid
{% include post-gallery.html group='tournament' label='Tournament photographs' %}
```

When a post or project places galleries explicitly, the automatic end gallery is disabled; include each desired group. The chess post demonstrates this optional approach.

### Control photo size and layout

Set defaults once in a post or project’s front matter (alongside `title` and `photos`):

```yaml
gallery:
  layout: grid
  columns: 2
  width: full
  fit: original
```

| Setting | Choices | Default |
| --- | --- | --- |
| `layout` | `featured` (first photo spans the row when the count is odd), `grid` (equal columns), `stack` (one per row) | `featured` |
| `columns` | `1`, `2`, or `3`; `stack` always uses one | `2` |
| `width` | `full` (article width), `medium` (up to 600px), `small` (up to 420px); narrower galleries are centered | `full` |
| `fit` | `original` (whole photo), `landscape` (4:3 crop), `square` (1:1 crop), `portrait` (3:4 crop) | `original` |

All galleries become one column on mobile. Crops only affect page thumbnails; the carousel always contains the complete photograph. Original image `width`/`height` metadata reserves loading space; use `width` and `fit` for presentation.

Override defaults for an individual gallery where you place it:

```liquid
{% include post-gallery.html group='tournament' label='Tournament photographs' layout='grid' columns=3 width='full' fit='square' %}
{% include post-gallery.html group='portrait' label='A portrait' layout='stack' width='small' fit='original' %}
```

Within an individual photo record, optional `span: full` makes it occupy a full row, and `fit: original` (or another crop choice) overrides the gallery crop for that photo. Settings apply in this order: photo crop, gallery include, page defaults, template defaults. Keep images in the `photos` list in the order you want them displayed.

The copyable `docs/templates/photo-post.md` and `docs/templates/photo-project.md` include an automatic gallery and these settings. Use `npm run new:project -- "My project" --photos` to create a project draft with photos. Change paths and captions to your own images before publishing.


Optional post fields: `topic` (e.g. Chess), `period` (e.g. 2023–2025 for a retrospective), `description` (search-preview text), and `cover` (index thumbnail path). With a cover, optional `cover_width` and `cover_height` reserve its space. Without a topic, cover, or photos, a plain text post works normally. If `summary` is omitted, the index uses the opening paragraph.

Use `/assets/` paths as shown; gallery templates handle repository-subpath deployments. For a single inline Markdown image, use `![Description]({{ '/assets/images/your-story/photo.jpg' | relative_url }})`. The first post's image provenance is recorded in `docs/chess-photo-sources.json`.

### Choose the downloadable CV

Set `mode` in `_data/cv_pdf.json`:

- `"auto"` (default): generate the PDF from the website data.
- `"manual"`: use your compiled PDF from `cv-source/manual.pdf`. You can change `manual_file` to another PDF inside `cv-source/`.

Every download link (sidebar, About, and CV page) uses `published_file` from the same settings file. Its default remains `/files/Rahil_Ehtesham_Mehr_CV.pdf`, so switching preserves the public URL. Keep your original manual PDF in `cv-source/`, not the generated `files/` destination. Commit it so GitHub deployment can find it. The source folder and intermediate automatic PDF are excluded from website output.

`npm run build`, `npm run validate`, preview-server startup, and GitHub deployment prepare the selected PDF automatically. Restart the preview server after changing modes. To refresh only the PDF while a preview is already running:

```sh
npm run setup:cv  # once per computer
npm run cv
npm run validate
```

In auto mode, the PDF shares the site's data and project summaries. In manual mode, your PDF is copied byte-for-byte and its source is never overwritten. A missing/invalid manual PDF or unknown mode stops the build; it does not silently use the other version. The web CV and its print button continue to use the website data in either mode. See [content notes](docs/CONTENT.md) for provenance and optional owner inputs.

## Publish with GitHub Pages

The source transfer repository is `theablemo/rahilwebsite`. The final website will be deployed from Rahil’s own repository; no custom domain is configured.

1. Create the intended GitHub repository, usually `<username>.github.io`, and push this project to its `main` branch.
2. In repository **Settings → Pages**, select **GitHub Actions** as the source.
3. Run **Build and deploy website**, or push a change to `main`.

Before Pages is configured, pushes still build and validate the site and skip deployment. After selecting GitHub Actions in Settings → Pages, run the existing workflow to publish.

The workflow installs pinned Ruby dependencies, prepares the selected CV, builds Jekyll, checks all local links/fragments and private-source exclusions, and uploads only `_site`. It derives the site origin and path from GitHub Pages, supporting both a user site and a repository subpath. Pull requests build/check without deploying. For other hosts, set `url` and `baseurl` in `_config.yml` and deploy `_site` after building. Add a `CNAME` only when an actual domain has been chosen.

## Verification and maintenance

See [verification notes](docs/VERIFICATION.md). Automated checks cover generated page structure, local references, fragments, the CV download, sitemap, and exclusions. DOM checks cover themes and mobile controls. Browser rendering has a separate status; source or DOM checks are not visual validation.

The [upstream note](docs/UPSTREAM.md) records the Academic Pages commit, license, preserved sources, and customized files. `Gemfile.lock` pins dependencies. No analytics, remote fonts, comment service, or contact-form backend is required.

The repository contains the production site, editing templates, validation scripts, and source attribution. Historical prototypes, research downloads, design/review artifacts, the original résumé source, caches, and installed dependencies stay local and are ignored by Git. The required vendored Sass sources under `_sass/vendor/` are included.
