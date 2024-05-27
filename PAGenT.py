import random
import matplotlib.pyplot as plt
import numpy as np
import customtkinter
from PIL import Image

def new_center_of_mass(x, y, z, r, p, n): # n should be an integer (n can be changed to 1 - geometric, 2 - area, 3 - mass based)
    sum_x = 0 # Sets the sum of the x coordinates to zero
    sum_y = 0 # Sets the sum of the y coordinates to zero
    sum_z = 0 # Sets the sum of the z coordinates to zero
    sum_r = 0 # Sets the sum of the radii to zero
    for i in range(len(p)): # Equation for the center of mass
        sum_x += x[i] * r[i]**n # Equation for the center of mass
        sum_y += y[i] * r[i]**n # Equation for the center of mass
        sum_z += z[i] * r[i]**n # Equation for the center of mass
        sum_r += r[i]**n # Equation for the center of mass
    cm_x = sum_x / sum_r # Equation for the center of mass
    cm_y = sum_y / sum_r # Equation for the center of mass
    cm_z = sum_z / sum_r # Equation for the center of mass
    return cm_x, cm_y, cm_z # Returns the new center of mass

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

        if (rog - rp[i]) <= dist <= (rp[i] + rog): # If the distance meets this conditional, then the sphere will be labeled as touching the rog sphere
            intersecting_list.append(particle_list[i]) # Adds the particles that were touching the rog sphere to a new list

def fractal_dimension(n_p, rp, rog_f): # This function will calculate the fractal dimension of the calculated particle
    df = (np.log(n_p / kf)) / (np.log(rog_f / rp)) # The equation for calculating the fractal dimension
    return df # Returns the fractal dimension number

def sphere_surface_placement(x, y, z, r1, r): # Finds a new sphere that is randomly placed on the outside of a chosen sphere
    p = r1 + r #
    ang_1 = random.uniform(-np.pi / 2, np.pi / 2) # Finds a random angle
    ang_2 = random.uniform(0, 2 * np.pi) # Finds a second random angle

    Nx = x + p * (np.sin(ang_1) * np.cos(ang_2)) # Finds the x coordinate of a sphere that is touching the selected sphere
    Ny = y + p * (np.sin(ang_1) * np.sin(ang_2)) # Finds the y coordinate of a sphere that is touching the selected sphere
    Nz = z + p * (np.cos(ang_1)) # Finds the z coordinate of a sphere that is touching the selected sphere

    return Nx, Ny, Nz, r # Returns these coordinates together

def gamma(n_p, rp, df_target): # Finds the gamma of the particle
    gm = np.sqrt((((n_p**2 * rp**2) / (n_p - 1)) * (n_p / kf)**(2 / df_target)) - ((n_p * rp**2) / (n_p - 1)) - (n_p * rp**2) * ((n_p - 1) / kf)**(2 / df_target)) # Gamma equation

    return gm # Returns the gamma

def plot_spheres(particles): # Plots the particles using matplotlib
    fig = plt.figure() # Starts the plot for the figure and sets it equal to the fig variable
    ax = fig.add_subplot(projection='3d') # Makes the axes for the plot and sets it equal to the ax variable

    for i in range(len(particles)): # Starts a loop that will create a circle with a correctly plotted radius
        u,v = np.mgrid[0:2 * np.pi:50j, 0:np.pi:50j] # Creates a mesh gird of the sphere

        x = particles[i][3] * np.cos(u) * np.sin(v) + particles[i][0] # Creates the x coordinate for a particle with the correct radius
        y = particles[i][3] * np.sin(u) * np.sin(v) + particles[i][1] # Creates the y coordinate for a particle with the correct radius
        z = particles[i][3] * np.cos(v) + particles[i][2] # Creates the z coordinate for a particle with the correct radius

        color = np.random.choice(['g', 'b', 'r', 'y']) # Chooses a random color for the particles
        alpha = 0.5 # Sets alpha (transparency)

        ax.plot_surface(x, y, z, color=color, alpha=alpha) # Plots the particle using the coordinates with the correct radius and the random color and alpha

    ax.set_xlabel('X') # Labels the X axis as X
    ax.set_ylabel('Y') # Labels the Y axis as Y
    ax.set_zlabel('Z') # Labels the Z axis as Z
    ax.set_title('Spheres') # Titles the plot as Spheres
    ax.set_aspect('equal') # Sets the rate that the axes changes to change automatically

    plt.savefig('Particle.png') # Saves the figure in the png file
    plt.show() # Finally, Shows the plot

