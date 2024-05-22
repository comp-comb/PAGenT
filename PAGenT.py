import random
import matplotlib.pyplot as plt
import numpy as np
import customtkinter
from PIL import Image

def center_of_mass(p, x, y, z): # This is a function that finds the average of the coordinates
    cm_x = sum(x) / len(p) # Finds the average x coordinate
    cm_y = sum(y) / len(p) # Finds the average y coordinate
    cm_z = sum(z) / len(p) # Finds the average z coordinate
    return cm_x, cm_y, cm_z # Returns the coordinates in the form of a point

def new_center_of_mass(x, y, z, r, p, n): # n should be an integer (n can be changed to 1 - geometric, 2 - area, 3 - mass based)
    sum_x = 0
    sum_y = 0
    sum_z = 0
    sum_r = 0
    for i in range(len(p)):
        sum_x += x[i] * r[i]**n
        sum_y += y[i] * r[i]**n
        sum_z += z[i] * r[i]**n
        sum_r += r[i]**n
    cm_x = sum_x / sum_r
    cm_y = sum_y / sum_r
    cm_z = sum_z / sum_r
    return cm_x, cm_y, cm_z

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

    plt.savefig('Particle.png')
    plt.show() # Finally, Shows the plot

def fractal_aggregation_using_gamma(): # This aggregation methods uses gamma to find intersecting particles
    global n_p # Asks the user how many particles they want to place
    global frp
    global trp # Asks the user what they want the radius of the particle to be
    global df_t # Ask the user what they want the target fractal dimension to be


    particle_list = [] # Creates a list for the particles to be placed
    ran_num_rp = random.uniform(frp, trp)
    particle_list.append([0, 0, 0, ran_num_rp]) # Places a particle in the center of the plot
    ran_num_rp = random.uniform(frp, trp)
    particle_list.append(sphere_surface_placement(0, 0, 0, particle_list[0][3], ran_num_rp)) # Finds another particle to place on the surface of the original particle
    max_try = 20 # Sets the max number of times the program will try a particle and try to find a particle


    x = []  # New list for each x coordinate of the spheres
    y = []  # New list for each y coordinate of the spheres
    z = []  # New list for each z coordinate of the spheres
    r = []
    intersecting_list = [] # New list for the intersecting particles
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0 # Resets the conditional for the following loop

        while counter_2 < max_try: # If the number of times function is run exceeds the max_try number, then the program will stop trying to find a particle
            intersecting_list.clear() # Clears the interesting circle list so that the program and find a new list of interesting circles for the new particle
            x.clear() # Clears the x list
            y.clear() # Clears the y list
            z.clear() # Clears the z list
            r.clear()

            for i in range(len(particle_list)):  # Finds the x, y, and z coordinates of the particles
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's
                r.append(particle_list[i][3])

            ran_num_rp = random.uniform(frp, trp)
            # cm = center_of_mass(particle_list, x, y, z) # Finds the current center of mass of the particle
            cm = new_center_of_mass(x, y, z, r, particle_list, 1)
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


    cm_final = center_of_mass(particle_list, x, y, z) # Finds the final center of mass
    rog_final = radius_of_gyration(particle_list, cm_final) # Finds the final radius of gyration
    print('Final Radius of Gyration:', rog_final) # Prints the radius of gyration
    df = fractal_dimension(n_p, sum(r)/len(particle_list), rog_final) # Finds the final fractal dimension
    print('Fractal Dimension:', df) # Prints the final fractal dimension
    for i in range(len(particle_list)): # Prints the list of particles
        print(f'Particle {i + 1}:', particle_list[i] ,'') # Printing each particle individually
        file.write(str(f'Particle {i + 1}: '+str(particle_list[i])+'\n')) # Writing each particle in the text file

    plot_spheres(particle_list) # Finally, plots the particles and shows that plot
    file.close() # Closes the file
    root2 = customtkinter.CTk()  # This is the GUI pop-up
    root2.geometry('750x400')  # Sets the dimensions for the window that will pop up (in pixels)
    root2.resizable(width=False, height=False)
    root2.title('Fractal Aggregation Particle List')  # Sets the title for the pop-up window
    GUI_background2 = customtkinter.CTkImage(dark_image=Image.open('GUI background.jpg'), size=(800,500))
    GUI_label2 = customtkinter.CTkLabel(master=root2, image=GUI_background2)
    GUI_label2.place(x=0, y=0, relwidth=1, relheight=1)
    frame2 = customtkinter.CTkFrame(master=root2)  # Makes a frame inside the root window
    frame2.pack(pady=20, padx=60, fill='both', expand='true')  # Makes the frame appear
    GUI_particle_list = customtkinter.CTkTextbox(master=frame2, width=650,
                                                 height=400)  # When the window opens, this text will display for the user
    GUI_particle_list.pack()
    for i in range(len(particle_list)):  # Prints the particle list
        GUI_particle_list.insert(0.0, f'Particle {i+1}: {particle_list[i]}\n')  # Writing each particle in the text file
    root2.mainloop()

