## Sicherstellen, dass alle Pakete installiert sind, vor allem neurokit2, pathlib und matplotlib
import neurokit2 as nk
from pathlib import Path
import pandas as pd
import os
import numpy as np
from numpy import nan
from itertools import chain
import matplotlib.pyplot as plt

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