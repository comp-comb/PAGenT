import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd
import os
import numpy as np
from matplotlib.patches import Circle
from scipy.signal import fftconvolve
from scipy.special import j1
from PIL import Image
import noise

# -----------------------------------------------------------------------------
# 1) XML → CSV
# -----------------------------------------------------------------------------
def parse_data_to_CSV(xml_dir, file_begins_with, file_ends_with, output_csv):
    xml_files = sorted(f for f in os.listdir(xml_dir)
                       if f.startswith(file_begins_with) and f.endswith(file_ends_with))
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
# 2) Mask generation (unchanged)
# -----------------------------------------------------------------------------
def plot_particle_mask(cluster_df, cluster_id, mask_dir):
    w, h, dpi = 1024,1024,96
    out = os.path.join(mask_dir, 'particle'); os.makedirs(out, exist_ok=True)
    for idx, row in enumerate(cluster_df.itertuples(), start=1):
        fig, ax = plt.subplots(figsize=(w/dpi,h/dpi), dpi=dpi)
        fig.patch.set_facecolor('black'); ax.set_facecolor('black')
        ax.add_patch(Circle((row.x,row.y), row.Radius, color='white', fill=True))
        ax.set_xlim(-w/2,w/2); ax.set_ylim(-h/2,h/2)
        ax.set_aspect('equal'); ax.axis('off')
        fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
        fn = os.path.join(out, f'mask_{cluster_id:06d}_{idx:06d}.png')
        fig.savefig(fn, dpi=dpi, bbox_inches=None, pad_inches=0,
                    facecolor=fig.get_facecolor())
        plt.close(fig)

def plot_clusters_mask(cluster_df, cluster_id, mask_dir):
    w, h, dpi = 1024,1024,96
    out = os.path.join(mask_dir, 'cluster'); os.makedirs(out, exist_ok=True)
    fig, ax = plt.subplots(figsize=(w/dpi,h/dpi), dpi=dpi)
    fig.patch.set_facecolor('black'); ax.set_facecolor('black')
    for row in cluster_df.itertuples():
        ax.add_patch(Circle((row.x,row.y), row.Radius, color='white', fill=True))
    ax.set_xlim(-w/2,w/2); ax.set_ylim(-h/2,h/2)
    ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    fn = os.path.join(out, f'mask_{cluster_id:06d}.png')
    fig.savefig(fn, dpi=dpi, bbox_inches=None, pad_inches=0,
                facecolor=fig.get_facecolor())
    plt.close(fig)



# -----------------------------------------------------------------------------
# 3) Noise + TEM‐style background
# -----------------------------------------------------------------------------
def add_gauss_noise(image, gaussian_std=0.09):
    noise = np.random.normal(scale=gaussian_std, size=image.shape)
    return np.clip(image + noise,0,1)

def add_poisson_noise(image, intensity=2):
    pn = np.random.poisson(image/intensity)*intensity
    return np.clip(image + pn,0,1)

def add_combined_noise(image, poisson_intensity=2, gaussian_std=0.09):
    return add_gauss_noise(add_poisson_noise(image, poisson_intensity), gaussian_std)

def generate_hrtem_noise_image(width=1024, height=1024, mean=128, std=15):
    rnd = np.random.normal(loc=mean, scale=std, size=(height,width))
    return np.clip(rnd, 0, 255).astype(np.uint8)

def make_airy_kernel(diameter, size=None, scale=1.5):
    # scale>1.0 “compresses” the pattern so rings are sharper
    if size is None:
        size = int(diameter*4)
    x = np.linspace(-2, 2, size)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X*X + Y*Y) + 1e-8
    P = (2*j1(np.pi*scale*R)/(np.pi*scale*R))**2
    P[np.isnan(P)] = 1
    return P / P.sum()

def build_circle_mask(cluster_df, w=1024, h=1024):
    """
    Returns a boolean (h,w) mask that is True inside ANY particle circle, False outside.
    """
    Y, X = np.ogrid[:h, :w]
    mask = np.zeros((h, w), dtype=bool)
    for row in cluster_df.itertuples():
        # assuming row.x,row.y are centered coords, and circle center is at image center
        cx = (w/2) + row.x
        cy = (h/2) + row.y
        r_px = row.Radius
        mask |= ( (X - cx)**2 + (Y - cy)**2 ) <= (r_px**2)
    return mask.astype(float)

