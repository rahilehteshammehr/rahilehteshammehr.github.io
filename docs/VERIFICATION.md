# Release verification

The source repository contains the production website, content, required Sass
dependencies, editing templates, validation scripts, and upstream license.
Original source documents, prototypes, research downloads, local design/review
artifacts, caches, and installed dependencies are excluded from Git.

## Source release checks — 19 September 2026

A clean export of the staged repository passed root and `/rahilwebsite` builds:
12 HTML pages and 201 local references/fragments in each, including PDF, sitemap,
and source exclusions. The export used the installed local Ruby/Python/Node
dependencies, without relying on untracked website source files. All 7 CV tests,
497 site DOM assertions, and 22 gallery assertions passed. Local JavaScript
syntax and staged whitespace checks also passed.

## Reproduce locally

With Ruby 3.2+ (3.3 recommended), Bundler, Python 3, and Node/npm installed:

```sh
npm run setup
npm run setup:cv
npm run validate
npm run test:cv
```

Optional DOM interaction checks:

```sh
npm install --prefix .cache/qa --save-exact jsdom@30.0.1
NODE_PATH="$PWD/.cache/qa/node_modules" node scripts/check_ui.cjs
NODE_PATH="$PWD/.cache/qa/node_modules" node scripts/check_gallery.cjs
```

The site checker crawls generated HTML, local links, fragments, the selected CV,
the sitemap, and source-file exclusions. CV tests cover automatic/manual
selection, invalid settings, missing input, and source preservation. DOM tests
cover themes, navigation, printing, and gallery interactions.

## GitHub validation and deployment

Pushes to `main` and pull requests build and validate the website on Linux using
Ruby 3.3 and Python 3.12. Deployment runs only when the repository has GitHub
Pages configured with GitHub Actions as its publishing source. The private
transfer repository can therefore validate the code without publishing a site.

## Review limits

Automated and DOM checks do not establish browser rendering, native dialog focus
containment, physical touch behavior, or printed browser layout. Review desktop
and mobile layouts, both themes, navigation, galleries, and the CV download in
a real browser before announcing the final site. Earlier browser launches on
the authoring computer were blocked by macOS permissions.

Outstanding content confirmations are recorded in [CONTENT.md](CONTENT.md).
The unfinished research news announcement was removed instead of publishing
its placeholder supervisor and unconfirmed date.
