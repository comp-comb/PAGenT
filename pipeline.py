import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd
import os
import numpy as np
from matplotlib.patches import Circle
from PIL import Image

# -----------------------------------------------------------------------------
# 1) XML → CSV
# -----------------------------------------------------------------------------
def parse_data_to_CSV(xml_dir, file_begins_with, file_ends_with, output_csv):
    xml_files = sorted([
        f for f in os.listdir(xml_dir)
        if f.startswith(file_begins_with) and f.endswith(file_ends_with)
    ])
    rows = []
    for cid, fname in enumerate(xml_files):
        tree = ET.parse(os.path.join(xml_dir, fname))
        dp = tree.getroot().find('.//data_particle')
        if dp is None:
            continue
        for part in dp.findall('particle'):
            pid = part.get('ID')
            r = float(part.find('radius').text)
            x, y, z = map(float, part.find('position').text.split(','))
            rows.append([cid, pid, r, x, y, z])
    df = pd.DataFrame(rows, columns=['Cluster','Particle','Radius','x','y','z'])
    df.to_csv(output_csv, index=False)
    return df

# -----------------------------------------------------------------------------
# 2) Mask generation (black background + white circle, exact 1024×1024)
# -----------------------------------------------------------------------------
def plot_particle_mask(cluster_df, cluster_id, mask_dir):
    w, h, dpi = 1024, 1024, 96
    out = os.path.join(mask_dir, 'particle')
    os.makedirs(out, exist_ok=True)

    for idx, row in enumerate(cluster_df.itertuples(), start=1):
        fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        circ = Circle((row.x, row.y), row.Radius, color='white', fill=True)
        ax.add_patch(circ)
        ax.set_xlim(-w/2, w/2)
        ax.set_ylim(-h/2, h/2)
        ax.set_aspect('equal')
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        fn = os.path.join(out, f'mask_{cluster_id:06d}_{idx:06d}.png')
        fig.savefig(fn, dpi=dpi, bbox_inches=None, pad_inches=0,
                    facecolor=fig.get_facecolor())
        plt.close(fig)

def plot_clusters_mask(cluster_df, cluster_id, mask_dir):
    w, h, dpi = 1024, 1024, 96
    out = os.path.join(mask_dir, 'cluster')
    os.makedirs(out, exist_ok=True)

    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    for row in cluster_df.itertuples():
        circ = Circle((row.x, row.y), row.Radius, color='white', fill=True)
        ax.add_patch(circ)
    ax.set_xlim(-w/2, w/2)
    ax.set_ylim(-h/2, h/2)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    fn = os.path.join(out, f'mask_{cluster_id:06d}.png')
    fig.savefig(fn, dpi=dpi, bbox_inches=None, pad_inches=0,
                facecolor=fig.get_facecolor())
    plt.close(fig)

# -----------------------------------------------------------------------------
# 3) Noise & TEM background
# -----------------------------------------------------------------------------
def add_gauss_noise(image, gaussian_std=0.09):
    noise = np.random.normal(scale=gaussian_std, size=image.shape)
    return np.clip(image + noise, 0, 1)

def add_poisson_noise(image, intensity=2):
    pn = np.random.poisson(image / intensity) * intensity
    return np.clip(image + pn, 0, 1)

def add_combined_noise(image, poisson_intensity=2, gaussian_std=0.09):
    tmp = add_poisson_noise(image, intensity=poisson_intensity)
    return add_gauss_noise(tmp, gaussian_std=gaussian_std)

def generate_hrtem_noise_image(width=1024, height=1024, mean=128, std=15):
    rnd = np.random.normal(loc=mean, scale=std, size=(height, width))
    return np.clip(rnd, 0, 255).astype(np.uint8)

