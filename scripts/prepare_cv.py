#!/usr/bin/env python3
"""Publish the selected CV at the shared download URL; never alter the manual source."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def settings(root):
    config = json.loads((root / '_data/cv_pdf.json').read_text())
    if not isinstance(config, dict):
        raise ValueError('_data/cv_pdf.json must contain a JSON object.')
    if config.get('mode') not in ('auto', 'manual'):
        raise ValueError('_data/cv_pdf.json: mode must be "auto" or "manual".')
    public = config.get('published_file', '')
    if not isinstance(public, str) or not public.startswith('/files/') or not public.endswith('.pdf'):
        raise ValueError('published_file must be a /files/...pdf URL.')
    output = (root / public.lstrip('/')).resolve()
    if not output.is_relative_to((root / 'files').resolve()):
        raise ValueError('published_file must stay inside files/.')
    manual = config.get('manual_file', '')
    if not isinstance(manual, str) or not manual.startswith('cv-source/') or not manual.endswith('.pdf'):
        raise ValueError('manual_file must be a cv-source/...pdf path.')
    source = (root / manual).resolve()
    if not source.is_relative_to((root / 'cv-source').resolve()):
        raise ValueError('manual_file must stay inside cv-source/.')
    if source == output:
        raise ValueError('Manual source and published PDF must be separate files.')
    return config, source, output


def prepare(root=ROOT):
    config, manual, output = settings(root)
    if config['mode'] == 'manual':
        source = manual
        if not source.is_file():
            raise ValueError(f'Manual CV not found: {config["manual_file"]}. Add your compiled PDF there, or set mode to "auto".')
    else:
        source = root / '.cache/generated-cv.pdf'
        try:
            subprocess.run([sys.executable, str(root / 'scripts/build_cv.py')], check=True)
        except subprocess.CalledProcessError as error:
            raise ValueError('Automatic CV generation failed. Run npm run setup:cv if dependencies are missing; then check the error above.') from error
    content = source.read_bytes()
    if not content.startswith(b'%PDF-'):
        raise ValueError(f'{source.name} is not a PDF file. Supply a compiled PDF, not a .tex source.')
    output.parent.mkdir(parents=True, exist_ok=True)
    # Replace only after generation and basic validation succeed.
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix='.cv-', delete=False, suffix='.tmp') as tmp:
        temporary = Path(tmp.name)
        tmp.write(content)
    try:
        temporary.chmod(0o644)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'CV mode: {config["mode"]}; published PDF: {config["published_file"]}')


if __name__ == '__main__':
    try:
        prepare()
    except (ValueError, OSError) as error:
        print(f'CV preparation failed: {error}', file=sys.stderr)
        sys.exit(1)
