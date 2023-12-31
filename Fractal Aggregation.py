import random
import matplotlib.pyplot as plt
import numpy as np

def center_of_mass(particle_list, x, y, z): # This is a function that finds the average of the coordinates
    cm_x = sum(x) / len(particle_list) # Finds the average x coordinate
    cm_y = sum(y) / len(particle_list) # Finds the average y coordinate
    cm_z = sum(z) / len(particle_list) # Finds the average z coordinate
    return cm_x, cm_y, cm_z # Returns the coordinates in the form of a point

def radius_of_gyration(particle_list, cm): # This function will find the radius of gyration from the coordinates given in the list
    summ = 0 # Set the summation to 0, preparing it for the numbers that will be added together on it
    for i in range(len(particle_list)): # Making a loop that adds all the coordinates together
        summ += (particle_list[i][0] - cm[0])**2 + (particle_list[i][1] - cm[1])**2 + (particle_list[i][2] - cm[2])**2 # The equation that is being added to the summation
    rg = np.sqrt(float(summ) / len(particle_list)) # The equation for radius of gyration, using the summation that the loop calculated
    return rg # Returning the number that the radius of gyration equation got

def distance(x_1, y_1, z_1, x_2, y_2, z_2): # Finds the distance between two particles
    dist = np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2 + (z_1 - z_2)**2) # Distance formula for two points
    return dist # Returns that distance

def intersecting_circles(particle_list, rp, intersecting_list, cm, rog): # Finds the distance between the center of mass and the particles and then categorizes them

    for i in range(len(particle_list)): # Starts a loop to test all the spheres' distances from the center of mass
        dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], cm[0], cm[1], cm[2]) # Distance formula

        if (rog - rp) <= dist <= (rp + rog): # If the distance meets this conditional, then the sphere will be labeled as touching the rog sphere
            intersecting_list.append(particle_list[i]) # Adds the particles that were touching the rog sphere to a new list

def fractal_dimension(n_p, rp, rog_f): # This function will calculate the fractal dimension of the calculated particle
    df = (np.log(n_p / kf)) / (np.log(rog_f / rp)) # The equation for calculating the fractal dimension
    return df # Returns the fractal dimension number

def sphere_surface_placement(x, y, z, r): # Finds a new sphere that is randomly placed on the outside of a chosen sphere
    p = 2 * r # Sets p equal to two times the radius of the particles
    ang_1 = random.uniform(-np.pi / 2, np.pi / 2) # Finds a random angle
    ang_2 = random.uniform(0, 2 * np.pi) # Finds a second random angle

    Nx = x + p * (np.sin(ang_1) * np.cos(ang_2)) # Finds the x coordinate of a sphere that is touching the selected sphere
    Ny = y + p * (np.sin(ang_1) * np.sin(ang_2)) # Finds the y coordinate of a sphere that is touching the selected sphere
    Nz = z + p * (np.cos(ang_1)) # Finds the z coordinate of a sphere that is touching the selected sphere

    return Nx, Ny, Nz # Returns these coordinates together

def gamma(n_p, rp, df_target): # Finds the gamma of the particle
    gm = np.sqrt((((n_p**2 * rp**2) / (n_p - 1)) * (n_p / kf)**(2 / df_target)) - ((n_p * rp**2) / (n_p - 1)) - (n_p * rp**2) * ((n_p - 1) / kf)**(2 / df_target)) # Gamma equation

    return gm # Returns the gamma

def plot_spheres(centers, radii): # Plots the particles using matplotlib
    fig = plt.figure() # Starts the plot for the figure and sets it equal to the fig variable
    ax = fig.add_subplot(projection='3d') # Makes the axes for the plot and sets it equal to the ax variable

    for center in centers: # Starts a loop that will create a circle with a correctly plotted radius
        u,v = np.mgrid[0:2 * np.pi:50j, 0:np.pi:50j] # Creates a mesh gird of the sphere

        x = radii * np.cos(u) * np.sin(v) + center[0] # Creates the x coordinate for a particle with the correct radius
        y = radii * np.sin(u) * np.sin(v) + center[1] # Creates the y coordinate for a particle with the correct radius
        z = radii * np.cos(v) + center[2] # Creates the z coordinate for a particle with the correct radius

        color = np.random.choice(['g', 'b', 'r', 'y']) # Chooses a random color for the particles
        alpha = 0.5 * np.random.random() + 0.5 # Finds a random alpha

        ax.plot_surface(x, y, z, color=color, alpha=alpha) # Plots the particle using the coordinates with the correct radius and the random color and alpha

    ax.set_xlabel('X') # Labels the X axis as X
    ax.set_ylabel('Y') # Labels the Y axis as Y
    ax.set_zlabel('Z') # Labels the Z axis as Z
    ax.set_title('Spheres') # Titles the plot as Spheres
    ax.set_aspect('auto') # Sets the rate that the axes changes to change automatically

    plt.show() # Finally, Shows the plot


