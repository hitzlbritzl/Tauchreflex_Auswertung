import impedance
from impedance import preprocessing
from impedance.models.circuits import CustomCircuit
import os

import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist
#Ablageordner für die beiden Dateien, hab einen Pfad genommen der schön kurz ist
directory = r'C:\Tauchreflexdaten'

#Sicherheitshalber das Arbeitsverzeichnis auf den Ablageordner gewechselt, man weiss ja nie
os.chdir(directory)
# Load data from the example EIS data
frequencies, Z = preprocessing.readPowerSuite'./021_BED1_LA_LEER.RAW_SIGNALS.rawICG.txt')

# keep only the impedance data in the first quadrant
frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)
circuit = 'R0-p(R1,C1)-p(R2-Wo1,C2)'
initial_guess = [.01, .01, 100, .01, .05, 100, 1]

circuit = CustomCircuit(circuit, initial_guess=initial_guess)
circuit.fit(frequencies, Z)
Z_fit = circuit.predict(frequencies)
fig, ax = plt.subplots()
plot_nyquist(Z, fmt='o', scale=10, ax=ax)
plot_nyquist(Z_fit, fmt='-', scale=10, ax=ax)

plt.legend(['Data', 'Fit'])
plt.show()
