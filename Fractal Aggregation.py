import random
import matplotlib.pyplot as plt
import numpy as np

def center_of_mass(particle_list, x, y, z): # This is a function that finds the average of the coordinates
    cm_x = sum(x) / len(particle_list) # Finds the average x coordinate
    cm_y = sum(y) / len(particle_list) # Finds the average y coordinate
    cm_z = sum(z) / len(particle_list) # Finds the average z coordinate
    return cm_x, cm_y, cm_z # Returns the coordinates in the form of a point

def radius_of_gyration(particle_list, cm): # This function will find the radius of gyration from all the coordinates
    summ = 0 # Set the summation to 0, preparing it for the numbers that will be added together on it
    for i in range(len(particle_list)): # Making a loop that adds all the coordinates together
        summ += (particle_list[i][0] - cm[0])**2 + (particle_list[i][1] - cm[1])**2 + (particle_list[i][2] - cm[2])**2 # The equation that is being added to the summation
    rg = np.sqrt(float(summ) / len(particle_list)) # The equation for radius of gyration, using the summation that the loop calculated
    return rg # Returning the number that the radius of gyration equation got

def distance(x_1, y_1, z_1, x_2, y_2, z_2): # Finds the distance between two circles
    dist = np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2 + (z_1 - z_2)**2) # Distance formula for two points
    return dist # Returns that distance

def intersecting_circles(particle_list, rp, intersecting_list, cm, rog): # Finds the distance between the center of mass and the spheres and then categorizes them

    for i in range(len(particle_list)): # Starts a loop to test all the spheres' distances from the center of mass
        dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], cm[0], cm[1], cm[2]) # Distance formula

        if (rog - rp) <= dist <= (rp + rog): # If the distance meets this conditional, then the sphere will be labeled as touching the rog sphere
            intersecting_list.append(particle_list[i])

def fractal_dimension(n_p, rp, rog_f):
    df = (np.log(n_p / kf)) / (np.log(rog_f / rp))
    return df

def sphere_surface_placement(x, y, z, r): # Finds a new sphere that is randomly placed on the outside of a chosen sphere
    p = 2 * r
    ang_1 = random.uniform(-np.pi / 2, np.pi / 2)
    ang_2 = random.uniform(0, 2 * np.pi)

    Nx = x + p * (np.sin(ang_1) * np.cos(ang_2))
    Ny = y + p * (np.sin(ang_1) * np.sin(ang_2))
    Nz = z + p * (np.cos(ang_1))

    return Nx, Ny, Nz

def gamma(n_p, rp, df_target):
    gm = np.sqrt((((n_p**2 * rp**2) / (n_p - 1)) * (n_p / kf)**(2 / df_target)) - ((n_p * rp**2) / (n_p - 1)) - (n_p * rp**2) * ((n_p - 1) / kf)**(2 / df_target))

    return gm

def plot_spheres(centers, radii):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for center in centers:
        u,v = np.mgrid[0:2 * np.pi:50j, 0:np.pi:50j]

        x = radii * np.cos(u) * np.sin(v) + center[0]
        y = radii * np.sin(u) * np.sin(v) + center[1]
        z = radii * np.cos(v) + center[2]

        color = np.random.choice(['g', 'b', 'r', 'y'])
        alpha = 0.5 * np.random.random() + 0.5

        ax.plot_surface(x, y, z, color=color, alpha=alpha)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Spheres')
    ax.set_aspect('auto')

    plt.show()


def fractal_aggregation_using_gamma():
    n_p = int(input('Number of Particles? '))
    rp = float(input('Radius of Particles? '))
    df_t = float(input('What is The Fractal Dimension (1-3)? '))

    particle_list = []
    particle_list.append([0, 0, 0]) # Sphere placed in the center of the box
    # plot_spheres(particle_list, rp)
    particle_list.append(sphere_surface_placement(0, 0, 0, rp))
    # plot_spheres(particle_list, rp)
    max_try = 20


    x = []  # New list for each x coordinate of the spheres
    y = []  # New list for each y coordinate of the spheres
    z = []  # New list for each z coordinate of the spheres
    intersecting_list = []
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0

        while counter_2 < max_try:
            intersecting_list.clear()
            x.clear()
            y.clear()
            z.clear()

            for i in range(len(particle_list)):  # (Return this from the sphere_placement function in Version 2)
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's

            cm = center_of_mass(particle_list, x, y, z)
            gm = gamma(len(particle_list), rp, df_t)
            rog = radius_of_gyration(particle_list, cm)

            # print('gamma:', gm)
            # print('Number of Particles:', len(particle_list))
            # print('Center of Mass:', cm)
            # print('Radius of Gyration:', rog)

            intersecting_circles(particle_list, rp, intersecting_list, cm, gm)
            ran_num = random.randrange(len(intersecting_list))
            counter = 0  # Resetting the counter to zero because the function is making a new circle

            while counter < max_try:  # Stops the function once the number of times the function has tried to find a point exceeds the max_try
                points = sphere_surface_placement(intersecting_list[ran_num][0], intersecting_list[ran_num][1], intersecting_list[ran_num][2], rp)  # Finds the coordinates for the new circle
                works = False  # Resets the condition so false, so we can define when the point meets criteria

                for i in range(len(particle_list)):  # Runs the loop, which finds the distance for each circle in spheres
                    dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], points[0], points[1], points[2])  # Finds the distance between each sphere

                    if dist >= 2 * rp:  # If the distance is greater than or equal to the two circles radi's than they circles are not crossing
                        works = True  # If this condition is met, then those circle's points don't cross, and it works

                    else:  # Sets the second condition that if the circle crosses another circle, run this line of code
                        counter += 1  # Adds one to the counter for everytime the function fails to find a point where the spheres can be placed
                        works = False  # If the sphere does not meet the requirement of being greater than or equal to one sphere, then it does not work, so work is set to False
                        break  # The function will then break the loop and try finding a new point

                if works == True:  # If all points are True after the loop has finished, it will then run these lines
                    particle_list.append(points)  # The new sphere that met all the requirements will be appended (added) to the list of other eligible spheres
                    # plot_spheres(particle_list, rp)
                    break  # Breaks the loop and starts the process of finding another sphere

            if works == False:  # If the loop has ended because the program can't find another eligible point, it will run this line
                print(f'Could not place a new particle after {max_try} attempts')  # This prints that the program tried max_try times to find a sphere
                counter_2 += 1

            if works == True:
                break
        if works == False:
            print(f'Could not place a new particle after {max_try} x {max_try} attempts')
    print(f'Placed {len(particle_list)} particles')  # Gives the user a message telling them the number of spheres placed


    cm_final = center_of_mass(particle_list, x, y, z)
    rog_final = radius_of_gyration(particle_list, cm_final)
    print('Final Radius of Gyration:', rog_final)
    df = fractal_dimension(n_p, rp, rog_final)
    print('Fractal Dimension:', df)
    print('Particle List:', particle_list)
    # print('This is Gamma')
    # print('First Distance Between Two Particles:', distance(particle_list[1][0], particle_list[1][1], particle_list[1][2], particle_list[2][0], particle_list[2][1], particle_list[2][2]))
    # print('Second Distance Between Two Particles:', distance(particle_list[0][0], particle_list[0][1], particle_list[0][2], particle_list[1][0], particle_list[1][1], particle_list[1][2]))
    plot_spheres(particle_list, rp)

