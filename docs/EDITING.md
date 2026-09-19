# Updating the website

You can make everyday updates on GitHub using your browser. You need to be signed in with permission to edit this repository. Publishing must be [set up once](DEVELOPMENT.md#publishing-setup).

## Make a small change

1. Open the file you want to change using the table below.
2. Click the pencil icon to edit it. Change the text, keeping the surrounding punctuation and spacing.
3. Click **Commit changes**, write a short description such as “Update research interests,” and save to `main`. A commit is a saved version of your changes.
4. Open the repository’s **Actions** tab. Wait for **Build and deploy website** to finish successfully, then visit your website and check the changed page.

If GitHub requires a pull request, save to a new branch, open the pull request, and merge it after the checks pass. A pull request is a proposed change awaiting review. A green build only publishes when Pages has been configured; the website address is in **Settings → Pages**.

| What you want to update | Where to edit |
| --- | --- |
| Introduction, interests, highlighted message, contact links, portrait, sidebar role | [`_data/profile.json`](../_data/profile.json) |
| Education, awards, teaching, skills, coursework, service, CV update date | [`_data/cv.json`](../_data/cv.json) |
| Research/project descriptions | The matching file in [`_projects/`](../_projects/) |
| Beyond Physics stories | The matching file in [`_posts/`](../_posts/) |
| Homepage news | [`_data/news.yml`](../_data/news.yml) |
| Downloadable CV choice | [`_data/cv_pdf.json`](../_data/cv_pdf.json) |

In `.json` files, edit the text between double quotes. Keep commas between entries, with no comma after the last entry. To put quotation marks inside text, write `\"`. In `.md` and `.yml` files, preserve indentation and use spaces, not tabs.

Set `highlight` to `""` to hide the highlighted homepage message. When graduation details change, update the education entry in `cv.json` and the graduation labels in `profile.json`.

## Add a story or research project

1. Open the [story template](../scripts/templates/post.md) or [project template](../scripts/templates/project.md), then click **Code** to see and copy its contents.
2. Open [`_posts/`](../_posts/) for a story or [`_projects/`](../_projects/) for a project. Choose **Add file → Create new file**.
3. Name a story `YYYY-MM-DD-short-title.md`, using its publication date. Name a project `short-title.md`. Use lowercase letters and hyphens, with a unique filename.
4. Paste the template, replace its example text, and keep the two `---` lines. The lines between them are the entry’s settings; write the main text below the second line.
5. Remove `published: false` when ready, then save with **Commit changes**. Stories and projects appear in their lists automatically.

For projects, use exactly `Undergraduate research` or `Academic project` as the category. A smaller `order` number appears first. The summary also appears in the automatic PDF CV. Optional supervisor fields can be copied from an existing project.

`published: false` hides an entry from the website, but its file remains visible in this public repository. Future-dated stories stay hidden until a build on or after that date; they do not publish on a timer. Keep an existing filename when changing a title so old links continue to work.

Use `## Heading`, `**bold text**`, `- list item`, and `[link text](https://example.com)` for simple formatting. The settings already supply the page title.

## Add photographs

Open [`assets/images/`](../assets/images/) and use **Add file → Upload files** to upload your photos. Use filenames such as `chess-team.jpg`. Then add this above the closing `---` in a story or project:

```yaml
photos:
  - src: /assets/images/chess-team.jpg
    alt: "The chess team beside the tournament boards."
    caption: "Our team at the tournament."
```

Repeat the three lines starting with `- src` for each photo. `alt` describes what is visible for people using a screen reader; `caption` is the text shown below the photo. Check that the filename matches exactly, including capitalization. For a credited image, add `credit: "Photographer or organization"` and `source: "https://example.com/original-page"` below its caption, at the same indentation.

Photos appear below the story automatically and open in a larger viewer when clicked. See [optional gallery settings](DEVELOPMENT.md#gallery-settings) for sizing or placing groups between paragraphs.

To replace the profile portrait, upload the new image and change `avatar` in `profile.json` to its `/assets/images/...` path. Update `avatar_alt` to describe it.

## Add a news update

Copy an entry in [`_data/news.yml`](../_data/news.yml), then change its text:

```yaml
- date: "2026-09"
  title: "A short update about my work."
  url: /research/
```

Keep the date in `YYYY-MM` format and in quotes. Omit the `url` line for an update without a link. The three newest entries appear on the homepage automatically.

## Update the CV

**By default, the PDF updates automatically when the website publishes.** Edit `profile.json`, `cv.json`, or the project summaries, and update the `updated` date in `cv.json`. Open the downloaded PDF afterward to check its pages.

To use a PDF you prepared yourself:

1. Use **Add file → Create new file** at the repository’s top level to create `cv-source/.gitkeep`. Leave its contents empty and save it. This creates the folder if it does not already exist.
2. Open `cv-source/`, choose **Add file → Upload files**, and upload your PDF as `manual.pdf`.
3. In [`_data/cv_pdf.json`](../_data/cv_pdf.json), change `"mode": "auto"` to `"mode": "manual"`, then save.

Leave the other settings unchanged. To replace this PDF later, upload a new `manual.pdf` to the same folder. Change the mode back to `auto` to resume automatic generation. The CV page itself always uses the website data; uploading a PDF changes the download only. Uploaded files are public in this repository.

## If something goes wrong

- **The page has not changed:** wait for Actions to finish, refresh the site, and check the entry’s date and `published` setting.
- **A check fails:** open the failed run in Actions. Check recent edits for missing quotes or commas, incorrect indentation, or a misspelled image path. Fix the file and save again; publishing retries automatically.
- **You need the old text:** open the file’s **History**, find the earlier version, and copy the original text back through the editor.

The `_theme/` and `scripts/` folders contain the website’s machinery. Everyday content updates use the files above. For changes to the menu, page layout, or hosting, use the [maintenance guide](DEVELOPMENT.md).