def fractal_aggregation_using_radius_of_gyration(): # This aggregation methods uses radius of gyration to find intersecting particles
    global n_p # Asks the user the number of particles they want to create
    global frp # Asks teh use what they want the radius of the particles to be
    global trp


    particle_list = [] # Creates a list for those particles
    ran_num_rp = random.uniform(frp, trp)
    particle_list.append([0, 0, 0, ran_num_rp]) # Particle placed in the center of the box
    ran_num_rp = random.uniform(frp, trp)
    particle_list.append(sphere_surface_placement(0, 0, 0, particle_list[0][3], ran_num_rp)) # Finds a particles on the surface of the original particle
    max_try = 20 # Sets the number of times the program will try a particle and try to find a new particle


    x = []  # New list for each x coordinate of the particles
    y = []  # New list for each y coordinate of the particles
    z = []  # New list for each z coordinate of the particles
    r = []
    intersecting_list = [] # Creates a list for the intersecting particles
    works = False  # Sets the condition for the following loops

    for i in range(n_p - 2):  # This is the loop that will run the sphere placement function the designated number of times the user wanted
        counter_2 = 0 # Sets the conditional for the following loop

        while counter_2 < max_try:  # If the number of times function is run exceeds the max_try number, then the program will stop trying to find a particle
            intersecting_list.clear()  # Clears the interesting circle list so that the program and find a new list of interesting circles for the new particle
            x.clear()  # Clears the x list
            y.clear()  # Clears the y list
            z.clear()  # Clears the z list
            r.clear()

            for i in range(len(particle_list)):  # Finds the x, y, and z coordinates of the current particles
                x.append(particle_list[i][0])  # Puts every x coordinate in that new list of x's
                y.append(particle_list[i][1])  # Puts every y coordinate in that new list of y's
                z.append(particle_list[i][2])  # Puts every z coordinate in that new list of z's
                r.append(particle_list[i][3])

            ran_num_rp = random.uniform(frp, trp)
            # cm = center_of_mass(particle_list, x, y, z) # Finds the current center of mass
            cm = new_center_of_mass(x, y, z, r, particle_list, 1)
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


    cm_final = center_of_mass(particle_list, x, y, z) # Finds the final center of mass
    rog_final = radius_of_gyration(particle_list, cm_final) # Finds the final radius of gyration
    print('Final Radius of Gyration:', rog_final) # Prints the final radius of gyration
    df = fractal_dimension(n_p, sum(r)/len(particle_list), rog_final) # Finds the fractal dimension
    print('Fractal Dimension:', df) # Prints the fractal dimension
    for i in particle_list: # Prints the particle list
        print('', i, '') # Printing each particle individually
        file.write(str(i)+'\n') # Writing each particle in the text file


    plot_spheres(particle_list) # Finally, plots the particles and shows the plot
    file.close() # Closes the file
    root2 = customtkinter.CTk()  # This is the GUI pop-up
    root2.geometry('750x400')  # Sets the dimensions for the window that will pop up (in pixels)
    root2.resizable(width=False, height=False)
    root2.title('Fractal Aggregation Particle List')  # Sets the title for the pop-up window
    GUI_background2 = customtkinter.CTkImage(dark_image=Image.open('GUI background.jpg'), size=(800,500))
    GUI_label2 = customtkinter.CTkLabel(master=root2, image=GUI_background2)
    GUI_label2.place(x=0, y=0, relwidth=1, relheight=1)
    frame2 = customtkinter.CTkFrame(master=root2)  # Makes a frame inside the root window
    frame2.pack(pady=20, padx=60, fill='both', expand='true')  # Makes the frame appear
    GUI_particle_list = customtkinter.CTkTextbox(master=frame2, width=650, height=400)  # When the window opens, this text will display for the user
    GUI_particle_list.pack()
    for i in range(len(particle_list)): # Prints the particle list
        GUI_particle_list.insert(0.0,f'Particle {i+1}: {particle_list[i]}\n') # Writing each particle in the text file
    root2.mainloop()



