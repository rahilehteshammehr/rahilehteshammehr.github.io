# Edit, preview, and publish the website

Work on your computer, check the result in your browser, then publish when you are ready. **Saving a file changes your local preview. Pushing your changes to GitHub starts the update to the public website.**

Everything you need for this workflow is below. After the first setup, follow steps **2 → 3 → 4 → 5** each time.

[1. First setup](#1-first-setup) · [2. Open the preview](#2-open-the-preview) · [3. Make your changes](#3-make-your-changes) · [4. Check the result](#4-check-the-result) · [5. Publish](#5-publish) · [Troubleshooting](#if-something-goes-wrong)

## 1. First setup

Do this once on each computer. If the website already runs on your computer, go to step 2.

### Get a local copy

You need Git, Node/npm, Ruby 3.3 with Bundler, Python 3.12, and a code editor installed. These are the tools that run the existing website; a helper can handle this one-time installation. You do not need to learn their programming languages to edit the content.

If you already have the website folder, open it in your editor. Otherwise, open your repository on GitHub, click **Code → HTTPS**, and copy its address. In a terminal, run the following, replacing `YOUR_REPOSITORY_URL` with that address:

```sh
git clone YOUR_REPOSITORY_URL website
cd website
```

This downloads the repository into a folder called `website`. Open that folder in your editor. Use the repository you will publish from, which may be a copy on your own GitHub account.

### Prepare the website

Open a terminal **inside the website folder**—the folder containing `package.json` and `README.md`. In Visual Studio Code, open the folder first, then choose **Terminal → New Terminal**. Run these commands one at a time, waiting for each to finish:

```sh
npm run setup
npm run setup:cv
```

The first installs the website dependencies; the second installs the PDF generator. If a command fails, fix that error before continuing. No `npm install` is needed for the normal website workflow.

### Enable publishing on GitHub

Do this once for the repository you will publish from:

1. Open the repository on GitHub and go to **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Go to **Actions → Build and deploy website → Run workflow**, choose `main`, and run it.
4. When both **build** and **deploy** finish successfully, find your website address in **Settings → Pages**. Bookmark it.

You need permission to change repository settings and push changes. Publishing uses the `main` branch. The workflow handles the website address and repository subpath automatically; no domain or address changes in the code are needed for GitHub Pages.

## 2. Open the preview

Open your website folder in the editor and open a terminal in that folder. Start each editing session by getting any updates from GitHub, then start the preview:

```sh
git switch main
git pull --ff-only
npm run dev
```

If you have unfinished changes from an earlier session, finish those first; do not discard them to make the pull work. If Git reports an error, stop and see troubleshooting below.

Wait until the terminal says the server is running, then open **<http://127.0.0.1:4000/>** in your browser. This is your local preview, visible only on your computer.

**Leave this terminal running while you edit.** Save a file in the editor, wait for the terminal to report that the site regenerated, then refresh the browser. To stop the preview, click in its terminal and press **Control-C**. You can start it again with `npm run dev`.

For commands during editing, open a second terminal in the same folder. Only run one preview server at a time. Restart the preview after changing `_config.yml` or the CV download mode.

## 3. Make your changes

Open the appropriate file **in your local editor**, change the text, and save. The paths below are inside your website folder.

| What you want to change | File or folder |
| --- | --- |
| Introduction, interests, highlight, contact links, portrait, sidebar role | `_data/profile.json` |
| Education, awards, teaching, skills, courses, service, CV update date | `_data/cv.json` |
| Research/project descriptions | The matching file in `_projects/` |
| Beyond Physics stories | The matching file in `_posts/` |
| Homepage news | `_data/news.yml` |
| Photographs | `assets/images/` |
| Automatic or manually supplied PDF CV | `_data/cv_pdf.json` |

In `.json` files, change the text between double quotes. Keep commas between entries, with no comma after the last entry. To put a quotation mark inside text, write `\"`. In `.md` and `.yml` files, preserve indentation and use spaces, not tabs.

In stories and projects, keep the two `---` lines: settings go between them, and the main text goes below the second line. Use `## Heading`, `**bold text**`, `- list item`, and `[link text](https://example.com)` for simple formatting. The settings already provide the page title.

Expand the instructions you need, then continue to step 4.

<details>
<summary><strong>Update the introduction or highlighted message</strong></summary>

Edit the relevant text in `_data/profile.json`. Set `highlight` to `""` to hide the highlighted homepage message. When graduation details change, update the education entry in `_data/cv.json` and the graduation labels in `_data/profile.json`.

</details>

<details>
<summary><strong>Add a story or research project</strong></summary>

In a second terminal, run one of these commands, replacing the title:

```sh
npm run new:post -- "My new story"
npm run new:project -- "My new project"
```

The command prints the new filename. Open it in your editor and replace the example text. Add `--photos` at the end of either command to include an example photo gallery. Existing files are never overwritten.

For projects, use exactly `Undergraduate research` or `Academic project` as the category. Smaller `order` numbers appear first. The summary also appears in the automatic PDF CV. Optional `supervisor` and `supervisor_url` fields can be copied from an existing project.

**New entries start as drafts.** To preview them, stop the regular preview with Control-C and run:

```sh
npm run dev:drafts
```

Open the same local address. This preview includes unpublished and future-dated entries. Remove `published: false` from the entry when ready to publish it. A draft is hidden on the website, but its source file is visible if pushed to this public repository.

A story's filename starts with its publication date, such as `2026-09-19-my-story.md`. Future-dated stories stay hidden in normal builds until a build on or after that date; they do not publish on a timer. To choose the date when creating a story, add `--date YYYY-MM-DD`. Keep existing filenames when changing titles so old links continue to work.

Stories and projects appear in their lists automatically. They do not need menu changes.

</details>

<details>
<summary><strong>Add photographs or replace the portrait</strong></summary>

Copy the image files into `assets/images/` on your computer. Use simple names such as `chess-team.jpg`. In a story or project, add this above the closing `---`:

```yaml
photos:
  - src: /assets/images/chess-team.jpg
    alt: "The chess team beside the tournament boards."
    caption: "Our team at the tournament."
```

Repeat the three lines starting with `- src` for each photo. Match the filenames exactly, including capitalization. `alt` describes what is visible for screen readers; `caption` is shown below the photo. For a credited image, add `credit: "Photographer or organization"` and `source: "https://example.com/original-page"` below its caption, at the same indentation.

Photos appear below the story automatically and open in a larger viewer when clicked. Resize very large camera images before adding them.

For the profile portrait, change `avatar` in `_data/profile.json` to your new `/assets/images/...` path and update `avatar_alt` to describe it.

Optional gallery sizing settings go above the closing `---` too:

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

A photo can have `span: full` or its own `fit`. Optional numeric image `width` and `height` reserve loading space. To place a group between paragraphs, give its photos `group: tournament` and insert this in the body:

```liquid
{% include post-gallery.html group='tournament' label='Tournament photographs' %}
```

An explicit gallery disables the automatic end gallery, so include every desired group. Include parameters can override page defaults, for example `columns=3 fit='square'`. The existing chess story demonstrates this.

</details>

<details>
<summary><strong>Add a homepage news update</strong></summary>

Copy an entry in `_data/news.yml` and change its text:

```yaml
- date: "2026-09"
  title: "A short update about my work."
  url: /research/
```

Keep the date in `YYYY-MM` format and in quotes. Omit `url` for an update without a link. The three newest entries appear automatically.

</details>

<details>
<summary><strong>Update or replace the downloadable CV</strong></summary>

By default, the PDF is generated from your profile, CV records, and project summaries. Edit those source files and the `updated` date in `_data/cv.json`. While previewing, run this in a second terminal to refresh the PDF:

```sh
npm run cv
```

Refresh the preview and open its **Download CV** link. The PDF also refreshes whenever you start the preview, validate, or publish.

To use a PDF you prepared yourself:

1. Create a folder named `cv-source` inside the website folder if it does not exist.
2. Copy your PDF into it and name the file `manual.pdf`.
3. In `_data/cv_pdf.json`, change `"mode": "auto"` to `"mode": "manual"`. Leave the other settings unchanged.
4. Restart the preview and check **Download CV**. Include both the PDF and the setting when publishing in step 5.

Replace `cv-source/manual.pdf` to update your manual CV. Change the mode back to `auto` to resume automatic generation. The web CV page always uses the website data; this setting changes only the downloaded PDF. Do not edit the generated PDF in `files/` directly. Files you push are public in this repository.

</details>

<details>
<summary><strong>Add a standalone page or change the menu</strong></summary>

Run `npm run new:page -- "My new page"` in a second terminal and edit the created file. Preview drafts as described above and remove `published: false` when ready. Every standalone page needs a unique `permalink`.

To add it to the menu, add a record to `_data/navigation.yml` with `title`, `url`, and `key`. Set the page's `nav` to the same key so its menu item is highlighted. Main page text and composition live in `_pages/`; the site title and search description are in `_config.yml`.

For internal links and inline images, use this form so links also work when the website is under a repository subpath:

```liquid
[Research]({{ '/research/' | relative_url }})
![Description]({{ '/assets/images/photo.jpg' | relative_url }})
```

</details>

## 4. Check the result

1. Review your changed pages in the local browser. Try a narrow window and both color themes. Open any new images and download the CV if you changed it.
2. Remove `published: false` from entries you want to publish and check story dates.
3. Stop the preview with **Control-C**, then run:

```sh
npm run validate
```

Wait for the final **PASS** message. This builds the normal public version and checks pages, local links, images, the PDF, and the sitemap. It does **not** publish anything. If it fails, fix the error before continuing.

To see exactly which entries the public build includes, especially after previewing drafts, run `npm run dev` again and refresh the browser. Check your pages, then stop the preview with Control-C before publishing. Automated checks do not check factual accuracy or visual appearance.

## 5. Publish

When you are happy with the preview and validation passes, run these commands **one at a time** in the website folder:

```sh
git status
```

Read the list of changed files. It should contain the edits, images, and any updated CV you intend to publish. If it includes something unexpected, resolve that before continuing. Then:

```sh
git add -A
git commit -m "Update website content"
git push origin main
```

You can replace `Update website content` with a short description of your update. `git add` selects the changes, `git commit` saves a version on your computer, and **`git push` sends it to GitHub and starts publishing**. Run this from `main`, as selected in step 2. If any command fails, stop and fix the error before running the next one.

Finally:

1. Open your repository on GitHub and select **Actions**.
2. Open the latest **Build and deploy website** run for your update. Wait for both **build** and **deploy** to succeed.
3. Open your bookmarked public website address from **Settings → Pages**, refresh, and check the changed pages.

You do not need to upload `_site/` or run a separate deployment command. If **deploy** is skipped, complete the one-time Pages setup in step 1; a successful build alone does not mean the public website changed. Once deployment finishes, you can close the editor and terminal—the public website stays online.

## If something goes wrong

| Problem | What to do |
| --- | --- |
| A command is not found | The corresponding tool is missing or unavailable in the terminal. Complete the one-time installation, reopen the terminal, and retry. |
| npm cannot find `package.json` | Open a terminal in the website folder, not its parent folder. |
| Preview says the address is already in use | Stop the other preview terminal with Control-C. Only one server can use port 4000. |
| Local changes do not appear | Save the source file, check the preview terminal for errors, and refresh. For drafts, use `npm run dev:drafts`; restart after changing `_config.yml` or CV mode. |
| A project is missing | Check `published`, its exact category, and any errors in the terminal. |
| A photo is missing | Match its path and capitalization to the actual file, then run `npm run validate`. |
| The PDF looks old | Run `npm run cv`, refresh, and reopen the PDF. |
| Git asks who you are when committing | Run `git config user.name "Your Name"` and `git config user.email "Your GitHub email"` with your details, then retry the commit. Use your GitHub-provided no-reply email if preferred. |
| GitHub sign-in or push authentication fails | Authenticate Git using your GitHub account. If GitHub CLI is installed, run `gh auth login`, then `gh auth setup-git`, and retry. Your GitHub account password is not a Git HTTPS password. |
| A pull or push is rejected | Keep your changes. If GitHub has newer commits, commit your finished local edits, run `git pull --rebase origin main`, and retry the push. If conflicts are reported, get help resolving them; do not force-push. |
| The repository requires a pull request | Before committing your update, create a branch with `git switch -c content-update`, then add and commit as above and run `git push -u origin content-update`. Open a pull request on GitHub and merge after checks pass. Use a new branch name for another update. Publishing starts when it reaches `main`. |
| The public site has not changed | Check the latest Actions run: both build and deploy must succeed. Refresh the public address, not the local preview. |
| Actions reports a failure | Open the failed step, correct the reported problem locally, validate, then commit and push again. |
| You need earlier text | On GitHub, open the file's History, find the earlier version, and copy the text back into your local file. Preview and publish normally. |

<details>
<summary><strong>Optional: quick edits directly on GitHub</strong></summary>

For a small text correction away from your computer, open the file on GitHub, click the pencil icon, and choose **Commit changes** to save to `main`. This starts the same publishing workflow, but you will not have a local preview before saving. Check Actions and the public site afterward. Next time you edit locally, use the pull command in step 2 to bring that change onto your computer.

</details>

<details>
<summary><strong>Technical maintenance and credits</strong></summary>

Everyday editing uses the flow above. The remaining folders contain the website machinery:

- `_theme/`: layouts, shared includes, and styles. Site-specific styling is in `_theme/styles/_rahil.scss`; `assets/css/main.scss` loads the base styles first.
- `scripts/`: build helpers, checks, and three content templates.
- `assets/js/`: theme switching, navigation, printing, and photo viewing.
- `.github/workflows/pages.yml`: automated checks and publishing. Pull requests build and check without deploying.
- `_site/`, `.cache/`, and `vendor/`: generated output or installed dependencies; ignored by Git. Do not edit generated files.

The source folders `_theme/`, `scripts/`, `docs/`, and `cv-source/` are excluded from the built website; tracked files are still visible in this public repository. For another host, set `url` and `baseurl` in `_config.yml` and deploy the generated `_site/` directory.

Additional checks for code changes:

```sh
npm run test:cv
npm install --prefix .cache/qa --save-exact jsdom@30.0.1
NODE_PATH="$PWD/.cache/qa/node_modules" node scripts/check_ui.cjs
NODE_PATH="$PWD/.cache/qa/node_modules" node scripts/check_gallery.cjs
```

The interaction checks use jsdom; they do not verify browser rendering. Run them after building the normal site. The CV tests check automatic/manual selection and source preservation.

The design derives from [Academic Pages](https://github.com/academicpages/academicpages.github.io/tree/3d28cd27d0551b3d9dd8132f207538355fbbc7cc), imported at commit `3d28cd27d0551b3d9dd8132f207538355fbbc7cc`. Its MIT license is retained in `LICENSE`. Only used templates and Sass imports remain, including required Breakpoint and Susy sources under `_theme/styles/vendor/`. Compare upstream updates selectively rather than replacing the customized theme. No analytics, remote fonts, or comment service is configured.

Photographs link to their source pages in the chess story. `docs/chess-photo-sources.json` retains the original asset URLs.

</details>