def fractal_aggregation_using_gamma(): # This aggregation methods uses gamma to find intersecting particles
    global n_p # Asks the user how many particles they want to place
    global frp # Asks the user what radius they want to start at
    global trp # Asks the user what radius they want to end at
    global df_t # Ask the user what they want the target fractal dimension to be


    particle_list = [] # Creates a list for the particles to be placed
    ran_num_rp = random.uniform(frp, trp) # Finds a random radius in the range of the user's choice
    particle_list.append([0, 0, 0, ran_num_rp]) # Places a particle in the center of the plot
    ran_num_rp = random.uniform(frp, trp) # Finds a random radius in the range of the user's choice
    particle_list.append(sphere_surface_placement(0, 0, 0, particle_list[0][3], ran_num_rp)) # Finds another particle to place on the surface of the original particle
    max_try = 20 # Sets the max number of times the program will try a particle and try to find a particle


    x = []  # New list for each x coordinate of the spheres
    y = []  # New list for each y coordinate of the spheres
    z = []  # New list for each z coordinate of the spheres
    r = []  # New list for each radius of the spheres
    intersecting_list = [] # New list for the intersecting particles
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0 # Resets the conditional for the following loop

        while counter_2 < max_try: # If the number of times function is run exceeds the max_try number, then the program will stop trying to find a particle
            intersecting_list.clear() # Clears the interesting circle list so that the program and find a new list of interesting circles for the new particle
            x.clear() # Clears the x list
            y.clear() # Clears the y list
            z.clear() # Clears the z list
            r.clear() # Clears the r list

            for i in range(len(particle_list)):  # Finds the x, y, and z coordinates of the particles
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's
                r.append(particle_list[i][3])  # Puts every radi in that new list of r's

            ran_num_rp = random.uniform(frp, trp) # Finds a random radius in the range of the user's choice
            cm = new_center_of_mass(x, y, z, r, particle_list, 1) # Finds the center of mass of the current particle in the loop
            gm = gamma(len(particle_list), sum(r)/len(particle_list), df_t) # Finds the current gamma of the particle

            intersecting_circles(particle_list, r, intersecting_list, cm, gm) # Finds the particles that are interesting
            ran_num = random.randrange(len(intersecting_list)) # Chooses a random sphere in the interesting particle list
            counter = 0  # Resetting the counter to zero because the function is making a new circle

            while counter < max_try:  # Stops the function once the number of times the function has tried to find a point exceeds the max_try
                points = sphere_surface_placement(intersecting_list[ran_num][0], intersecting_list[ran_num][1], intersecting_list[ran_num][2], intersecting_list[ran_num][3], ran_num_rp)  # Finds the coordinates for the new particle
                works = False  # Resets the condition so false, so we can define when the point meets criteria

                for i in range(len(particle_list)):  # Runs the loop, which finds the distance for each particle
                    dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], points[0], points[1], points[2])  # Finds the distance between each particle

                    if dist >= particle_list[i][3] + points[3]:  # If the distance is greater than or equal to the two particle's radiis, then the particles are not crossing
                        works = True  # If this condition is met, then those particle's points don't cross, and it works

                    else:  # Sets the second condition that if the particles crosses another particle, run this line of code
                        counter += 1  # Adds one to the counter for everytime the function fails to find a point where the particle can be placed
                        works = False  # If the particle does not meet the requirement of being greater than or equal to one sphere, then it does not work, so work is set to False
                        break  # The function will then break the loop and try finding a new point

                if works == True:  # If all points are True after the loop has finished, it will then run these lines
                    particle_list.append(points)  # The new particle that met all the requirements will be appended (added) to the list of other eligible particles
                    break  # Breaks the loop and starts the process of finding another particle

            if works == False:  # If the loop has ended because the program can't find another eligible point, it will run this line
                print(f'Could not place a new particle after {max_try} attempts')  # This prints that the program tried max_try times to find a particle
                counter_2 += 1 # Adds 1 to the conditional

            if works == True: # If the function found a particle
                break # It breaks out of the function
        if works == False: # If the function did not find a particle
            print(f'Could not place a new particle after {max_try} x {max_try} attempts') # It prints that it could not find coordinates that worked for a particle and could not find another particle
    print(f'Placed {len(particle_list)} particles')  # Gives the user a message telling them the number of particles placed


    cm_final = new_center_of_mass(x, y, z, r, particle_list, 1) # Finds the final center of mass
    rog_final = radius_of_gyration(particle_list, cm_final) # Finds the final radius of gyration
    print('Final Radius of Gyration:', rog_final) # Prints the radius of gyration
    df = fractal_dimension(n_p, sum(r)/len(particle_list), rog_final) # Finds the final fractal dimension
    print('Fractal Dimension:', df) # Prints the final fractal dimension
    for i in range(len(particle_list)): # Prints the list of particles
        print(f'Particle {i + 1}:', particle_list[i] ,'') # Printing each particle individually
        file.write(str(f'Particle {i + 1}: '+str(particle_list[i])+'\n')) # Writing each particle in the text file

    plot_spheres(particle_list) # Plots the particles and shows that plot
    file.close() # Closes the file
    root2 = customtkinter.CTk()  # This is the GUI pop-up
    root2.geometry('750x400')  # Sets the dimensions for the window that will pop up (in pixels)
    root2.resizable(width=False, height=False) # Doesn't allow the GUI Window to be changed
    root2.title('Fractal Aggregation Particle List')  # Sets the title for the pop-up window
    GUI_background2 = customtkinter.CTkImage(dark_image=Image.open('GUI background.jpg'), size=(800,500)) # Sets the background for the GUI
    GUI_label2 = customtkinter.CTkLabel(master=root2, image=GUI_background2) # Sets the background for the GUI
    GUI_label2.place(x=0, y=0, relwidth=1, relheight=1) # Places the background in the GUI
    frame2 = customtkinter.CTkFrame(master=root2)  # Makes a frame inside the root window
    frame2.pack(pady=20, padx=60, fill='both', expand='true')  # Makes the frame appear
    GUI_particle_list = customtkinter.CTkTextbox(master=frame2, width=650,
                                                 height=400)  # When the window opens, this text will display for the user
    GUI_particle_list.pack() # Declares the GUI Particle List
    for i in range(len(particle_list)):  # Prints the particle list
        GUI_particle_list.insert(0.0, f'Particle {i+1}: {particle_list[i]}\n')  # Writing each particle in the text file
    root2.mainloop() # Declares the GUI

