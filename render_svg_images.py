import subprocess, os
from PIL import Image, ImageChops

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

edge_exe = None
for p in edge_paths:
    if os.path.exists(p):
        edge_exe = p
        break

print("Using Edge executable for high-DPI rendering:", edge_exe)

svg_configs = [
    ('figure1_pipeline_diagram.svg', 'figure1_pipeline_diagram.png', 2400, 1200),
    ('fig2_xg_scatter.svg', 'fig2_xg_scatter.png', 2000, 1500),
    ('fig3_team_market_values.svg', 'fig3_team_market_values.png', 2000, 1500)
]

for svg_file, png_out, win_w, win_h in svg_configs:
    abs_svg = os.path.abspath(svg_file).replace('\\', '/')
    abs_png = os.path.abspath(png_out)
    
    cmd = [
        edge_exe,
        '--headless',
        '--disable-gpu',
        '--hide-scrollbars',
        '--force-device-scale-factor=2.0',
        f'--window-size={win_w},{win_h}',
        f'--screenshot={abs_png}',
        f'file:///{abs_svg}'
    ]
    subprocess.run(cmd, check=True)
    
    # Auto-crop surrounding white margins cleanly
    img = Image.open(abs_png).convert('RGB')
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        left, upper, right, lower = bbox
        left = max(0, left - 15)
        upper = max(0, upper - 15)
        right = min(img.width, right + 15)
        lower = min(img.height, lower + 15)
        cropped = img.crop((left, upper, right, lower))
        cropped.save(abs_png)
        print(f"[SUCCESS] {svg_file} -> {png_out} (High-DPI Resolution: {cropped.size[0]}x{cropped.size[1]})")
    else:
        print(f"[SUCCESS] {svg_file} -> {png_out} (Full Resolution: {img.size[0]}x{img.size[1]})")