kf = 1.5 # Sets the kf for the whole program
#  gamma_entry_value_decimals = False
file = open('Text-File.txt', mode = 'w') # Opens the file and makes it able to be written in, so we can use it in the code
customtkinter.set_appearance_mode('dark') # Sets the appearance for the GUI to dark mode
customtkinter.set_default_color_theme('dark-blue') # Sets the color for the widgets to dark blue

root = customtkinter.CTk() # This is the GUI pop-up
root.geometry('500x400') # Sets the dimensions for the window that will pop up (in pixels)
root.resizable(width=False, height=False)
root.title('Fractal Aggregation') # Sets the title for the pop-up window
GUI_background = customtkinter.CTkImage(dark_image = Image.open('GUI background.jpg'), size = (600,500))
GUI_label = customtkinter.CTkLabel(master = root, image = GUI_background)
GUI_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
frame = customtkinter.CTkFrame(master=root) # Makes a frame inside the root window
frame.pack(pady = 20, padx = 60, fill = 'both', expand = 'true') # Makes the frame appear

text1 = customtkinter.CTkLabel(master = frame, text = 'Do you want to generate an aggregate particle via method 1 that'
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text1.pack(pady = 0, padx = 0)
text2 = customtkinter.CTkLabel(master = frame, text = 'uses radius of gyration as a reference radius for growth (1) '
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text2.pack(pady = 0, padx = 0)
text3 = customtkinter.CTkLabel(master = frame, text = 'or method 2 that attempts to generate an aggregate'
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text3.pack(pady = 0, padx = 0)
text4 = customtkinter.CTkLabel(master = frame, text = 'with a target fractal dimension (2)?'
                              , width = 0, height = 0, corner_radius = 5) # When the window opens, this text will display for the user
text4.pack(pady = 0, padx = 0)

# function_input = customtkinter.CTkLabel(master=frame, text='Number of Particles'
#                                          , width=0, height=0, corner_radius=5) # When this funtion is called, this text will display for the user
# function_input.pack() # Declares the position for function_input
# function_input.pack_forget() # Hides function_input

def option_1(): # A list of commands that button 1 will go through when it is clicked

    text1.pack_forget() # Hides text
    text2.pack_forget() # Hides text
    text3.pack_forget() # Hides text
    text4.pack_forget() # Hides text
    button1.pack_forget() # Hides button
    button2.pack_forget() # Hides button
    rog_textbox1.pack()
    rog_entrybox1.pack()
    rog_slider1.pack()
    rog_textbox2.pack()
    rog_entrybox2.pack()
    rog_slider2.pack()
    rog_textbox3.pack()
    rog_entrybox3.pack()
    rog_slider3.pack()
    rog_submit_button.pack()
    # entry.pack() # Declares the entry box
    # entry.place(x=120, y=100) # Sets the position in the frame
    # slider.pack()
    # slider_label.pack()
    # rog_enter_button1.pack() # Declares the submit button
    # rog_enter_button1.place(x=120, y=150) # Sets the position in the frame
    # function_input.pack() # Declares the label
    # function_input.place(x=120, y=50) # Sets the position in the frame

button1 = customtkinter.CTkButton(master = frame, text = 'Option 1 (ROG)', command = option_1) # The button will pop up when the window is opened, and once clicked, it will run the option 1 function
button1.pack(pady = 50, padx = 10) # Declares the button

def option_2(): # A list of commands that button 2 will go through when it is clicked

    text1.pack_forget() # Hides text
    text2.pack_forget() # Hides text
    text3.pack_forget() # Hides text
    text4.pack_forget() # Hides text
    button1.pack_forget() # Hides button
    button2.pack_forget() # Hides button
    gm_textbox1.pack()
    gm_entrybox1.pack()
    gm_slider1.pack()
    gm_textbox2.pack()
    gm_entrybox2.pack()
    gm_slider2.pack()
    gm_textbox4.pack()
    gm_entrybox4.pack()
    gm_slider4.pack()
    gm_textbox3.pack()
    gm_entrybox3.pack()
    gm_slider3.pack()
    gm_submit_button.pack()
    # entry.pack() # Declares the entry box
    # entry.place(x=120, y=100) # Sets the position in the frame
    # slider.pack()
    # slider_label.pack()
    # gamma_enter_button1.pack() # Declares the submit button
    # gamma_enter_button1.place(x=120, y=150) # Sets the position in the frame
    # function_input.pack() # Declares the label
    # function_input.place(x=120, y=50) # Sets the position in the frame

button2 = customtkinter.CTkButton(master = frame, text = 'Option 2 (Gamma)', command = option_2) # The button will pop up when the window is opened, and once clicked, it will run the option 2 function
button2.pack(pady = 0, padx = 10) # Declares the button



rog_textbox1 = customtkinter.CTkLabel(master=frame, text = 'Number of Particles')
rog_textbox1.pack()
rog_textbox1.pack_forget()
rog_entrybox1 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Number of Particles')
rog_entrybox1.pack()
rog_entrybox1.pack_forget()
def rog_slider_command1(value):
    rog_entrybox1.delete(0, 100)
    rog_entrybox1.insert(0, int(value))
rog_slider1 = customtkinter.CTkSlider(master=frame, from_=1, to = 100, number_of_steps=99, command=rog_slider_command1)
rog_slider1.pack()
rog_slider1.pack_forget()



rog_textbox2 = customtkinter.CTkLabel(master=frame, text = 'Radius From')
rog_textbox2.pack()
rog_textbox2.pack_forget()
rog_entrybox2 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius From')
rog_entrybox2.pack()
rog_entrybox2.pack_forget()
def rog_slider_command2(value):
    rog_entrybox2.delete(0, 100)
    rog_entrybox2.insert(0, value)
rog_slider2 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=rog_slider_command2)
rog_slider2.pack()
rog_slider2.pack_forget()



rog_textbox3 = customtkinter.CTkLabel(master=frame, text = 'Radius To')
rog_textbox3.pack()
rog_textbox3.pack_forget()
rog_entrybox3 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius To')
rog_entrybox3.pack()
rog_entrybox3.pack_forget()
def rog_slider_command3(value):
    rog_entrybox3.delete(0, 100)
    rog_entrybox3.insert(0, value)
rog_slider3 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=rog_slider_command3)
rog_slider3.pack()
rog_slider3.pack_forget()

def rog_submit_button_command():
    global n_p
    global frp
    global trp
    n_p = int(rog_entrybox1.get())
    frp = float(rog_entrybox2.get())
    trp = float(rog_entrybox3.get())
    root.destroy()
    fractal_aggregation_using_radius_of_gyration()

rog_submit_button = customtkinter.CTkButton(master = frame, text = 'Submit', command = rog_submit_button_command)
rog_submit_button.pack()
rog_submit_button.pack_forget()



gm_textbox1 = customtkinter.CTkLabel(master=frame, text = 'Number of Particles')
gm_textbox1.pack()
gm_textbox1.pack_forget()
gm_entrybox1 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Number of Particles')
gm_entrybox1.pack()
gm_entrybox1.pack_forget()
def gm_slider_command1(value):
    gm_entrybox1.delete(0, 100)
    gm_entrybox1.insert(0, int(value))
gm_slider1 = customtkinter.CTkSlider(master=frame, from_=1, to = 100, number_of_steps=99, command=gm_slider_command1)
gm_slider1.pack()
gm_slider1.pack_forget()



gm_textbox2 = customtkinter.CTkLabel(master=frame, text = 'Radius From')
gm_textbox2.pack()
gm_textbox2.pack_forget()
gm_entrybox2 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius From')
gm_entrybox2.pack()
gm_entrybox2.pack_forget()

def gm_slider_command2(value):
    gm_entrybox2.delete(0, 100)
    gm_entrybox2.insert(0, value)
gm_slider2 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=gm_slider_command2)
gm_slider2.pack()
gm_slider2.pack_forget()