def fractal_aggregation_using_radius_of_gyration(): # This aggregation methods uses radius of gyration to find intersecting particles
    global n_p # Asks the user the number of particles they want to create
    global frp # Asks the user what they want the starting radius to be
    global trp # Asks the user what they want the end radius to be


    particle_list = [] # Creates a list for those particles
    ran_num_rp = random.uniform(frp, trp) # Finds a random radius from the start and end radius
    particle_list.append([0, 0, 0, ran_num_rp]) # Particle placed in the center of the box
    ran_num_rp = random.uniform(frp, trp) # Finds a random radius from the start and end radius
    particle_list.append(sphere_surface_placement(0, 0, 0, particle_list[0][3], ran_num_rp)) # Finds a particles on the surface of the original particle
    max_try = 20 # Sets the number of times the program will try a particle and try to find a new particle


    x = []  # New list for each x coordinate of the particles
    y = []  # New list for each y coordinate of the particles
    z = []  # New list for each z coordinate of the particles
    r = []  # new list for each radius of the particles
    intersecting_list = [] # Creates a list for the intersecting particles
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0 # Sets the conditional for the following loop

        while counter_2 < max_try:  # If the number of times function is run exceeds the max_try number, then the program will stop trying to find a particle
            intersecting_list.clear()  # Clears the interesting circle list so that the program and find a new list of interesting circles for the new particle
            x.clear()  # Clears the x list
            y.clear()  # Clears the y list
            z.clear()  # Clears the z list
            r.clear()  # Clears the r list

            for i in range(len(particle_list)):  # Finds the x, y, and z coordinates of the current particles
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's
                r.append(particle_list[i][3])  # Puts every radius in that new list of r's

            ran_num_rp = random.uniform(frp, trp) # Finds a random radius from the start and end radius
            cm = new_center_of_mass(x, y, z, r, particle_list, 1) # Finds the center of mass of the particle in each loop
            rog = radius_of_gyration(particle_list, cm) # Finds the current radius of gyration

            intersecting_circles(particle_list, r, intersecting_list, cm, rog) # Finds the particles that are intersecting
            ran_num = random.randrange(len(intersecting_list)) # Chooses a random particle from the intersecting particle list
            counter = 0  # Resetting the counter to zero because the function is making a new particle

            while counter < max_try:  # Stops the function once the number of times the function has tried to find a point exceeds the max_try
                points = sphere_surface_placement(intersecting_list[ran_num][0], intersecting_list[ran_num][1], intersecting_list[ran_num][2], intersecting_list[ran_num][3], ran_num_rp)  # Finds the coordinates for the new particle
                works = False  # Resets the condition so false, so we can define when the point meets criteria

                for i in range(len(particle_list)):  # Runs the loop, which finds the distance for each particle
                    dist = distance(particle_list[i][0], particle_list[i][1], particle_list[i][2], points[0], points[1], points[2])  # Finds the distance between each particle

                    if dist >= particle_list[i][3] + points[3]:  # If the distance is greater than or equal to the two particle's radii, then the particles are not crossing
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


    cm_final = new_center_of_mass(x, y, z, r, particle_list, 1) # Finds the final center of mass
    rog_final = radius_of_gyration(particle_list, cm_final) # Finds the final radius of gyration
    print('Final Radius of Gyration:', rog_final) # Prints the final radius of gyration
    df = fractal_dimension(n_p, sum(r)/len(particle_list), rog_final) # Finds the fractal dimension
    print('Fractal Dimension:', df) # Prints the fractal dimension
    for i in particle_list: # Prints the particle list
        print('', i, '') # Printing each particle individually
        file.write(str(i)+'\n') # Writing each particle in the text file


    plot_spheres(particle_list) # Plots the particles and shows the plot
    file.close() # Closes the file
    root2 = customtkinter.CTk()  # This is the GUI pop-up
    root2.geometry('750x400')  # Sets the dimensions for the window that will pop up (in pixels)
    root2.resizable(width=False, height=False) # Doesn't allow the GUI window to be changed
    root2.title('Fractal Aggregation Particle List')  # Sets the title for the pop-up window
    GUI_background2 = customtkinter.CTkImage(dark_image=Image.open('GUI background.jpg'), size=(800,500)) # Sets the background for the GUI
    GUI_label2 = customtkinter.CTkLabel(master=root2, image=GUI_background2) # Sets the background for the GUI
    GUI_label2.place(x=0, y=0, relwidth=1, relheight=1) # Places the GUI background in the GUI
    frame2 = customtkinter.CTkFrame(master=root2)  # Makes a frame inside the root window
    frame2.pack(pady=20, padx=60, fill='both', expand='true')  # Makes the frame appear
    GUI_particle_list = customtkinter.CTkTextbox(master=frame2, width=650, height=400)  # When the window opens, this text will display for the user
    GUI_particle_list.pack() # Declares the particle list
    for i in range(len(particle_list)): # Prints the particle list
        GUI_particle_list.insert(0.0,f'Particle {i+1}: {particle_list[i]}\n') # Writing each particle in the text file
    root2.mainloop() # Declares the GUI



