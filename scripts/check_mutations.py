"""Jalankan tiga mutasi terisolasi dan simpan keluaran pytest sebagai bukti."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src' / 'pricing.py'
EVIDENCE = ROOT / 'bukti'
MUTATIONS = [
    ('01-tanpa-diskon', 'return subtotal * (1 - MEMBER_DISCOUNT_RATE)',
     'return subtotal', 2),
    ('02-pajak-12-persen', 'TAX_RATE = 0.11', 'TAX_RATE = 0.12', 4),
    ('03-tanpa-validasi-kuantitas',
     '    if quantity <= 0:\n        raise ValueError("quantity must be positive")\n', '', 3),
]


def run_case(name, source, expected_failures):
    # Setiap kasus mendapat sumber, test, dan cache Python yang terpisah.
    with tempfile.TemporaryDirectory(prefix='pricing-mutation-') as directory:
        workspace = Path(directory)
        (workspace / 'src').mkdir()
        (workspace / 'src' / 'pricing.py').write_text(source, encoding='utf-8')
        shutil.copytree(ROOT / 'tests', workspace / 'tests',
                        ignore=shutil.ignore_patterns('__pycache__'))
        env = dict(os.environ, PYTHONPATH=str(workspace / 'src'),
                   PYTHONDONTWRITEBYTECODE='1', PYTEST_ADDOPTS='',
                   PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', NO_COLOR='1')
        command = [sys.executable, '-m', 'pytest', '-v', '--tb=short',
                   '--color=no', '-p', 'no:cacheprovider', 'tests']
        result = subprocess.run(command, cwd=workspace, env=env,
                                text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    failures = [line for line in result.stdout.splitlines()
                if line.startswith('FAILED tests/')]
    header = (f'Kasus: {name}\nPython: {sys.version.split()[0]}\n'
              f'SHA256 sumber kasus: {hashlib.sha256(source.encode()).hexdigest()}\n'
              'Perintah: python -m pytest -v --tb=short --color=no '
              '-p no:cacheprovider tests\n'
              f'Exit code: {result.returncode}\n\n')
    (EVIDENCE / f'{name}.txt').write_text(header + result.stdout, encoding='utf-8')
    expected_exit = 1 if expected_failures else 0
    if result.returncode != expected_exit or len(failures) != expected_failures:
        raise RuntimeError(f'{name}: hasil tidak sesuai; lihat log bukti.')
    print(f'{name}: {len(failures)} gagal; exit code {result.returncode}')


def main():
    EVIDENCE.mkdir(exist_ok=True)
    original = SOURCE.read_text(encoding='utf-8')
    run_case('00-implementasi-benar', original, 0)
    for name, old, new, failures in MUTATIONS:
        if original.count(old) != 1:
            raise RuntimeError(f'{name}: lokasi mutasi tidak unik.')
        run_case(name, original.replace(old, new, 1), failures)
    run_case('04-implementasi-benar-setelah-mutasi', original, 0)
    if SOURCE.read_text(encoding='utf-8') != original:
        raise RuntimeError('Sumber proyek berubah selama pengujian.')


if __name__ == '__main__':
    main()