# -----------------------------------------------------------------------------
# 4) Cluster rendering + multiple noises + optional TEM background + custom color
# -----------------------------------------------------------------------------
def plot_clusters(cluster_df, cluster_id,
                  image_dir, noisyoutput_dir,
                  noise_types=['gauss'],
                  tem_style=False, tem_mean=128, tem_std=15,
                  tem_color=(0.045,0.045,0.045,0.3)):
    w, h, dpi = 1024, 1024, 96

    # Draw base: optional TEM‐style background
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    if tem_style:
        bg = generate_hrtem_noise_image(width=w, height=h,
                                        mean=tem_mean, std=tem_std)
        ax.imshow(bg, cmap='gray', origin='lower',
                  extent=[-w/2, w/2, -h/2, h/2],
                  interpolation='nearest', aspect='auto')

    # Draw semi‐transparent circles using provided color
    for row in cluster_df.itertuples():
        circ = Circle((row.x, row.y), row.Radius,
                      color=tem_color, fill=True, linewidth=0)
        ax.add_patch(circ)

    ax.set_xlim(-w/2, w/2)
    ax.set_ylim(-h/2, h/2)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(noisyoutput_dir, exist_ok=True)

    # Save the base (TEM + circles)
    base_fn = os.path.join(image_dir, f'image_{cluster_id:06d}.png')
    fig.savefig(base_fn, dpi=dpi, bbox_inches=None, pad_inches=0)
    plt.close(fig)

    base_img = plt.imread(base_fn)
    # Apply each noise in the list
    for nt in noise_types:
        if nt == 'gauss':
            out = add_gauss_noise(base_img)
        elif nt == 'poisson':
            out = add_poisson_noise(base_img)
        elif nt == 'combined':
            out = add_combined_noise(base_img)
        elif nt == 'tem':
            # re‐overlay TEM background over circles
            bg = generate_hrtem_noise_image(width=w, height=h,
                                            mean=tem_mean, std=tem_std) / 255.0
            bg_rgb = np.dstack([bg]*3)
            mask = base_img[...,0] > 0
            out = bg_rgb.copy()
            out[mask] = 1.0
        else:
            raise ValueError(f"Unknown noise type '{nt}'")

        noisy_fn = os.path.join(noisyoutput_dir,
                                f'image_{cluster_id:06d}_{nt}.png')
        plt.imsave(noisy_fn, out)
        print(f"Rendered cluster {cluster_id:06d} with {nt}")

# -----------------------------------------------------------------------------
# 5) Main pipeline
# -----------------------------------------------------------------------------
def main(xml_dir, file_begins_with, file_ends_with,
         output_csv, mask_dir, image_dir, noisyoutput_dir,
         mask_type='both',
         noise_types=['gauss'],
         tem_style=False, tem_mean=128, tem_std=15,
         tem_color=(0.045,0.045,0.045,0.3)):

    df = parse_data_to_CSV(xml_dir, file_begins_with, file_ends_with, output_csv)

    for cid in df['Cluster'].unique():
        sub = df[df['Cluster'] == cid]
        if sub.empty:
            continue

        # Generate masks
        if mask_type in ('particle','both'):
            plot_particle_mask(sub, cid, mask_dir)
        if mask_type in ('cluster','both'):
            plot_clusters_mask(sub, cid, mask_dir)

        # Render TEM & noise
        plt.rcdefaults()
        plot_clusters(sub, cid,
                      image_dir, noisyoutput_dir,
                      noise_types,
                      tem_style, tem_mean, tem_std,
                      tem_color)

# -----------------------------------------------------------------------------
# 6) Script entrypoint
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main(
        xml_dir='./xmls/',
        file_begins_with='geometry',
        file_ends_with='.xml',
        output_csv='./data.csv',
        mask_dir='./masks/',
        image_dir='./images/',
        noisyoutput_dir='./noisyoutput/',
        mask_type='both',
        noise_types=['gauss','poisson','tem'],
        tem_style=True,
        tem_mean=180,
        tem_std=25,
        tem_color=(0.045,0.045,0.045,0.3)
    )
