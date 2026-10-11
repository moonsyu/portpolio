"""Build both current HTML portfolio PDFs as one section per widescreen page."""
from argparse import ArgumentParser
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=['all', 'full', 'web-app'], default='all')
    parser.add_argument('--node', default=os.environ.get('PDF_NODE', 'node'))
    parser.add_argument('--node-modules', type=Path)
    parser.add_argument('--browser-executable', type=Path)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--work-dir', type=Path)
    args = parser.parse_args()
    env = os.environ.copy()
    env['PDF_PYTHON'] = sys.executable
    if args.node_modules:
        env['NODE_PATH'] = str(args.node_modules.resolve())
    command = [args.node, str(ROOT / 'scripts/build_pdf.cjs'), '--variant', args.variant]
    for option in ['browser_executable', 'output_dir', 'work_dir']:
        value = getattr(args, option)
        if value:
            command.extend(['--' + option.replace('_', '-'), str(value.resolve())])
    subprocess.run(command, cwd=ROOT, env=env, check=True)
