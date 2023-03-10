"""Fit of an IIR filter to a frequency response of a second-order dynamic system.

Try to play with this script by changing the parameters of the 2nd order system or
the order of the fitted filter.

.. seealso:: :mod:`PyDynamic.model_estimation.fit_filter`
"""
import numpy as np
from matplotlib.pyplot import cla, figure, show
from PyDynamic.misc.filterstuff import db
from PyDynamic.misc.SecondOrderSystem import sos_FreqResp
from PyDynamic.model_estimation.fit_filter import LSIIR
from scipy.signal import freqz

# sensor/measuring system
f0 = 36e3  # system resonance frequency in Hz
S0 = 0.124  # system static gain
delta = 0.0055  # system damping

f = np.linspace(0, 80e3, 30)  # frequencies for fitting the system
Hvals = sos_FreqResp(S0, delta, f0, f)  # frequency response of the 2nd order system

# fitting the IIR filter
Fs = 500e3  # sampling frequency
Na = 4
Nb = 4  # IIR filter order (Na - denominator, Nb - numerator)

b, a, tau, _ = LSIIR(Hvals, Na, Nb, f, Fs)  # fit IIR filter to freq response

f_plot = np.linspace(0, 80e3, 1000)  # frequency range for the plot
Hc = sos_FreqResp(S0, delta, f0, f_plot)  # frequency response of the 2nd order system
Hf = freqz(b, a, 2 * np.pi * f_plot / Fs)[
    1
]  # frequency response of the fitted IIR filter
Hf = Hf * np.exp(
    2j * np.pi * f_plot / Fs * tau
)  # take into account the filter time delay tau

fig1 = figure(1)
cla()
ax1 = fig1.add_subplot(111)
ax1.plot(f_plot, db(Hc), "+", f_plot, db(Hf))
ax1.legend(("System", "LSIIR fit"))
ax1.set_xlabel("frequency / Hz", fontsize=18)
ax1.set_ylabel("freq. response amplitude / a.u.", fontsize=18)

fig2 = figure(2)
cla()
ax2 = fig2.add_subplot(111)
ax2.plot(f_plot, np.angle(Hc), "+", f_plot, np.angle(Hf))
ax2.legend(("System", "LSIIR fit"))
ax2.set_xlabel("frequency / Hz", fontsize=18)
ax2.set_ylabel("freq. response angle / rad", fontsize=18)

show()
