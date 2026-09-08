import sys 
import os
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation 
from ProjectileMotion import *
from GUI import *

class GraphData:
    def __init__(self):
        self.window = ctk.CTk(fg_color="#1F1F29")
        self.window.wm_title("BPhO 2024")
        ctk.set_appearance_mode("Dark")

        self.fig = plt.figure()
        self.ax = plt.subplot()

        velocity = 10
        launchAngle = 45
        point = (10,5)
        launchHeight = 2
        self.graph = matPlotter(self.fig,self.ax)

        self.GUI = GUIHandler(self.window,self.graph)
        self.graph.GUI = self.GUI
        self.graph.load(velocity,launchAngle,point,launchHeight)
        self.GUI.load()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()

        self.fig.canvas.mpl_connect('key_press_event', self.graph.retreivekeyInputs)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

        self.window.update()
        self.window.mainloop()

graphData = GraphData()