gm_textbox4 = customtkinter.CTkLabel(master=frame, text = 'Radius To')
gm_textbox4.pack()
gm_textbox4.pack_forget()
gm_entrybox4 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Radius To')
gm_entrybox4.pack()
gm_entrybox4.pack_forget()
def gm_slider_command4(value):
    gm_entrybox4.delete(0, 100)
    gm_entrybox4.insert(0, value)
gm_slider4 = customtkinter.CTkSlider(master=frame, from_=1, to=5, number_of_steps=4, command=gm_slider_command4)
gm_slider4.pack()
gm_slider4.pack_forget()



gm_textbox3 = customtkinter.CTkLabel(master=frame, text = 'Fractal Dimension')
gm_textbox3.pack()
gm_textbox3.pack_forget()
gm_entrybox3 = customtkinter.CTkEntry(master=frame, placeholder_text = 'Fractal Dimension')
gm_entrybox3.pack()
gm_entrybox3.pack_forget()
def gm_slider_command3(value):
    gm_entrybox3.delete(0, 100)
    gm_entrybox3.insert(0, value)
gm_slider3 = customtkinter.CTkSlider(master=frame, from_=1.5, to=3, number_of_steps=8, command=gm_slider_command3)
gm_slider3.pack()
gm_slider3.pack_forget()

