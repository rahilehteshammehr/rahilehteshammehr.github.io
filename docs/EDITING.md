# Working with the website

This is a file-based Jekyll website. Edit its Markdown, JSON, and YAML files in a text editor, preview locally, then publish the changes through GitHub. There is no separate admin dashboard, database, or subscription. Everyday content edits do not require HTML or CSS.

## Your usual workflow

Open a terminal in this project folder. On this computer, setup is already available:

```sh
npm run dev
```

Visit [the local preview](http://127.0.0.1:4000/). Save an edit, wait for the terminal to say the site regenerated, and refresh the browser. Stop the server with **Control-C**. Restart it after changing `_config.yml`. If port 4000 is already in use, use the running preview or stop its terminal before starting another one.

Before publishing:

```sh
npm run validate
```

This builds the site and checks page structure, local links, images, section links, the PDF download, the sitemap, and excluded source files. A successful check does not assess factual accuracy, external website availability, or visual appearance: also review your changed pages, both themes, and a narrow browser window.

On another computer, install Node/npm, Python 3, Ruby 3.2+ (3.3 recommended), and Bundler, then run `npm run setup` and `npm run setup:cv` (the latter is needed for auto-generated PDFs). The ignored `.cache` and `vendor` folders are local dependencies, not website content.

## Where to edit

| What you want to change | Source |
| --- | --- |
| Intro paragraphs, highlighted message, interests, personal paragraph, name, email, affiliation, location, LinkedIn, portrait, graduation label | `_data/profile.json` |
| Education, awards, teaching, skills, languages, courses, service, CV update date | `_data/cv.json` |
| PDF mode and manual PDF source | `_data/cv_pdf.json` |
| Research/project summary and detail page | Its file in `_projects/` |
| Story or photographs | Its file in `_posts/`; image files in `assets/images/` |
| Three newest homepage news items | `_data/news.yml` |
| About contact paragraph, research introduction, other page-specific text | `_pages/` |
| Navigation labels and links | `_data/navigation.yml` |
| Site title, search description, sidebar role, FIDE link, portrait alt text, domain settings | `_config.yml` |
| Colors, spacing, typography, layout | `_sass/_rahil.scss` |

`profile.json` is the live source of contact details for both the website and auto-generated CV. The author identity fields retained in `_config.yml` are upstream compatibility values. `title` still controls the masthead and browser title. Education details and `graduation_label` describe different display contexts; update both when graduation changes.

Never edit `_site/` or `_site-subpath/`: they are generated and overwritten on the next build. Historical prototypes and the original résumé source stay on the original authoring computer and are not part of the repository. The active website and automatic CV use the Markdown and JSON files described above.

## Feature a current-focus message

Edit `highlight` in `_data/profile.json`:

```json
"highlight": "I am currently looking for graduate-level positions in experimental physics for the 2027 cohort."
```

This optional message appears in bold on a subtle background below the About introduction, above the contact links. Use plain text; bold styling is automatic. Replace it whenever your focus changes. Set `"highlight": ""` or remove the field to hide it entirely. It appears only on the homepage and is not included in the CV.

## Add a post

```sh
npm run new:post -- "My new story"
```

For photographs:

```sh
npm run new:post -- "A tournament weekend" --photos
```

The command prints the new filename. Open it, replace the summary and body, and keep the `---` lines around the settings at the top. Change the date using `--date 2026-09-19` if needed; by default, it uses your computer's current date.

Posts are automatically listed under **Beyond Physics**, newest first. No navigation edits are needed. The filename slug controls the URL; changing only the displayed title preserves links. An optional `--slug my-story` sets a specific slug. Existing files and duplicate post slugs are never overwritten.

## Add a research project

```sh
npm run new:project -- "My new project"
```

To start with a photo gallery, use `npm run new:project -- "My new project" --photos`. Replace the example image paths, descriptions, and captions. Existing projects can add the same `photos` and optional `gallery` settings described below.

Fill in the front matter:

- `title`: full project title; optional `short_title` overrides it in listings.
- `category`: exactly `Undergraduate research` or `Academic project`.
- `period`: a readable date or period, such as `Fall 2026`.
- `field`: field of study.
- `summary`: plain text used in listings and the PDF. Keep it concise.
- `order`: a number; smaller numbers appear first within each category.
- `topics`: a list such as `["Thin films", "Materials"]`, or `[]`.
- Optional `supervisor` and `supervisor_url`: omit either if unavailable.

Write the full description below the second `---`. Published undergraduate research appears on About, Research & Projects, and the web CV; academic projects appear on Research & Projects and the web CV. Regenerate the PDF to include the new entry there.

## Drafts and future dates

New content starts with `published: false`, so normal builds and deployment omit it. To preview drafts, stop the normal preview server and run:

```sh
npm run dev:drafts
```

This includes unpublished and future-dated content on your computer. Remove `published: false` when ready, and make sure a post's date is not in the future. Run `npm run validate` to check the normal public build before publishing.

A future date is **not an automatic publishing schedule**. A static site only changes on a new build: push a change or run the deployment workflow after the date arrives. Draft projects are also excluded from the generated PDF.

## Add photographs

Copy photos into a folder such as `assets/images/my-story/`. Use lowercase filenames with hyphens. Compress large camera originals before adding them; keep enough resolution for the full-screen viewer.

In the post or project's front matter, add a `photos` list or replace the example paths and descriptions:

```yaml
photos:
  - src: /assets/images/my-story/team.jpg
    alt: "The university chess team beside the tournament boards."
    caption: "A caption with the event and date."
```

Describe what is visible in `alt`; use `caption` for context. Add optional `credit` and `source` for a source-page link. Optional image `width` and `height` reserve space while loading. The shared gallery and viewer handle the presentation automatically, below the post or project description. Project photos appear on the project detail page.

Gallery defaults can be set in the same front matter:

```yaml
gallery:
  layout: grid
  columns: 2
  width: full
  fit: original
```

Use `fit: original` to show whole photos; `square`, `landscape`, and `portrait` crop thumbnails only. Use `width: small` or `medium` for narrower galleries. The [README gallery reference](../README.md#control-photo-size-and-layout) covers grouped galleries and per-photo overrides.

## Add news or a standalone page

For news, copy a record in `_data/news.yml`. Use a quoted `YYYY-MM` date, a title, and an optional URL. The newest three appear automatically. Internal URLs start with `/`. Only publish news with confirmed names and dates; the unfinished research announcement has been removed.

For a standalone page:

```sh
npm run new:page -- "My new page"
```

Edit its title, description, and Markdown. It inherits the shared design. Link to it from an existing page, or add a navigation record:

```yaml
  - title: My new page
    url: /my-new-page/
    key: my-new-page
```

For a navigation item, also add `nav: my-new-page` to the page's front matter so the active link is highlighted. Keep the main menu short; ordinary stories and projects already have listings. Ensure each standalone page has a unique `permalink`.

## Choose and update the downloadable CV

Edit `_data/cv_pdf.json`. Only change `mode` to switch:

```json
{
  "mode": "auto",
  "manual_file": "cv-source/manual.pdf",
  "published_file": "/files/Rahil_Ehtesham_Mehr_CV.pdf"
}
```

- **Auto:** keep `"mode": "auto"` to generate the PDF from profile data, CV data, and project summaries. Run `npm run setup:cv` once per computer to install its dependencies.
- **Manual:** compile your LaTeX CV yourself, put the resulting PDF at `cv-source/manual.pdf`, and set `"mode": "manual"`. A different filename is fine if you update `manual_file` to match (inside `cv-source/`). Commit the PDF along with the setting so deployment has access to it. No LaTeX installation is needed by the website.

Keep `published_file` unchanged to preserve existing public links. All PDF downloads use this one setting, including the sidebar, About, and CV page. The build copies your manual PDF byte-for-byte and never alters the original. Neither the source folder nor the intermediate auto-generated PDF is included in the website output.

Then run:

```sh
npm run validate
```

Builds, preview-server startup, and GitHub deployment prepare whichever mode is selected. **Restart `npm run dev` after changing modes.** While the preview server is running, `npm run cv` refreshes the selected PDF after content changes or replacing your manual file. A missing/non-PDF manual file or invalid mode stops the build with an error rather than publishing the wrong version.

In auto mode, update `updated` in `_data/cv.json` yourself. The web CV and **Print this page** always use website data; this switch controls the downloadable PDF only. Open `files/Rahil_Ehtesham_Mehr_CV.pdf` to check the selected result. Review every page after substantial additions: auto-generated content can grow beyond the current two pages.

## Formatting and troubleshooting

Markdown supports `## Section`, `**bold**`, `- list items`, and `[link text](https://example.com)`. Use the page's front-matter title rather than adding another `# Title`. For links within this site, use the deployment-safe form:

```liquid
[See research]({{ '/research/' | relative_url }})
![Photo description]({{ '/assets/images/my-story/team.jpg' | relative_url }})
```

JSON requires double quotes, commas between items, and no trailing comma after the last item. YAML requires spaces instead of tabs; quote titles containing a colon. Dates in news must be quoted. In JSON strings, write `\"` for a literal quotation mark. Copy a nearby valid entry and change its values.

- **Edit not appearing:** confirm the source file, refresh the browser, inspect the terminal for errors, and check `published` and the post date.
- **Missing photo:** verify capitalization and the exact file path; run `npm run validate`.
- **Project missing from listings:** verify its exact category and `published` setting.
- **PDF looks old:** run `npm run cv`, rebuild, and reopen the PDF.
- **Content looks cramped:** shorten listing summaries while keeping detail in the Markdown body. Preview mobile and both themes.

## Publish

The source transfer repository is `theablemo/rahilwebsite`; the final deployment will use Rahil’s own GitHub repository. The existing GitHub Pages workflow builds, prepares the selected PDF, validates, and deploys when changes reach `main`, once the repository has Pages enabled with GitHub Actions. See [publishing instructions](../README.md#publish-with-github-pages).

After setup, you can edit these same files in GitHub's web editor or locally. Use a branch/pull request to review changes before merging into `main`. Version control lets you restore earlier content. Excluded files do not enter the website build, but a **public repository still exposes its tracked source files**: review source documents and personal material before choosing repository visibility.