kf = 1.5 # Sets the kf for the whole program
file = open('Text-File.txt', mode = 'w') # Opens the file and makes it able to be written in, so we can use it in the code
customtkinter.set_appearance_mode('dark') # Sets the appearance for the GUI to dark mode
customtkinter.set_default_color_theme('dark-blue') # Sets the color for the widgets to dark blue

root = customtkinter.CTk() # This is the GUI pop-up
root.geometry('500x400') # Sets the dimensions for the window that will pop up (in pixels)
root.resizable(width=False, height=False) # Doesn't allow the GUI window to be changed
root.title('Fractal Aggregation') # Sets the title for the pop-up window
GUI_background = customtkinter.CTkImage(dark_image = Image.open('GUI background.jpg'), size = (600,500)) # Sets the background for the GUI
GUI_label = customtkinter.CTkLabel(master = root, image = GUI_background) # Sets the background for the GUI
GUI_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) # Places the GUI background in the GUI
frame = customtkinter.CTkFrame(master=root) # Makes a frame inside the root window
frame.pack(pady = 20, padx = 60, fill = 'both', expand = 'true') # Makes the frame appear

text1 = customtkinter.CTkLabel(master = frame, text = 'Do you want to generate an aggregate particle via method 1 that'
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text1.pack(pady = 0, padx = 0) # Declares the text
text2 = customtkinter.CTkLabel(master = frame, text = 'uses radius of gyration as a reference radius for growth (1) '
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text2.pack(pady = 0, padx = 0) # Declares the text
text3 = customtkinter.CTkLabel(master = frame, text = 'or method 2 that attempts to generate an aggregate'
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text3.pack(pady = 0, padx = 0) # Declares the text
text4 = customtkinter.CTkLabel(master = frame, text = 'with a target fractal dimension (2)?'
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text4.pack(pady = 0, padx = 0) # Declares the text

def option_1(): # A list of commands that button 1 will go through when it is clicked

    text1.pack_forget() # Hides text
    text2.pack_forget() # Hides text
    text3.pack_forget() # Hides text
    text4.pack_forget() # Hides text
    button1.pack_forget() # Hides button
    button2.pack_forget() # Hides button
    rog_textbox1.pack() # Declares text
    rog_entrybox1.pack() # Declares entrybox
    rog_slider1.pack() # Declares slider
    rog_textbox2.pack() # Declares text
    rog_entrybox2.pack() # Declares entrybox
    rog_slider2.pack() # Declares slider
    rog_textbox3.pack() # Declares text
    rog_entrybox3.pack() # Declares entrybox
    rog_slider3.pack() # Declares slider
    rog_submit_button.pack() # Declares button

button1 = customtkinter.CTkButton(master = frame, text = 'Option 1 (ROG)', command = option_1) # The button will pop up when the window is opened, and once clicked, it will run the option 1 function
button1.pack(pady = 50, padx = 10) # Declares the button

def option_2(): # A list of commands that button 2 will go through when it is clicked

    text1.pack_forget() # Hides text
    text2.pack_forget() # Hides text
    text3.pack_forget() # Hides text
    text4.pack_forget() # Hides text
    button1.pack_forget() # Hides button
    button2.pack_forget() # Hides button
    gm_textbox1.pack() # Declares text
    gm_entrybox1.pack() # Declares entrybox
    gm_slider1.pack() # Declares slider
    gm_textbox2.pack() # Declares text
    gm_entrybox2.pack() # Declares entrybox
    gm_slider2.pack() # Declares slider
    gm_textbox4.pack() # Declares text
    gm_entrybox4.pack() # Declares entrybox
    gm_slider4.pack() # Declares slider
    gm_textbox3.pack() # Declares text
    gm_entrybox3.pack() # Declares entrybox
    gm_slider3.pack() # Declares slider
    gm_submit_button.pack() # Declares button

button2 = customtkinter.CTkButton(master = frame, text = 'Option 2 (Gamma)', command = option_2) # The button will pop up when the window is opened, and once clicked, it will run the option 2 function
button2.pack(pady = 0, padx = 10) # Declares the button



rog_textbox1 = customtkinter.CTkLabel(master=frame, text = 'Number of Particles') # Creates text above the number of particles entrybox
rog_textbox1.pack() # Declares text
rog_textbox1.pack_forget() # Hides text
rog_entrybox1 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Number of Particles') # Creates entrybox for the number of particles
rog_entrybox1.pack() # Declares entrybox
rog_entrybox1.pack_forget() # Hides entrybox
def rog_slider_command1(value): # Command for the slider
    rog_entrybox1.delete(0, 100) # Deletes all text in entrybox
    rog_entrybox1.insert(0, int(value)) # Inserts the value from the slider into the entrybox
rog_slider1 = customtkinter.CTkSlider(master=frame, from_=1, to = 100, number_of_steps=99, command=rog_slider_command1) # Creates the slider for the number of particles
rog_slider1.pack() # Declares slider
rog_slider1.pack_forget() # Hides slider



rog_textbox2 = customtkinter.CTkLabel(master=frame, text = 'Radius From') # Creates text above the from radius entrybox
rog_textbox2.pack() # Declares text
rog_textbox2.pack_forget() # Hides text
rog_entrybox2 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius From') # Creates entrybox for the from radius
rog_entrybox2.pack() # Declares entrybox
rog_entrybox2.pack_forget() # Hides entrybox
def rog_slider_command2(value): # Command for the slider
    rog_entrybox2.delete(0, 100) # Deletes all text in the entrybox
    rog_entrybox2.insert(0, value) # Inserts the value from the slider into the entrybox
rog_slider2 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=rog_slider_command2) # Creates the slider for the from radius
rog_slider2.pack() # Declares slider
rog_slider2.pack_forget() # Hides slider



rog_textbox3 = customtkinter.CTkLabel(master=frame, text = 'Radius To') # Creates the text above the to radius entrybox
rog_textbox3.pack() # Declares text
rog_textbox3.pack_forget() # Hides text
rog_entrybox3 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius To') # Creates enrtybox for the to raidus
rog_entrybox3.pack() # Declares entrybox
rog_entrybox3.pack_forget() # Hides entrybox
def rog_slider_command3(value): # Command for the slider
    rog_entrybox3.delete(0, 100) # Deletes all text in the entrybox
    rog_entrybox3.insert(0, value) # Inserts the value from the slider into the entrybox
rog_slider3 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=rog_slider_command3) # Creates the slider for the to radius
rog_slider3.pack() # Declares slider
rog_slider3.pack_forget() # Hides slider

def rog_submit_button_command(): # Command for submit button
    global n_p # Sets the n_p variable as a global variable
    global frp # Sets the frp variable as a global variable
    global trp # Sets the trp variable as a global variable
    n_p = int(rog_entrybox1.get()) # gets the variable from the entrybox
    frp = float(rog_entrybox2.get()) # gets the variable from the entrybox
    trp = float(rog_entrybox3.get()) # gets the variable from the entrybox
    root.destroy() # Gets rid of the GUI
    fractal_aggregation_using_radius_of_gyration() # Runs the fractal aggregation function

rog_submit_button = customtkinter.CTkButton(master = frame, text = 'Submit', command = rog_submit_button_command) # Creates the submit button
rog_submit_button.pack() # Declares submit button
rog_submit_button.pack_forget() # Hides submit button



gm_textbox1 = customtkinter.CTkLabel(master=frame, text = 'Number of Particles') # Creates the text above the number of particles entrybox
gm_textbox1.pack() # Declares text
gm_textbox1.pack_forget() # Hides text
gm_entrybox1 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Number of Particles') # Creates entrybox for the number of particles
gm_entrybox1.pack() # Declares entrybox
gm_entrybox1.pack_forget() # Hide entrybox
def gm_slider_command1(value): # Command for slider
    gm_entrybox1.delete(0, 100) # Deletes all text in the entrybox
    gm_entrybox1.insert(0, int(value)) # Inserts the value from the slider into the entrybox
gm_slider1 = customtkinter.CTkSlider(master=frame, from_=1, to = 100, number_of_steps=99, command=gm_slider_command1) # Creates the slider for the number of particles
gm_slider1.pack() # Declares slider
gm_slider1.pack_forget() # Hides slider



gm_textbox2 = customtkinter.CTkLabel(master=frame, text = 'Radius From') # Creates the text above the from radius entrybox
gm_textbox2.pack() # Declares text
gm_textbox2.pack_forget() # Hides text
gm_entrybox2 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius From') # Creates entryboxc for the from radius
gm_entrybox2.pack() # Declares entrybox
gm_entrybox2.pack_forget() # Hides entrybox

def gm_slider_command2(value): # Command for slider
    gm_entrybox2.delete(0, 100) # Deletes all text in the entrybox
    gm_entrybox2.insert(0, value) # Inserts the value from the slider into the entrybox
gm_slider2 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=gm_slider_command2) # Creates the slider for the from radius
gm_slider2.pack() # Decalres slider
gm_slider2.pack_forget() # Hides slider



gm_textbox4 = customtkinter.CTkLabel(master=frame, text = 'Radius To') # Creates the text above the to radius entrybox
gm_textbox4.pack() # Declares text
gm_textbox4.pack_forget() # Hides text
gm_entrybox4 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius To') # Creates entrybox for the to radius
gm_entrybox4.pack() # Declares entrybox
gm_entrybox4.pack_forget() # Hides entrybox
def gm_slider_command4(value): # Command for slider
    gm_entrybox4.delete(0, 100) # Deletes all text in the entrybox
    gm_entrybox4.insert(0, value) # Inserts the value from the slider into the entrybox
gm_slider4 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=gm_slider_command4) # Creates the slider for the to radius
gm_slider4.pack() # Declares slider
gm_slider4.pack_forget() # Hides slider



