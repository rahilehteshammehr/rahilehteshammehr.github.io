# Academic Pages source

- Repository: https://github.com/academicpages/academicpages.github.io
- Imported commit: `3d28cd27d0551b3d9dd8132f207538355fbbc7cc`
- Retrieved: 19 September 2026
- License: MIT, retained at `LICENSE`

The complete `_sass`, `_includes`, and `_layouts` directories were imported, including required sources under `_sass/vendor/`. Trailing whitespace and excess final blank lines were normalized for the source release. Custom styling lives in `_rahil.scss`; `assets/css/main.scss` adds that partial after the upstream styles. The upstream default/single layouts and head, masthead, author-profile, and footer includes have been tailored. A project layout, icon include, and project-entry include are new.

The site uses the Academic Pages Sass source and Jekyll/Liquid structure, with local content collections. It does not load the prototype's compiled CSS. Unused upstream demo pages, publication entries, sample personal data, JavaScript bundles, analytics, comments, and third-party fonts were not enabled. The local JavaScript handles theme, mobile navigation, printing, and the photo carousel.

For maintenance, compare upstream updates to this pinned commit, especially when updating a customized include. Do not overwrite `_data`, `_pages`, `_projects`, `_sass/_rahil.scss`, or the local scripts with demo files. This is a personal implementation; changes do not need to be submitted to the upstream template.
