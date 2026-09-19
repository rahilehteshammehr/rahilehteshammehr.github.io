#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Prefer the project-local Ruby when present, then Homebrew, then PATH.
if [[ -x .cache/ruby/arm64/bin/ruby ]]; then
  export PATH="$PWD/.cache/ruby/arm64/bin:$PATH"
  export DYLD_LIBRARY_PATH="$PWD/.cache/ruby/arm64/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
  export RUBYLIB="$PWD/.cache/ruby/arm64/lib/ruby/3.3.0:$PWD/.cache/ruby/arm64/lib/ruby/3.3.0/arm64-darwin23${RUBYLIB:+:$RUBYLIB}"
  export GEM_HOME="$PWD/.cache/ruby-gems"
  export GEM_PATH="$GEM_HOME:$PWD/.cache/ruby/arm64/lib/ruby/gems/3.3.0"
  export GEM_SPEC_CACHE="$PWD/.cache/gem-specs"
  export BUNDLE_USER_HOME="$PWD/.cache/bundle"
  bundle_cmd=(ruby .cache/ruby/arm64/bin/bundle)
elif [[ -x /opt/homebrew/opt/ruby@3.3/bin/ruby ]]; then
  export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
  bundle_cmd=(bundle)
else
  bundle_cmd=(bundle)
fi
if ! ruby -e 'exit Gem::Version.new(RUBY_VERSION) >= Gem::Version.new("3.2") ? 0 : 1'; then
  echo 'Ruby 3.2+ is required. Install Ruby 3.3 and Bundler, then run npm run setup.' >&2
  exit 1
fi
if [[ "${1:-}" == install ]]; then
  "${bundle_cmd[@]}" config set --local path vendor/bundle
  exec "${bundle_cmd[@]}" install
fi
if [[ "${1:-}" == build || "${1:-}" == serve ]]; then
  bash scripts/cv.sh
fi
exec "${bundle_cmd[@]}" exec jekyll "$@"
