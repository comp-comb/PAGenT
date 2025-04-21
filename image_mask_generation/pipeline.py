import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Ellipse
from PIL import Image

# Function to parse the xml files and save the data to a csv file
def parse_data_to_CSV(xml_dir, file_begins_with, file_ends_with, output_csv):

    # get all xml files in the directory
    xml_files = []
    for file in os.listdir(xml_dir):
        if file.endswith(file_ends_with) and file.startswith(file_begins_with):
            xml_files.append(file)

    #DF for the final file
    data = pd.DataFrame(columns = ['Cluster', 'Particle', 'Radius', 'x', 'y', 'z'])

    # Initialize lists to store data
    particle_id, radius, x, y, z = [], [], [], [], []
    cluster_id = []
    counter=0

    # loop through all xml files
    for file in xml_files:
        # parse the xml file
        tree = ET.parse(xml_dir + file)
        root = tree.getroot()
        # Extract particle data
        data_particle = root.find(".//data_particle")
        for particle in data_particle.findall('particle'):
            part_id = particle.get('ID')
            part_radius = float(particle.find('radius').text.strip())
            position = [float(p.strip()) for p in particle.find('position').text.strip().split(',')]
            # Append data to lists
            particle_id.append(part_id)
            radius.append(part_radius)
            x.append(position[0])
            y.append(position[1])
            z.append(position[2])
            cluster_id.append(counter)
        counter+=1

    # Add data to the dataframe
    data['Cluster'] = cluster_id
    data['Particle'] = particle_id
    data['Radius'] = radius
    data['x'] = x
    data['y'] = y
    data['z'] = z

    # Save the dataframe to a csv file
    data.to_csv(output_csv, index=False)

    return data

########################################################################################

# Function to plot the individual particles in a cluster and save them as a 1-bit image
def plot_particle_mask(cluster_df, clusters):
    # setting the plot size 
    w = 1024
    h = 1024
    # setting the dpi of the figure
    dpi = 96
    # setting the figure properties
    plt.rcParams["figure.figsize"] = [w/dpi, h/dpi]
    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams['savefig.facecolor'] = 'black'
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams['figure.facecolor'] = 'black'
   
    #list to store mask data
    particle_datadf = []
    # The count variable keeps track of the rank of particles in a cluster
    count = 1
    for index, row in cluster_df.iterrows():
        fig, ax = plt.subplots()
        fig.set_size_inches(w/dpi, h/dpi)
        x = row['x']
        y = row['y']
        radius = row['Radius']
        ax.set_facecolor("black")
        circle = plt.Circle((x, y), radius, fill=True, color='w')
        ax.add_artist(circle)
        ax.set_aspect(1)
        ax.set_xlim([-w/2, w/2])
        ax.set_ylim([-h/2, h/2])
        border = plt.Rectangle((-w/2, -h/2), w, h, fill=False, edgecolor='r', linewidth=2)
        ax.add_patch(border)
        plt.axis('off')
        #plt.tight_layout()
        # saving the figure
        output = mask_dir
        if not os.path.exists(output):
            os.makedirs(output)
        # Create additional directories if not present
        if not os.path.exists(f'{output}/particle'):
            os.makedirs(f'{output}/particle')
        filename = f'{output}/particle/mask_{str(clusters).zfill(6)}_{str(count).zfill(6)}.png'
        plt.savefig(filename, bbox_inches=None, pad_inches=0)
        plt.close()   # close the figure window 
        
        #img = Image.open(filename).convert('1')
        #img.save(filename)

        particle_datadf.append([x,y,radius,count])

        count += 1
    
    particle_datadf = pd.DataFrame(particle_datadf, columns = ["x","y","radius","count"])
    return particle_datadf



