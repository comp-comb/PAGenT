import numpy as np


def rodrigues_rot(B,C,global_z,A_loc):

    #define local z axis using segment between points B and C
    local_z = (B-C)/np.linalg.norm(B-C)
    #get vector which z axis rotates about between global and local 
    r = np.cross(global_z,local_z)
    #sin of angle
    s = np.linalg.norm(r)
    print('s:',s)
    #cos of angle
    c = np.dot(global_z,local_z)
    print('c:',c)
    #matrix for calculation of rodrigues rotation matrix
    K = np.array([[0,-r[2],r[1]],[r[2],0,-r[0]],[-r[1],r[0],0]])
    print('K:',K)
    #3x3 identity matrix
    I = np.eye(3)
    #rodrigues rotation matrix formula
    R = I + s*K +(1-c)*np.dot(K,K)
    print('Rotation Matrix', R)
    #apply rotation to local coords of point A
    A_rot = np.dot(R,A_loc)
    #apply translation to rotated points to obtain global coordinates of point A
    A_global = A_rot + C
    
    return A_global



#EXAMPLE UTILIZATION
#the input values here were just chosen by Dr. Roy and I to verify this method works. 
#use whatever calculation methods for each input as required. I have included some info for guidance if necessary


#this function requires 4 inputs:

#1. global z axis - we will define this as [0,0,1]
global_z = np.array([0,0,1])

#2. center of mass (global) for this aggregation step.
    #use whatever variable you have assigned to this point's calculation
    #using point 1.5,0,0 in this case
cm = np.array([1.5,0,0])

#3. global coordinates of point B.
    #this will be the coordinates of the particle retrieved from the intersecting particle list
    #defined as 3,0,0 in this case
B = np.array([3,0,0])

#4. local coordinates of A 
    #obtained through the spherical coordinate function we have been using
    # we will use -2.855,0,0.5811
A_loc = np.array([-2.855,0,0.5811])

#5. call function to obtain global coordinates of point A:
A_global = rodrigues_rot(B,cm,global_z,A_loc)
print('A global:', A_global)