def fractal_aggregation_using_radius_of_gyration():
    n_p = int(input('Number of Particles? '))
    rp = float(input('Radius of Particles? '))


    particle_list = []
    particle_list.append([0, 0, 0]) # Sphere placed in the center of the box
    particle_list.append(sphere_surface_placement(0, 0, 0, rp))
    max_try = 20


    x = []  # New list for each x coordinate of the spheres
    y = []  # New list for each y coordinate of the spheres
    z = []  # New list for each z coordinate of the spheres
    intersecting_list = []
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0

        while counter_2 < max_try:
            intersecting_list.clear()
            x.clear()
            y.clear()
            z.clear()

            for i in range(len(particle_list)):  # (Return this from the sphere_placement function in Version 2)
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's

            cm = center_of_mass(particle_list, x, y, z)
            rog = radius_of_gyration(particle_list, cm)

            intersecting_circles(particle_list, rp, intersecting_list, cm, rog)
            ran_num = random.randrange(len(intersecting_list))
            counter = 0  # Resetting the counter to zero because the function is making a new circle

            while counter < max_try:  # Stops the function once the number of times the function has tried to find a point exceeds the max_try
                points = sphere_surface_placement(intersecting_list[ran_num][0], intersecting_list[ran_num][1], intersecting_list[ran_num][2], rp)  # Finds the coordinates for the new circle
                works = False  # Resets the condition so false, so we can define when the point meets criteria

                for i in range(len(particle_list)):  # Runs the loop, which finds the distance for each circle in spheres
                    dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], points[0], points[1], points[2])  # Finds the distance between each sphere

                    if dist >= 2 * rp:  # If the distance is greater than or equal to the two circles radi's than they circles are not crossing
                        works = True  # If this condition is met, then those circle's points don't cross, and it works

                    else:  # Sets the second condition that if the circle crosses another circle, run this line of code
                        counter += 1  # Adds one to the counter for everytime the function fails to find a point where the spheres can be placed
                        works = False  # If the sphere does not meet the requirement of being greater than or equal to one sphere, then it does not work, so work is set to False
                        break  # The function will then break the loop and try finding a new point

                if works == True:  # If all points are True after the loop has finished, it will then run these lines
                    particle_list.append(points)  # The new sphere that met all the requirements will be appended (added) to the list of other eligible spheres
                    break  # Breaks the loop and starts the process of finding another sphere

            if works == False:  # If the loop has ended because the program can't find another eligible point, it will run this line
                print(f'Could not place a new sphere after {max_try} attempts')  # This prints that the program tried max_try times to find a sphere
                counter_2 += 1

            if works == True:
                break
        if works == False:
            print(f'Could not place a new sphere after {max_try} x {max_try} attempts')
    print(f'Placed {len(particle_list)} particles')  # Gives the user a message telling them the number of spheres placed


    cm_final = center_of_mass(particle_list, x, y, z)
    rog_final = radius_of_gyration(particle_list, cm_final)
    print('Final Radius of Gyration:', rog_final)
    df = fractal_dimension(n_p, rp, rog_final)
    print('Fractal Dimension:', df)
    print('Particle List:', particle_list)
    # print('This is ROG')
    # print('First Distance Between Two Spheres:', distance(particle_list[1][0], particle_list[1][1], particle_list[1][2], particle_list[2][0], particle_list[2][1], particle_list[2][2]))
    # print('Second Distance Between Two Spheres:', distance(particle_list[0][0], particle_list[0][1], particle_list[0][2], particle_list[1][0], particle_list[1][1], particle_list[1][2]))
    plot_spheres(particle_list, rp)

kf = 1.5
print('Do you want to generate an aggregate particle via method 1 that uses radius of gyration as a reference radius for growth (1)')
print('or method 2 that attempts to generate an aggregate with a target fractal dimension (2)?')
response = int(input())

if response == 1:
    fractal_aggregation_using_radius_of_gyration()

elif response == 2:
    fractal_aggregation_using_gamma()