def gm_submit_button_command():
    global n_p
    global frp
    global trp
    global df_t
    n_p = int(gm_entrybox1.get())
    frp = float(gm_entrybox2.get())
    trp = float(gm_entrybox4.get())
    df_t = float(gm_entrybox3.get())
    root.destroy()
    fractal_aggregation_using_gamma()

gm_submit_button = customtkinter.CTkButton(master = frame, text = 'Submit', command = gm_submit_button_command)
gm_submit_button.pack()
gm_submit_button.pack_forget()
# entry = customtkinter.CTkEntry(master = frame, placeholder_text = 'Click Here') # This is will make an entry box for the user to submit their numbers, when asked
# entry.pack() # Declares the entry box
# entry.pack_forget() # Hides the entry box
#
# def slider_option1(value):
#     global entry
#     entry.delete(0, 100)
#     if gamma_entry_value_decimals == True:
#         entry.insert(0, value)
#         slider_label.configure(text = value)
#     else:
#         entry.insert(0, int(value))
#         slider_label.configure(text = int(value))
#
# slider = customtkinter.CTkSlider(master = frame, from_= 1, to = 100, number_of_steps = 99, command = slider_option1)
# slider.pack(pady = 20)
# slider.pack_forget()
# slider_label = customtkinter.CTkLabel(master = frame, text = '')
# slider_label.pack(pady = 0)
# slider_label.pack_forget()
#
# # Radius of Gyration's buttons
# def rog_enter_button_command1(): # This will be run after the user has clicked the button for the first prompt
#     global n_p # Sets the variable in this function to be a global variable, which can be used throughout different functions
#     n_p = int(entry.get()) # Sets the global n_p to whatever the user typed
#     function_input.configure(text = 'Radius of Particles') # Changes the text of the label
#     rog_enter_button1.pack_forget() # Hides the first button
#     entry.delete(0, 1000000000) # Deletes all the characters that the user typed in
#     rog_enter_button2.pack() # Declares the second button
#     rog_enter_button2.place(x=120, y=150) # Sets the position of the second button
#     slider.configure(from_ = 1, to = 5, number_of_steps = 4)
#
# rog_enter_button1 = customtkinter.CTkButton(master = frame, text = 'SUBMIT', command = rog_enter_button_command1) # This is the first button for the first ROG prompt
# rog_enter_button1.pack() # Declares the button
# rog_enter_button1.pack_forget() # Hides the button
#
# def rog_enter_button_command2(): # This will be run after the user has clicked the button for the second prompt
#     global rp # Sets the variable in this function to be a global variable, which can be used throughout different functions
#     rp = float(entry.get()) # Sets the global rp to whatever the user typed
#     root.destroy() # Closes the GUI
#     fractal_aggregation_using_radius_of_gyration() # Runs the radius of gyration aggregation method using the variable gathered
#
# rog_enter_button2 = customtkinter.CTkButton(master = frame, text = 'SUBMIT', command = rog_enter_button_command2) # This is the second button for the second ROG prompt
# rog_enter_button2.pack() # Declares the button
# rog_enter_button2.pack_forget() # Hides the button
#
# # Gamma's buttons
# def gamma_enter_button_command1(): # This will be run after the user has clicked the button for the first prompt
#     global n_p # Sets the variable in this function to be a global variable, which can be used throughout different functions
#     n_p = int(entry.get()) # Sets the global n_p to whatever the user typed
#     function_input.configure(text = 'Radius of Particles') # Changes the text of the label
#     gamma_enter_button1.pack_forget() # Hides the first button
#     entry.delete(0, 1000000000) # Deletes all the characters that the user typed in
#     gamma_enter_button2.pack() # Declares the second button
#     gamma_enter_button2.place(x=120, y=150) # Sets the position of the second button
#     slider.configure(from_ = 1, to = 5, number_of_steps = 4)
#
# gamma_enter_button1 = customtkinter.CTkButton(master = frame, text = 'SUBMIT', command = gamma_enter_button_command1) # This is the first button for the first gamma prompt
# gamma_enter_button1.pack() # Declares the button
# gamma_enter_button1.pack_forget() # Hides the button
#
# def gamma_enter_button_command2(): # This will be run after the user has clicked the button for the second prompt
#     global rp # Sets the variable in this function to be a global variable, which can be used throughout different functions
#     rp = float(entry.get()) # Sets the global rp to whatever the user typed
#     function_input.configure(text = 'Fractal Dimension (1.5-3)') # Changes the text of the label
#     gamma_enter_button2.pack_forget() # Hides the second button
#     entry.delete(0, 1000000000) # Deletes all the characters that the user typed in
#     gamma_enter_button3.pack() # Declares the third button
#     gamma_enter_button3.place(x=120, y=150) # Sets the position of the third button
#     slider.configure(from_ = 1.5, to = 3, number_of_steps = 8)
#     global gamma_entry_value_decimals
#     gamma_entry_value_decimals = True
#
# gamma_enter_button2 = customtkinter.CTkButton(master = frame, text = 'SUBMIT', command = gamma_enter_button_command2) # This is the second button for the second gamma prompt
# gamma_enter_button2.pack() # Declares the button
# gamma_enter_button2.pack_forget() # Hides the button
#
# def gamma_enter_button_command3(): # This will be run after the user has clicked the button for the third prompt
#     global df_t # Sets the variable in this function to be a global variable, which can be used throughout different functions
#     df_t = float(entry.get()) # Sets the global df_t to whatever the user typed
#     root.destroy() # Closes the GUI
#     fractal_aggregation_using_gamma() # Runs the gamma aggregation method using the variable gathered
#
# gamma_enter_button3 = customtkinter.CTkButton(master = frame, text = 'SUBMIT', command = gamma_enter_button_command3) # This is the third button for the third gamma prompt
# gamma_enter_button3.pack() # Declares the button
# gamma_enter_button3.pack_forget() # Hides the button

root.mainloop() # Tells Python to run the GUI