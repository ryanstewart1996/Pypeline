    ## Python Code for Elevation Profile Calculation Equation
 

#renders the elevation profile code and performs outflow calculations
def render_qf(g,d,e,mu,rho):
    import numpy as np
    import outflow_code as oc
    import os
    #define constants
    g = 9.81 #gravitational constant
    valve_close_t = 240 #time it takes valves to close in seconds, based on ASME and CSA Z662 requirements

    #input turns the csv file into a 2D array
    #elvA is Array imported csv file, columns are x and y of elevation profile
    Elevation = np.genfromtxt(open('Elevation_Profile.csv', 'r'), delimiter=",",)
    #print(input)
    col1 = Elevation[:,0]
    col2 = Elevation[:,1]
    col3 = Elevation[:,2]
    #program runs left and right side of pipeline leak location seperately
    #so we flip[ the direction of both]
    flip1 = np.flip(col1,0)*(-1)
    flip2 = np.flip(col2,0)
    #Behind LHS (Left Hand Side)
    range = np.size(col1)
    qtotal=np.zeros(range)
    finalH=np.zeros(range)
    i=1
    while i<range:
        col1elv=col1[0:(i+1)]
        col2elv=col2[0:(i+1)]
        t=0
        valveoff=0
        [M,I]=[np.amax(col2elv), np.argmax(col2elv)]
        H=np.amax(col2elv)-col2elv[i]
        Z=col1elv[I]-col1elv[i]
        h1=col1elv[I]
        while (Z<0) & (H>0):
            if H > 0:
                v1 = oc.get_vel(g,d,H,(-Z),e,mu,rho)[0] # need to get in between reynold numbers...
                Q = v1*(3.14)*(d*d)/4
                qtotal[i] = qtotal[i]+(Q*0.03)
                h1 = h1+v1*0.03
                Z = Z+v1*0.03
                H = np.interp(h1, col1elv, col2elv)-col2elv[i]
                t=t+0.03
            #    print('going...')
            if H < (-1000):
                    h1 = h1+1000
                    Z = Z+1000
                    H = np.interp(h1, col1elv, col2elv)-col2elv[i]
            if H < 0 :
                h1 = h1+100
                Z = Z+100
                H = np.interp(h1, col1elv, col2elv)-col2elv[i]
            if (t>valve_close_t) & (valveoff==0): #to make programming easier, just turn this to on if you wanna see what it is like without valves
                valveoff=1
                list = np.zeros(i+1)
                h_list=0
                x=0
                while h_list < i:
                    x=h_list
                    list[h_list]=x
                    h_list += 1
                point=Z+col1elv[i]
                location = np.interp(point, col1elv, list)
                loc=int(round(location))
                print(loc)
                [y,loc]=new_Z_h1(i, col1elv, col3)
                if y>loc:
                    h1=col1elv[y]
                    Z=col1elv[y]-col1elv[i]
                    H = np.interp(h1, col1elv, col2elv)-col2elv[i]
                    print('location modified')
                else:
                    print('location not changed')
        i = i+1
        print(i,t, h1, Z)
    #End LHS
    
    #Begin RHS (Right Hand Side)
    qtotalright = np.zeros(range)
    finalH = np.zeros(range)
    i=512 #### LETS CHANGE THIS TO %!@ FOR TESTING REASONS.. DONT WANT IT TO RENDER EVERY TIME
    while i<range:
        col1elv = flip1[0:(i+1)];
        col2elv = flip2[0:(i+1)];
        t=0;
        valveoff=0
        [M,I]=[np.amax(col2elv), np.argmax(col2elv)]
        H=np.amax(col2elv)-col2elv[i]
        Z=col1elv[I]-col1elv[i]
        h1=col1elv[I]
        while (Z<0) & (H>0):
            if H > 0:
                v1 = oc.get_vel(g,d,H,(-Z),e,mu,rho)[0]
                Q = v1*(np.pi)*(d*d)/4
                qtotalright[i] = qtotalright[i]+(Q*0.03)
                h1 = h1+v1*0.03
                Z = Z+v1*0.03
                H = np.interp(h1, col1elv, col2elv)-col2elv[i]
                t=t+0.03
            if H < (-1000):
                h1 = h1+1000
                Z = Z+1000
                H = np.interp(h1, col1elv, col2elv)-col2elv[i]
            if H < 0 :
                h1 = h1+100
                Z = Z+100
                H = np.interp(h1, col1elv, col2elv)-col2elv[i]
            if (t>valve_close_t) & (valveoff==0):
                valveoff=1
                list = np.zeros(i+1)
                h_list=0
                x=0
                while h_list < i:
                    x=h_list
                    list[h_list]=x
                    h_list += 1
                point=Z+col1elv[i]
                location = np.interp(point, col1elv, list)
                loc=int(round(location))
                print(loc)
                [y,loc]=new_Z_h1(i, col1elv, col3)
                if y>loc:
                    h1=col1elv[y]
                    Z=col1elv[y]-col1elv[i]
                    H = np.interp(h1, col1elv, col2elv)-col2elv[i]
                    print('location modified')
                else:
                    print('location not changed')

        i = i+1
        print(i, t)
    #End RHS
    qfinal = qtotal+np.flip(qtotalright)
    qfinal = qfinal*6.28981 #convert cubic meters to barrels
    #print(qfinal) # we now get the same numbers as our MATLAB CODE in way less time
    # Writing above equation outputs to a csv file
    np.savetxt("qfinal.csv", qfinal, delimiter=",")

    return [qfinal, col1, col2]