gm_textbox3 = customtkinter.CTkLabel(master=frame, text = 'Fractal Dimension') # Creates the text above the fractal dimension entrybox
gm_textbox3.pack() # Declares text
gm_textbox3.pack_forget() # Hides text
gm_entrybox3 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Fractal Dimension') # Creates fractal dimension entrybox
gm_entrybox3.pack() # Declares entrybox
gm_entrybox3.pack_forget() # Hides entrybox
def gm_slider_command3(value): # Command for slider
    gm_entrybox3.delete(0, 100) # Deletes all text in the entrybox
    gm_entrybox3.insert(0, value) # Inserts the value from the slider into the entrybox
gm_slider3 = customtkinter.CTkSlider(master=frame, from_=1.5, to=3, number_of_steps=8, command=gm_slider_command3) # Creates the sldier for the fractal dimension
gm_slider3.pack() # Declares slider
gm_slider3.pack_forget() # Hides slider

def gm_submit_button_command(): # Command for the submit button
    global n_p # Sets the n_p variable as a global variable
    global frp # Sets the frp variable as a global variable
    global trp # Sets the trp variable as a global variable
    global df_t # Sets the df_t variable as a global variable
    n_p = int(gm_entrybox1.get()) # gets the variable from the entrybox
    frp = float(gm_entrybox2.get()) # gets the variable from the entrybox
    trp = float(gm_entrybox4.get()) # gets the variable from the entrybox
    df_t = float(gm_entrybox3.get()) # gets the variable from the entrybox
    root.destroy() # Gets rid of the GUI
    fractal_aggregation_using_gamma() # Runs the fractal aggregation function

gm_submit_button = customtkinter.CTkButton(master = frame, text = 'Submit', command = gm_submit_button_command) # Creates the submit button
gm_submit_button.pack() # Declares submit button
gm_submit_button.pack_forget() # Hides submit button

root.mainloop() # Tells Python to run the GUI