def build_noisy_circle_mask(cluster_df, w=1024, h=1024,
                            noise_scale=0.1, noise_amp=0.2):
    """
    Returns a float mask (h,w) where each circle’s radius is perturbed:
      noisy_radius(θ) = R * (1 + noise_amp * N( x, y ))
    with noise N sampled from noise.snoise2(noise_scale * X, noise_scale * Y).

    noise_scale: roughly the spatial frequency of the wiggles (smaller → larger features)
    noise_amp:   maximum relative radius perturbation (e.g. 0.2 → ±20%)
    """
    Y, X = np.ogrid[:h, :w]
    mask = np.zeros((h, w), dtype=float)

    for row in cluster_df.itertuples():
        cx = w/2 + row.x
        cy = h/2 + row.y
        R0 = row.Radius

        # Compute distance field and sample a noise field
        dx = X - cx
        dy = Y - cy
        R = np.sqrt(dx*dx + dy*dy)

        # Perlin noise sampled in image coords
        # (you can also sample in polar coords for radial-only variation)
        Nx = noise_scale * (X / w)
        Ny = noise_scale * (Y / h)
        # Vectorize noise.snoise2 over the grid
        noise_grid = np.vectorize(lambda xx, yy: noise.snoise2(xx, yy))(Nx, Ny)

        # Compute perturbed radius field
        Rpert = R0 * (1 + noise_amp * noise_grid)

        # Fill mask where distance ≤ perturbed radius
        mask += (R <= Rpert).astype(float)

    # if overlapping particles, mask>1 where they overlap—OK for our coverage map later
    return mask


def build_lumpy_circle_mask(
    cluster_df, w=1024, h=1024,
    octaves=4, lacunarity=2.0, gain=0.5,
    base_scale=3.0,  # how many wiggles around the circle
    base_amp=0.5     # maximum ±50% radius variation
):
    """
    For each particle, sample a fractal 1D noise in theta to modulate R(θ):
      NF(θ) = sum_{i=0..octaves-1} gain^i * snoise2(scale*θ, scale*i)
    and then threshold R <= R0*(1 + base_amp*NF(θ)).
    """
    Y, X = np.ogrid[:h, :w]
    mask = np.zeros((h, w), dtype=float)

    cx0, cy0 = w/2, h/2
    for row in cluster_df.itertuples():
        cx = cx0 + row.x
        cy = cy0 + row.y
        R0 = row.Radius

        dx = X - cx
        dy = Y - cy
        R  = np.sqrt(dx*dx + dy*dy)
        θ  = np.arctan2(dy, dx)  # -π..π

        # Normalize θ to [0,1] for noise input
        t = (θ + np.pi) / (2*np.pi)

        # build fractal noise
        nf = np.zeros_like(R)
        frequency = base_scale
        amp = 1.0
        for _ in range(octaves):
            nf += amp * np.vectorize(noise.snoise2)(frequency * t, frequency * t*1.1)
            frequency *= lacunarity
            amp       *= gain

        # Rpert = R0 * (1 + base_amp * nf)
        Rpert = R0 * (1 + base_amp * nf)

        # fill where R <= Rpert
        mask += (R <= Rpert).astype(float)

    return mask

