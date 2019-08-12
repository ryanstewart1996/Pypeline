
def gui_out():

    import numpy as np
    import sys
    import matplotlib
    matplotlib.use('TkAgg')

    from numpy import arange, sin, pi
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    from matplotlib import style


    import tkinter as Tk
    root = Tk.Tk()
    root.wm_title("Outflow Analysis Tool")
    style.use('Solarize_Light2')


#this should be its own function
    Elevation = np.genfromtxt(open('Elevation_Profile.csv', 'r'), delimiter=",")
    c1 = Elevation[:,0]
    c2 = Elevation[:,1]
    c3 = Elevation[:,2]
    qf= np.genfromtxt(open('qfinal.csv', 'r'), delimiter=",")
    qv=np.genfromtxt(open('qfinalLHS.csv', 'r'), delimiter=",")



    f = Figure(figsize=(8, 6), dpi=100)
    ax = f.add_subplot(111)

    c13=c3*c1
    c13=c13[c13 !=0]
    c3=c3*c2
    c3=c3[c3 !=0 ]


    ax.plot(c1, c2, 'C0', c13, c3, 'rx', markersize=10)
    ax2 = ax.twinx()
    ax2.plot(c1, qf,'C6', c1, qv, 'g', markersize=1)
    #ax3=ax.twinx()
    #ax3.plot(c1, c3,'r--', markersize=2)
    ax.set_title('Elevation Profile and Maximum Outflow along Pipeline')
    ax.set_xlabel('Pipeline Chainage (meters)')
    ax.set_ylabel('Pipeline Elevation (meters)')
    ax.set_yscale('linear')
    ax2.set_yscale('linear')
    ax2.set_ylabel('Outflow (Barrels)')

    ax.legend(['Elevation Profile', 'Valves'], loc=2)
    ax2.legend(['Outflow no Valves', 'Outflow with\nValve Placement'], loc=1)


    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    button = Tk.Button(master=root, text='Quit', command=sys.exit)
    button.pack(side=Tk.BOTTOM)

    Tk.mainloop()


def mat_out():
        import numpy as np
        Elevation = np.genfromtxt(open('Elevation_Profile.csv', 'r'), delimiter=",")
        c1 = Elevation[:,0]
        c2 = Elevation[:,1]
        qf= np.genfromtxt(open('qfinal.csv', 'r'), delimiter=",")
        myList = np.matrix([c1, c2, qf])
        myList = np.transpose(myList)
        return myList
