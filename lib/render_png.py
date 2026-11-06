#!/usr/bin/env python3
"""render_png.py <file.html> <out.png> [width=1850] [scale=2]

Chụp TOÀN TRANG một file HTML bằng Chrome headless: tự đo chiều cao trang rồi chụp đúng khổ.
Chạy được trên macOS / Windows / Linux. Chrome headless trên macOS hay không tự thoát sau khi chụp,
nên mọi lệnh đều có giới hạn thời gian (timeout) thay vì chờ vô hạn.
"""
import os
import re
import subprocess
import sys
import tempfile

CANDIDATES = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
]


def chrome():
    for c in CANDIDATES:
        if os.path.exists(c):
            return c
    sys.exit('Không tìm thấy Chrome. Sửa CANDIDATES trong render_png.py.')


def run(args, timeout=25):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired as e:  # Chrome đã chụp xong nhưng không thoát: bình thường trên macOS
        out = e.stdout or ''
        return out.decode('utf-8', 'ignore') if isinstance(out, bytes) else out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1850
    scale = sys.argv[4] if len(sys.argv) > 4 else '2'
    profile = os.path.join(tempfile.gettempdir(), 'archkit-chrome-profile')  # không đụng Chrome đang mở
    base = [chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
            '--user-data-dir=' + profile, '--virtual-time-budget=5000']
    url = lambda p: 'file:///' + p.replace('\\', '/').lstrip('/')

    # 1) đo chiều cao bằng bản sao tạm có gắn script đo
    probe = os.path.join(os.path.dirname(src), '.probe-' + os.path.basename(src))
    html = open(src, encoding='utf-8').read().replace(
        '</body>',
        '<script>window.addEventListener("load",function(){document.documentElement.setAttribute('
        '"data-h",Math.ceil(document.body.getBoundingClientRect().height)+8)})</script></body>')
    open(probe, 'w', encoding='utf-8').write(html)
    try:
        dom = run(base + ['--window-size=%d,900' % width, '--dump-dom', url(probe)])
    finally:
        os.remove(probe)
    m = re.search(r'data-h="(\d+)"', dom or '')
    height = int(m.group(1)) if m else 1400

    # 2) chụp
    if os.path.exists(out):
        os.remove(out)
    run(base + ['--force-device-scale-factor=' + scale, '--window-size=%d,%d' % (width, height),
                '--screenshot=' + out, url(src)])
    print('%s  %dx%d @%sx  %s' % (os.path.basename(out), width, height, scale,
                                   'OK' if os.path.exists(out) else 'FAIL'))


if __name__ == '__main__':
    main()