def plot_part_mask2(cluster_df,clusters):
    # setting the plot size 
    
    count=0
  
    output = mask_dir
    if not os.path.exists(output):
        os.makedirs(output)
    if not os.path.exists(f'{output}/particle'):
        os.makedirs(f'{output}/particle')

    for index, row in cluster_df.iterrows():
        w=1024
        h=1024
        # setting the dpi of the figure
        dpi=96
        # setting the figure properties
        plt.rcParams["figure.figsize"] = [w/dpi, h/dpi]
        plt.rcParams["figure.dpi"] = dpi
        plt.rcParams['savefig.facecolor'] = 'black'
        plt.rcParams['savefig.dpi'] = dpi
        plt.rcParams['figure.facecolor'] = 'black'
        
        fig, ax = plt.subplots()
        fig.set_size_inches(w/dpi,h/dpi)
        ax.set_facecolor("black")

        x = row['x']
        y = row['y']
        radius = row['Radius']
        
        circle = plt.Circle((x, y), radius, fill=True, color='w')
        ax.add_artist(circle)
        # ax.set_aspect('equal', adjustable='box')
        ax.set_aspect(1)
        ax.set_xlim([-1024/2, 1024/2])
        ax.set_ylim([-1024/2, 1024/2])
        plt.axis('off')

        filename = f'{output}/particle/mask_{str(clusters).zfill(6)}_{count:06d}.png'
        plt.savefig(filename, bbox_inches=None, pad_inches=0)
        img = Image.open(filename).convert('1')
        img.save(filename)
        plt.close()  

        count += 1
    
    #plt.tight_layout()
    print(f"PART_MASK: total particle masks: {count}")
 
   

    
    
    # close the figure window 


#############################################################################################

# Function to plot the individual particles in a cluster and save them as a 1-bit image
def plot_clusters_mask(cluster_df,clusters):
    # setting the plot size 
    w=1024
    h=1024
    # setting the dpi of the figure
    dpi=96
    # setting the figure properties
    plt.rcParams["figure.figsize"] = [w/dpi, h/dpi]
    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams['savefig.facecolor'] = 'black'
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams['figure.facecolor'] = 'black'
   
    fig, ax = plt.subplots()
    fig.set_size_inches(w/dpi,h/dpi)
    ax.set_facecolor("black")
    count =0
    for index, row in cluster_df.iterrows():
        
        x = row['x']
        y = row['y']
        radius = row['Radius']
        
        circle = plt.Circle((x, y), radius, fill=True, color='w')
        ax.add_artist(circle)
        # ax.set_aspect('equal', adjustable='box')

        count +=1
       
    ax.set_aspect(1)
    ax.set_xlim([-w/2, w/2])
    ax.set_ylim([-h/2, h/2])
    #plt.tight_layout()
    plt.axis('off')
 
    output = mask_dir
    if not os.path.exists(output):
        os.makedirs(output)
    # Create additional directories if not present
    if not os.path.exists(f'{output}/cluster'):
        os.makedirs(f'{output}/cluster')

    filename = f'{output}/cluster/mask_{str(clusters).zfill(6)}.png'
    plt.savefig(filename, bbox_inches=0, pad_inches=0)
    img = Image.open(filename).convert('1')
    img.save(filename)
    plt.close()   # close the figure window 
    print(f"Cluster_mask: total particles: {count}")

    


###################################################################################
#Functions ot add noise to images

def add_gauss_noise(image, gaussian_std=0.09):
    gauss_noise = np.random.normal(scale=gaussian_std, size=image.shape)
    noisy_image = image + gauss_noise
    noisy_image = np.clip(noisy_image,0,1)
    return noisy_image
def add_poisson_noise(image, intensity = 2):
    poisson_noise = np.random.poisson(image / intensity) * intensity
    noisy_image = np.clip(image+poisson_noise,0,1)
    return noisy_image
def add_combined_noise(image, poisson_intensity = 2, gaussian_std=0.09):
    poisson_noise = np.random.poisson(image / poisson_intensity) * poisson_intensity
    poisson_image = np.clip(image+poisson_noise,0,1)   

    gauss_noise = np.random.normal(scale=gaussian_std, size=image.shape) 
    noisy_image = np.clip(poisson_image+gauss_noise,0,1)
    return noisy_image

######################################################################################

#plot full clusters and add noise

