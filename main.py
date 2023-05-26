## Sicherstellen, dass alle Pakete installiert sind, vor allem neurokit2, pathlib und matplotlib
import neurokit2 as nk
from pathlib import Path
import pandas as pd
import os
import impedance
from impedance.models.circuits import CustomCircuit
from impedance import preprocessing
import numpy as np
from numpy import nan
from itertools import chain
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *

#Abfangen dass die Datentypen mal klein und mal gross sein können, nicht fertig
#DataFormats = ("n.txt", "N.TXT")

#Ablageordner für die beiden Dateien, hab einen Pfad genommen der schön kurz ist
directory = r'C:\Tauchreflexdaten'

#Sicherheitshalber das Arbeitsverzeichnis auf den Ablageordner gewechselt, man weiss ja nie
os.chdir(directory)

# get file paths of '.txt' files in DIRECTORY folder,
# hier werden die Pfadangaben zu den beiden Dateien in einer Variable namens fpaths gespeichert
fpaths = [i for i in Path.cwd().glob('*.txt')]
# da lasse ich mir ausgeben, welche Pfade er gespeichert hat, sicher ist sicher
print(fpaths)
# care about icg later, do ecg first!
# die Daten für icg sind in der zweiten Zeile in fpaths! also fpaths 1
icg = fpaths[1]
icg = icg.read_text()
icg = [float(i) for i in icg.split(',')[:-1]]

# load ecg data ('.txt') as df
ecg = fpaths[0]
ecg = ecg.read_text().split(',')[:-1]
ecg = np.array([float(i) for i in ecg]).reshape((len(ecg), 1))
ecg = pd.DataFrame(ecg, columns=['ECG'])
#print (ecg)
# run r-peak detection on ecg data:
peaks, info = nk.ecg_peaks(ecg, sampling_rate=1000)
peak_times = np.where(peaks['ECG_R_Peaks'] == 1)[0]
#print(peak_times)
# detect artifacts
artifact_times = []
for i in range(1, len(ecg) - 1):
    if ecg.iloc[i, 0] > ecg.iloc[i - 1, 0] and ecg.iloc[i, 0] > ecg.iloc[i + 1, 0] and ecg.iloc[i, 0] > 0.5 * max(
            ecg.iloc[:, 0]):
        artifact_times.append(i)
#print(artifact_times)
# plot artifacts
#for i in artifact_times:
 #   plt.axvline(i, color='green')

# mark artifacts
ecg_marked = ecg.copy()
ecg_marked.iloc[artifact_times, 0] = nan
print(ecg_marked)
# create final df
final_df = ecg_marked.copy()
final_df['ECG_R_Peaks'] = peaks['ECG_R_Peaks']
print(final_df)
plt.figure(figsize=(40, 10))
plt.plot(final_df["ECG_R_Peaks"])
plt.plot(ecg["ECG"])
for i in artifact_times:
    plt.axvline(i, color='green')
plt.show()

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
LARGE_FONT= ("Verdana", 12)
tkFenster = Tk()
tkFenster.title('ZumAusprobieren')
tkFenster.geometry('600x400')
#label = tk.Label(self, text = "EKG Daten", font=LARGE_FONT)
#label.pack(pady=10,padx=10)
#button1 = ttk.Button(self, text="Quit",
#                            command=lambda: controller.show_frame(StartPage))
#button1.pack()
tkFenster.mainloop()
self.figure = Figure(figsize=(100, 100), dpi=100)
self.axes = self.figure.add_subplot(111)
self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
self.canvas.get_tk_widget().pack()
def plotxy(ecg, x, y):
    ecg.axes.plot(x,y)
    ecg.canvas.draw()

def clearplot(self):
    self.axes.cla()
    self.canvas.draw()

 #def plotdata(ecg):
 #    x, y = ecg.getxy()
 #    pw.plotxy(x, y)

 #def clear():
 #    pw.clearplot()

 #if __name__ == "__main__":
 #    datgen = ecg()

     root = tk.Tk()

     mf = tk.Frame()
     pw = Plotwindow(mf, (200, 150))
     mf.pack()

     bf = tk.Frame()
     b1 = tk.Button(bf, text="Plot", command=plotdata)
     b1.pack(side=tk.LEFT)
     b2 = tk.Button(bf, text="Clear", command=clear)
     b2.pack(side=tk.LEFT)
     bf.pack()

     root.mainloop()


canvas = FigureCanvasTkAgg(f,self)
canvas.show()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas, self)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



'''circuit = impedance.preprocessing.readCHInstruments(fpaths[1])
#circuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200], circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-Wo_1')

#circuit.fit(icg)

print(circuit)
def plot_impedance_cardiography(data):
 #   """
#    Plots Impedance Cardiography data

    Parameters
    ----------
    data : array or list
        The array or list containing the impedance cardiography data

    """

    # Preprocess the impedance cardiography data
    icg_processed = nk.ecg_process(data, sampling_rate=500)

    # Plot the impedance cardiography data
    plt.figure(figsize=(40, 10))
    plt.plot(icg_processed["ICG"])
    plt.show()


plot_impedance_cardiography(icg)'''