# -----------------------------------------------------------------------------
# 4) Cluster rendering + fringe application + noise outputs
# -----------------------------------------------------------------------------
def plot_clusters(cluster_df, cluster_id,
                  image_dir, noisyoutput_dir,
                  noise_types=['gauss'],
                  tem_style=False, tem_mean=128, tem_std=15,
                  tem_color=(0.045,0.045,0.045,0.3)):
    w, h, dpi = 1024,1024,96

    # Draw base: TEM background + circles
    fig, ax = plt.subplots(figsize=(w/dpi,h/dpi), dpi=dpi)
    # if tem_style:
    #     bg = generate_hrtem_noise_image(w,h,tem_mean,tem_std)
    #     ax.imshow(bg, cmap='gray', origin='lower',
    #               extent=[-w/2,w/2,-h/2,h/2], interpolation='nearest')
    for row in cluster_df.itertuples():
        ax.add_patch(Circle((row.x,row.y), row.Radius,
                            color=tem_color, fill=True, linewidth=0))
    ax.set_xlim(-w/2,w/2); ax.set_ylim(-h/2,h/2)
    ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(noisyoutput_dir, exist_ok=True)

    base_fn = os.path.join(image_dir, f'image_{cluster_id:06d}.png')
    fig.savefig(base_fn, dpi=dpi, bbox_inches=None, pad_inches=0)
    plt.close(fig)

    base_img = plt.imread(base_fn)

    # Generate outputs per noise type
    for nt in noise_types:
        if nt == 'gauss':
            out = add_gauss_noise(base_img)
        elif nt == 'poisson':
            out = add_poisson_noise(base_img)
        elif nt == 'combined':
            out = add_combined_noise(base_img)
        elif nt == 'tem':
            # 1) TEM grain background
            bg = generate_hrtem_noise_image(w, h, tem_mean, tem_std) / 255.0
            bg3 = np.dstack([bg]*3)

            # 2) Fringe map
            avg_r = np.mean(cluster_df['Radius'])
            kernel = make_airy_kernel(avg_r*2, scale=1)

            # instead of:
            mask_union = build_circle_mask(cluster_df, w, h)
            # # use:
            # mask_union = build_noisy_circle_mask(
            #     cluster_df, w, h,
            #     noise_scale=2,   # tweak for feature size
            #     noise_amp=0.7      # tweak for wiggle magnitude
            # )

            # or:

            # instead of build_circle_mask(...)
            # mask_union = build_lumpy_circle_mask(
            #     cluster_df, w, h,
            #     octaves=5,
            #     lacunarity=2.5,
            #     gain=0.4,
            #     base_scale=2.0,
            #     base_amp=0.8
            # )



            raw = fftconvolve(mask_union, kernel, mode='same')
         
            strength, gamma = 1, 1
            fringes = np.clip(strength * raw, 0, 1)**gamma

            # if not using airy kernel, use:
            # fringes=mask_union

            

            # # 3) Draw fringes
            ring_rgb   = np.array(tem_color[:3])[None,None,:]
            ring_alpha = tem_color[3]
            alpha_map  = (ring_alpha * fringes)[...,None]
            rgb_map    = ring_rgb * fringes[...,None]
            out = bg3*(1-alpha_map) + rgb_map*alpha_map

            # 4) Build an *integer* coverage map*
            count_map = np.zeros((h, w), dtype=np.float32)
            Y, X = np.ogrid[:h, :w]
            for row in cluster_df.itertuples():
                cx = w/2 + row.x
                cy = h/2 + row.y
                r  = row.Radius
                # per‑circle mask
                circle = ((X-cx)**2 + (Y-cy)**2) <= r**2
                count_map[circle] += 1

            # 5) Generate your “particle” noise image
            pn = generate_hrtem_noise_image(w, h, tem_mean*0.3, tem_std*1.2)/255.0

            # 6) Compute an *interior alpha map* that darkens with overlap count.
            #    e.g. base_alpha = 0.6 for single‑layer, then alpha = base_alpha*count
            base_alpha = 0.3
            interior_alpha = np.zeros_like(count_map)
            nonzero = count_map > 0
            interior_alpha[nonzero] = (base_alpha * count_map[nonzero])

            # 7) Blend particle noise in with per‑pixel alpha
            ai = interior_alpha[...,None]  # shape (h,w,1)
            out = out*(1-ai) + pn[...,None]*ai

            # 8) Clamp
            out = np.clip(out, 0, 1)

        else:
            raise ValueError(f"Unknown noise type '{nt}'")

        fn = os.path.join(noisyoutput_dir,
                          f'image_{cluster_id:06d}_{nt}.png')
        plt.imsave(fn, out)
        print(f"Rendered cluster {cluster_id:06d} with {nt}")

# -----------------------------------------------------------------------------
# 5) Main pipeline
# -----------------------------------------------------------------------------
def main(xml_dir, file_begins_with, file_ends_with,
         output_csv, mask_dir, image_dir, noisyoutput_dir,
         mask_type='both',
         noise_types=['gauss'],
         tem_style=False, tem_mean=1, tem_std=15,
         tem_color=(0.045,0.045,0.045,0.3)):
    df = parse_data_to_CSV(xml_dir, file_begins_with, file_ends_with, output_csv)
    for cid in df['Cluster'].unique():
        sub = df[df['Cluster']==cid]
        if sub.empty:
            continue
        if mask_type in ('particle','both'):
            plot_particle_mask(sub, cid, mask_dir)
        if mask_type in ('cluster','both'):
            plot_clusters_mask(sub, cid, mask_dir)
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
        noise_types=['tem'],
        tem_style=True,
        tem_mean=180,
        tem_std=15,
        tem_color=(0.045, 0.045, 0.045, 0.3)
    )