def plot_clusters(cluster_df,clusters, noisetype):
    #plot size
    w = 1024
    h = 1024
    #figure dpi
    dpi= 96

    plt.rcParams["figure.figsize"] = [w/dpi, h/dpi]
    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams['figure.facecolor'] = '#A4A4A4' #paddle: 7E7E7E  sipkemtem: #A4A4A4
    #plt.rcParams['savefig.facecolor'] = '#B6B6B6'
    fig, ax = plt.subplots()
    fig.set_size_inches(w/dpi,h/dpi)
    temcolor = (.045,.045,.045,0.3)
    count =0 
    #list to store particle data
    cluster_data = []
    for index, row in cluster_df.iterrows():
        x = row['x']
        y = row['y']
        radius = row['Radius']
        circle = plt.Circle((x,y),radius, fill=True, color=temcolor,linewidth=0, antialiased=True)
        ax.add_artist(circle)
        #ellipse = Ellipse((x,y), width = radius* np.random.uniform(1,4), height = radius*np.random.uniform(1,4), fill=True, color=temcolor,linewidth=0, antialiased=False)
        #ax.add_artist(ellipse)
        ax.set_aspect(1)
        ax.set_xlim([-1024/2,1024/2])
        ax.set_ylim([-1024/2,1024/2])
        cluster_data.append([x,y,radius])
        count+=1
    #ax.set_aspect(1)
    #ax.set_xlim([-w/2,w/2])
    #ax.set_ylim([-h/2,h/2])
    #border = plt.Rectangle((-w/2, -h/2), w, h, fill=False, edgecolor='r', linewidth=2)
    #ax.add_patch(border)

    plt.axis('off')
    #plt.tight_layout()
    #plt.show()

    output = image_dir
    if not os.path.exists(output):
        os.makedirs(output)

    noisyoutput = noisyoutput_dir
    if not os.path.exists(noisyoutput):
        os.makedirs(noisyoutput)

    filename = f'{output}/image_{str(clusters).zfill(6)}.png'
    plt.savefig(filename,bbox_inches=None,pad_inches=0)
    image = plt.imread(filename)
    if noisetype == 1:
        noisy_image = add_gauss_noise(image)
    if noisetype == 2:
        noisy_image = add_poisson_noise(image)
    if noisetype == 3:
        noisy_image = add_combined_noise(image)

  
    noisy_filename = f'{noisyoutput}image_{str(clusters).zfill(6)}.png'
    plt.imsave(noisy_filename, noisy_image)
    #plt.show()
    
    cluster_datadf = pd.DataFrame(cluster_data, columns=["x","y","radius"])
   
    plt.close()   # close the figure window

    print(f"Cluster_render: total particle count: {count}")
    return cluster_datadf


######################################################################################

#run though all

def main(xml_dir, file_begins_with, file_ends_with, output_csv, mask_dir, 
         image_dir, noisyoutput_dir, noisetype, mask_type):
    data = parse_data_to_CSV(xml_dir, file_begins_with, file_ends_with, output_csv)

    #can also be started directly from csv
    #data= pd.read_csv(output_csv, index_col=False)

    particle_dataframes = []
    cluster_dataframes = []

    if mask_type == 'particle' or mask_type == 'both':
    #looping through clusters and calling plot particle mask function
        for clusters in data['Cluster'].unique():
            cluster_df = data[data['Cluster'] == clusters]
            plot_part_mask2(cluster_df, clusters)
            #particle_df= plot_particle_mask(cluster_df, clusters)
            #if not particle_df.empty:
                #particle_dataframes.append(particle_df)

    if mask_type == 'cluster' or mask_type == 'both':
        for clusters in data['Cluster'].unique():
            cluster_df = data[data['Cluster'] == clusters]
            plot_clusters_mask(cluster_df, clusters)

    for clusters in data['Cluster'].unique():
        cluster_df = data[data['Cluster'] == clusters]
        plt.rcdefaults()
        plot_clusters(cluster_df, clusters, noisetype)
        #cluster_datadf = plot_clusters(cluster_df, clusters, noisetype)
        if not cluster_df.empty:
            plot_clusters(cluster_df, clusters, noisetype)
            #cluster_dataframes.append(cluster_datadf)

    # Combine dataframes
    #if particle_dataframes:
    #    particle_datadf = pd.concat(particle_dataframes, ignore_index=True)
    #else:
    #    particle_datadf = pd.DataFrame(columns=["x", "y", "radius", "count"])

    #if cluster_dataframes:
    #    cluster_datadf = pd.concat(cluster_dataframes, ignore_index=True)
    #else:
    #    cluster_datadf = pd.DataFrame(columns=["x", "y", "radius"])

   

    #return cluster_datadf, particle_datadf  # Returning for further use


if __name__ == "__main__":
    # Example usage
    # Define your parameters here
    ROOT = './'
    xml_dir = os.path.join(ROOT, 'xmls/')
    file_begins_with = 'geometry'
    file_ends_with = '.xml'
    output_csv = os.path.join(ROOT,'data.csv')
    mask_dir = os.path.join(ROOT, 'masks/')
    image_dir = os.path.join(ROOT, 'images/')
    noisyoutput_dir = os.path.join(ROOT,'noisyoutput/')
    noisetype = 1 #1 for gaussian, 2 for poisson, 3 for combined

    main(xml_dir, file_begins_with, file_ends_with, output_csv, 
         mask_dir, image_dir, noisyoutput_dir, noisetype, mask_type='both')

