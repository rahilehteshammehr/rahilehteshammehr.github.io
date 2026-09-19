# Technical maintenance

For everyday content changes, use the [editing guide](EDITING.md).

## Publishing setup

1. Put the repository on the intended GitHub account, with `main` as the publishing branch.
2. In **Settings → Pages**, select **GitHub Actions** as the source.
3. In **Actions**, select **Build and deploy website → Run workflow**, or save a change to `main`.
4. Find the published address in **Settings → Pages**.

The workflow builds and checks pull requests. Changes to `main` deploy only when Pages is configured. The workflow supplies the site address and repository subpath automatically; a `<username>.github.io` repository works too. No custom domain is configured. For another host, set `url` and `baseurl` in `_config.yml` and publish the generated `_site/` directory.

## Local preview

Install Ruby 3.2+ (3.3 recommended), Bundler, Python 3.9+, and Node/npm. Node is only used for command shortcuts and optional interaction checks.

```sh
npm run setup
npm run setup:cv
npm run dev
```

Open <http://127.0.0.1:4000/>. Save a source file and refresh to see the change. Stop with Control-C. Restart after editing `_config.yml` or changing PDF mode. While previewing, `npm run cv` refreshes the PDF after content edits. Manual PDF mode does not need `setup:cv`.

```sh
npm run validate  # build and check the published version
npm run test:cv   # check PDF selection and source preservation
```

Optional interaction checks use jsdom and do not verify browser rendering:

```sh
npm install --prefix .cache/qa --save-exact jsdom@30.0.1
NODE_PATH="$PWD/.cache/qa/node_modules" node scripts/check_ui.cjs
NODE_PATH="$PWD/.cache/qa/node_modules" node scripts/check_gallery.cjs
```

Review changed pages in a browser at desktop and mobile widths, in both themes. Open the PDF after substantial content additions.

## Where things live

| Folder or file | Purpose |
| --- | --- |
| `_data/`, `_posts/`, `_projects/` | Editable profile, CV, news, stories, and projects |
| `_pages/` | Main page composition, standalone pages, and 404 page |
| `assets/` | Images, stylesheet entry point, and browser scripts |
| `_theme/` | Only the layouts, includes, and Sass dependencies used by this site |
| `scripts/` | Build helpers, checks, and three content templates |
| `files/` | Published CV PDF; overwritten from the selected source during builds |
| `docs/` | Editing and maintenance guides, plus photo attribution records |
| `_config.yml` | Site title, search description, routing, and build settings |
| `.github/workflows/pages.yml` | Automated checks and publishing |

`_site/`, `.cache/`, and `vendor/` are local generated output or installed dependencies and stay out of Git. Do not edit generated files. Optional `cv-source/manual.pdf` is an owner-supplied PDF; upload it with the mode setting so deployment can find it. `_theme/`, `scripts/`, `docs/`, and `cv-source/` are excluded from the built website, but any tracked files remain public in the repository.

Profile details live in `_data/profile.json`; CV records in `_data/cv.json`; download selection and the stable public PDF path in `_data/cv_pdf.json`. Automatic and manual downloads are prepared by `scripts/prepare_cv.py`. An invalid selection stops the build.

## Optional authoring shortcuts

```sh
npm run new:post -- "My story"
npm run new:project -- "My project" --photos
npm run new:page -- "My page"
npm run dev:drafts
```

These create unpublished drafts without overwriting existing files. Posts accept `--date YYYY-MM-DD`; all commands accept `--slug short-title`; posts and projects accept `--photos`. Remove `published: false` when ready. Stop a running preview before starting the draft preview.

Standalone pages need a unique `permalink`. To add one to the menu, add a record to `_data/navigation.yml` with `title`, `url`, and `key`, and set the page’s `nav` to that key. Stories and projects do not need menu entries.

For internal Markdown links and inline images, use Jekyll’s `relative_url` filter so repository subpaths work:

```liquid
[Research]({{ '/research/' | relative_url }})
![Description]({{ '/assets/images/photo.jpg' | relative_url }})
```

## Gallery settings

Optional defaults go above the closing `---` in a post or project:

```yaml
gallery:
  layout: grid
  columns: 2
  width: full
  fit: original
```

| Setting | Choices |
| --- | --- |
| `layout` | `featured` (default; first photo spans an odd-sized group), `grid`, `stack` |
| `columns` | `1`, `2` (default), `3`; mobile and stack layouts use one |
| `width` | `full` (default), `medium` (600px), `small` (420px) |
| `fit` | `original` (default), `landscape`, `square`, `portrait`; crops thumbnails only |

A photo can have `span: full` or its own `fit`. Optional numeric image `width` and `height` reserve loading space. To place a group between paragraphs, give its photos `group: tournament` and insert:

```liquid
{% include post-gallery.html group='tournament' label='Tournament photographs' %}
```

An explicit gallery disables the automatic end gallery, so include every desired group. Include parameters can override page defaults, for example `columns=3 fit='square'`. The existing chess story demonstrates grouped galleries.

## Theme and attribution

The design derives from [Academic Pages](https://github.com/academicpages/academicpages.github.io/tree/3d28cd27d0551b3d9dd8132f207538355fbbc7cc), imported at commit `3d28cd27d0551b3d9dd8132f207538355fbbc7cc`. Its MIT license is retained in [`LICENSE`](../LICENSE). Only used layouts, includes, and Sass imports are retained; unused demo, comment, analytics, icon-font, and alternate-theme sources have been removed.

Site-specific styles are in `_theme/styles/_rahil.scss`; `assets/css/main.scss` loads the retained base styles first. Required Breakpoint and Susy Sass sources remain under `_theme/styles/vendor/`. Compare upstream changes selectively rather than replacing the customized theme wholesale. Local scripts handle theme switching, navigation, printing, and photo viewing. No analytics, remote fonts, or comment service is configured.

Photographs link to their source pages in the chess story. [`chess-photo-sources.json`](chess-photo-sources.json) retains the original asset URLs.