#solve velocity without friction factor
def solve_v(g, d, H, Z):
    import numpy as np
    fric = 0.16 #good guess for firction factor
    v1 = np.sqrt(2*g*H)
    v1f = np.sqrt((2*g*H)/(1+(fric*Z/d)))
    return [v1, v1f]

#solve velocity with known friction factor
def solve_vwf(g, d, H, Z, f):
    import numpy as np
    v1 = np.sqrt(2*g*H)
    v1f = np.sqrt((2*g*H)/(1+(f*Z/d)))
    return [v1, v1f]


#viscosity of canadian crude is from 5-10 pascal seconds
def reynolds(a, rho, d, mu):
    Re = rho*a*d/mu
    return Re

def moody_f(Re, e, d):
    if Re > 2300 :
        f = 0.0055(1+((2*10000*e/d)+1000000/Re)**(1/3)) ##Moody Colebrook Equation Approximation
    if Re < 2300 :
        f= 64/Re
    return f

#solve for velocity with a friction factor using moody chart (even if you dont know the friction factor
def get_vel(g, d, H, Z, e, mu, rho):
    import outflow_code as oc
    i = 1
    vel = oc.solve_v(g, d, H, Z)
    Re = oc.reynolds(vel[1], rho, d, mu)
    f1 = oc.moody_f(Re, e, d)
    f=0.16
    while ((f1-f)/f<-0.1) | ((f1-f)/f>0.1):
        f=f1
        vel = oc.solve_vwf(g,d,H,Z,f)
        Re = oc.reynolds(vel[1], rho, d, mu)
        f1 = oc.moody_f(Re, e, d)
        i = i+1
    #print(i)
    return vel

#approximation of moody chart using Bellos, Nalbantis, Tsakiris approximation 
def bnt_f(Re, e, d):
    import numpy as np
    a = 1/(1+((Re/2712)**8.4))
    b = 1/(1+((Re/(150*d/e))**1.8))
    f = ((64/Re)**a)*((0.75*np.log(Re/5.37))**(1*(a-1)*b))*((0.88*np.log(6.82*d/e))**(2*(a-1)*(1-b))) #BNT approximatino
    return f

#if you hve valves along pipelien route, add them here
def new_Z_h1(i, col1elv, col3):
    import numpy as np
    list = np.zeros(i+1)
    h_list=0
    x=0
    while h_list < i:
        x=h_list
        list[h_list]=x
        h_list += 1
    point=Z+col1elv[i]
    location = np.interp(point, col1elv, list)
    loc=int(round(location))
        #loc=13 #would be the 14th point
    list = np.zeros(np.size(col1elv))
    list[loc]=1
    lI=np.argmax(list) # fnd index of where we the location is to modify valve array
    valset=np.concatenate([list[0:loc+1], col3[loc+1:]])#new array for solving
    valset[i] = 2
    q= 0
    x=0
    while valset[i-q]!=1:
        q=q+1
        x=i-q
    #print(x, lI)
    if x<0:
        return 0, loc
    if x>0:
        return x, loc
    if x==0:
        return x, loc



#H=10
#Z=93
#rho=1000
#mu=7.5
#e = 0.000015
#g=9.81
#d=0.5