def fractal_aggregation_using_gamma(): # This aggregation methods uses gamma to find intersecting particles
    n_p = int(input('Number of Particles? ')) # Asks the user how many particles they want to place
    rp = float(input('Radius of Particles? ')) # Asks the user what they want the radius of the particle to be
    df_t = float(input('What is The Fractal Dimension (1-3)? ')) # Ask the user what they want the target fractal dimension to be

    particle_list = [] # Creates a list for the particles to be placed
    particle_list.append([0, 0, 0]) # Places a particle in the center of the plot
    # plot_spheres(particle_list, rp)
    particle_list.append(sphere_surface_placement(0, 0, 0, rp)) # Finds another particle to place on the surface of the original particle
    # plot_spheres(particle_list, rp)
    max_try = 20 # Sets the max number of times the program will try a particle and try to find a particle


    x = []  # New list for each x coordinate of the spheres
    y = []  # New list for each y coordinate of the spheres
    z = []  # New list for each z coordinate of the spheres
    intersecting_list = [] # New list for the intersecting particles
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0 # Resets the conditional for the following loop

        while counter_2 < max_try: # If the number of times function is run exceeds the max_try number, then the program will stop trying to find a particle
            intersecting_list.clear() # Clears the interesting circle list so that the program and find a new list of interesting circles for the new particle
            x.clear() # Clears the x list
            y.clear() # Clears the y list
            z.clear() # Clears the z list

            for i in range(len(particle_list)):  # Finds the x, y, and z coordinates of the particles
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's

            cm = center_of_mass(particle_list, x, y, z) # Finds the current center of mass of the particle
            gm = gamma(len(particle_list), rp, df_t) # Finds the current gamma of the particle
            rog = radius_of_gyration(particle_list, cm) # Finds the current radius of gyration of the particle

            # print('gamma:', gm)
            # print('Number of Particles:', len(particle_list))
            # print('Center of Mass:', cm)
            # print('Radius of Gyration:', rog)

            intersecting_circles(particle_list, rp, intersecting_list, cm, gm) # Finds the particles that are interesting
            ran_num = random.randrange(len(intersecting_list)) # Chooses a random sphere in the interesting particle list
            counter = 0  # Resetting the counter to zero because the function is making a new circle

            while counter < max_try:  # Stops the function once the number of times the function has tried to find a point exceeds the max_try
                points = sphere_surface_placement(intersecting_list[ran_num][0], intersecting_list[ran_num][1], intersecting_list[ran_num][2], rp)  # Finds the coordinates for the new particle
                works = False  # Resets the condition so false, so we can define when the point meets criteria

                for i in range(len(particle_list)):  # Runs the loop, which finds the distance for each particle
                    dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], points[0], points[1], points[2])  # Finds the distance between each particle

                    if dist >= 2 * rp:  # If the distance is greater than or equal to the two particle's radiis, then the particles are not crossing
                        works = True  # If this condition is met, then those particle's points don't cross, and it works

                    else:  # Sets the second condition that if the particles crosses another particle, run this line of code
                        counter += 1  # Adds one to the counter for everytime the function fails to find a point where the particle can be placed
                        works = False  # If the particle does not meet the requirement of being greater than or equal to one sphere, then it does not work, so work is set to False
                        break  # The function will then break the loop and try finding a new point

                if works == True:  # If all points are True after the loop has finished, it will then run these lines
                    particle_list.append(points)  # The new particle that met all the requirements will be appended (added) to the list of other eligible particles
                    # plot_spheres(particle_list, rp)
                    break  # Breaks the loop and starts the process of finding another particle

            if works == False:  # If the loop has ended because the program can't find another eligible point, it will run this line
                print(f'Could not place a new particle after {max_try} attempts')  # This prints that the program tried max_try times to find a particle
                counter_2 += 1 # Adds 1 to the conditional

            if works == True: # If the function found a particle
                break # It breaks out of the function
        if works == False: # If the function did not find a particle
            print(f'Could not place a new particle after {max_try} x {max_try} attempts') # It prints that it could not find coordinates that worked for a particle and could not find another particle
    print(f'Placed {len(particle_list)} particles')  # Gives the user a message telling them the number of particles placed


    cm_final = center_of_mass(particle_list, x, y, z) # Finds the final center of mass
    rog_final = radius_of_gyration(particle_list, cm_final) # Finds the final radius of gyration
    print('Final Radius of Gyration:', rog_final) # Prints the radius of gyration
    df = fractal_dimension(n_p, rp, rog_final) # Finds the final fractal dimension
    print('Fractal Dimension:', df) # Prints the final fractal dimension
    print('Particle List:', particle_list) # Prints the list of particles
    # print('This is Gamma')
    # print('First Distance Between Two Particles:', distance(particle_list[1][0], particle_list[1][1], particle_list[1][2], particle_list[2][0], particle_list[2][1], particle_list[2][2]))
    # print('Second Distance Between Two Particles:', distance(particle_list[0][0], particle_list[0][1], particle_list[0][2], particle_list[1][0], particle_list[1][1], particle_list[1][2]))
    plot_spheres(particle_list, rp) # Finally, plots the particles and shows that plot

def fractal_aggregation_using_radius_of_gyration(): # This aggregation methods uses radius of gyration to find intersecting particles
    n_p = int(input('Number of Particles? ')) # Asks the user the number of particles they want to create
    rp = float(input('Radius of Particles? ')) # Asks teh use what they want the radius of the particles to be


    particle_list = [] # Creates a list for those particles
    particle_list.append([0, 0, 0]) # Particle placed in the center of the box
    particle_list.append(sphere_surface_placement(0, 0, 0, rp)) # Finds a particles on the surface of the original particle
    max_try = 20 # Sets the number of times the program will try a particle and try to find a new particle


    x = []  # New list for each x coordinate of the particles
    y = []  # New list for each y coordinate of the particles
    z = []  # New list for each z coordinate of the particles
    intersecting_list = [] # Creates a list for the intersecting particles
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0 # Sets the conditional for the following loop

        while counter_2 < max_try:  # If the number of times function is run exceeds the max_try number, then the program will stop trying to find a particle
            intersecting_list.clear()  # Clears the interesting circle list so that the program and find a new list of interesting circles for the new particle
            x.clear()  # Clears the x list
            y.clear()  # Clears the y list
            z.clear()  # Clears the z list

            for i in range(len(particle_list)):  # Finds the x, y, and z coordinates of the current particles
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's

            cm = center_of_mass(particle_list, x, y, z) # Finds the current center of mass
            rog = radius_of_gyration(particle_list, cm) # Finds the current radius of gyration

            intersecting_circles(particle_list, rp, intersecting_list, cm, rog) # Finds the particles that are intersecting
            ran_num = random.randrange(len(intersecting_list)) # Chooses a random particle from the intersecting particle list
            counter = 0  # Resetting the counter to zero because the function is making a new particle

            while counter < max_try:  # Stops the function once the number of times the function has tried to find a point exceeds the max_try
                points = sphere_surface_placement(intersecting_list[ran_num][0], intersecting_list[ran_num][1], intersecting_list[ran_num][2], rp)  # Finds the coordinates for the new particle
                works = False  # Resets the condition so false, so we can define when the point meets criteria

                for i in range(len(particle_list)):  # Runs the loop, which finds the distance for each particle
                    dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], points[0], points[1], points[2])  # Finds the distance between each particle

                    if dist >= 2 * rp:  # If the distance is greater than or equal to the two particle's radii, then the particles are not crossing
                        works = True  # If this condition is met, then those particle's points don't cross, and it works

                    else:  # Sets the second condition that if the particles crosses another circle, run this line of code
                        counter += 1  # Adds one to the counter for everytime the function fails to find a point where the spheres can be placed
                        works = False  # If the particle does not meet the requirement of being greater than or equal to one particle, then it does not work, so work is set to False
                        break  # The function will then break the loop and try finding a new point

                if works == True:  # If all points are True after the loop has finished, it will then run these lines
                    particle_list.append(points)  # The new particle that met all the requirements will be appended (added) to the list of other eligible particles
                    break  # Breaks the loop and starts the process of finding another particle

            if works == False:  # If the loop has ended because the program can't find another eligible point, it will run this line
                print(f'Could not place a new sphere after {max_try} attempts')  # This prints that the program tried max_try times to find a particle
                counter_2 += 1 # Adds one to the conditional

            if works == True: # If the function found a particle
                break # It breaks out of this loop
        if works == False: # If the function could not find a particle
            print(f'Could not place a new sphere after {max_try} x {max_try} attempts') # It prints that it could not find coordinates that worked for a particle and could not find another particle
    print(f'Placed {len(particle_list)} particles')  # Gives the user a message telling them the number of particles placed


    cm_final = center_of_mass(particle_list, x, y, z) # Finds the final center of mass
    rog_final = radius_of_gyration(particle_list, cm_final) # Finds the final radius of gyration
    print('Final Radius of Gyration:', rog_final) # Prints the final radius of gyration
    df = fractal_dimension(n_p, rp, rog_final) # Finds the fractal dimension
    print('Fractal Dimension:', df) # Prints the fractal dimension
    print('Particle List:', particle_list) # Prints the particle list
    # print('This is ROG')
    # print('First Distance Between Two Spheres:', distance(particle_list[1][0], particle_list[1][1], particle_list[1][2], particle_list[2][0], particle_list[2][1], particle_list[2][2]))
    # print('Second Distance Between Two Spheres:', distance(particle_list[0][0], particle_list[0][1], particle_list[0][2], particle_list[1][0], particle_list[1][1], particle_list[1][2]))
    plot_spheres(particle_list, rp) # Finally, plots the particles and shows the plot

kf = 1.5 # Sets the kf for the whole program
print('Do you want to generate an aggregate particle via method 1 that uses radius of gyration as a reference radius for growth (1)') # Prints the following text
print('or method 2 that attempts to generate an aggregate with a target fractal dimension (2)?') # Prints the following text
response = int(input()) # The user types whether they want option 1 or 2

if response == 1: # If the user chooses option 1
    fractal_aggregation_using_radius_of_gyration() # The radius of gyration aggregation function is called

elif response == 2: # If the user chooses option 2
    fractal_aggregation_using_gamma() # The gamma aggregation function is called