from tkinter import Tk, StringVar
from tkinter import ttk
import matplotlib as mpl
mpl.use('TkAgg')  # back-end TkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from rigol import Generator, Scope

root = Tk()
root.title("RIGOL DG1022")

gen = Generator()
scope = Scope()

signal        = StringVar(value="SINE")   
freq          = StringVar(value="1000")   
amplitude     = StringVar(value="5.0")   
offset        = StringVar(value="1.0")
phase         = StringVar(value="0")
status        = StringVar(value="Not connected")

status_all    = StringVar(value = "Update All Values")
status_scope  = StringVar(value="Not connected")
status_freq   = StringVar(value = "No value yet")
status_vmax   = StringVar(value = "No value yet")
status_vamp   = StringVar(value = "No value yet")
status_duty   = StringVar(value = "No value yet")
status_ftime  = StringVar(value = "No value yet")
status_rtime  = StringVar(value = "No value yet")
status_vavg   = StringVar(value = "No value yet")
status_vrms    = StringVar(value = "No value yet")

ttk.Label(root, text="Select the signal and the value of the signal ").grid(row=0, column=0, columnspan=100, padx=5, pady=5, sticky="w")
ttk.Label(root, text="Signal").grid(row=5, column=0, padx=5, pady=5, sticky="w")
ttk.Combobox(root, textvariable=signal, values=["SINE", "SQUARE", "RAMP", "DC"],
            width=8).grid(row=5, column=10, padx=5, pady=5)

ttk.Entry(root, textvariable=freq, width=10).grid(row=10, column=100, padx=5, pady=5)
ttk.Label(root, text="Freq ").grid(row=10, column=90, padx=5, pady=5, sticky="w")
ttk.Label(root, text="Hz").grid(row=10, column=110, padx=5, pady=5, sticky="w")

ttk.Entry(root, textvariable=amplitude, width=10).grid(row=20, column=100, padx=5, pady=5)
ttk.Label(root, text="Amplitude").grid(row=20, column=90, padx=5, pady=5, sticky="w")
ttk.Label(root, text="V").grid(row=20, column=110, padx=5, pady=5, sticky="w")

ttk.Entry(root, textvariable=offset, width=10).grid(row=30, column=100, padx=5, pady=5)
ttk.Label(root, text="Offset").grid(row=30, column=90, padx=5, pady=5, sticky="w")
ttk.Label(root, text="V").grid(row=30, column=110, padx=5, pady=5, sticky="w")

ttk.Spinbox(root, textvariable=phase, from_=0, to=360, increment=1, width=8).grid(row=40, column=100, padx=5, pady=5)
ttk.Label(root, text="Phase").grid(row=40, column=90, padx=5, pady=5, sticky="w")
ttk.Label(root, text="deg").grid(row=40, column=110, padx=5, pady=5, sticky="w")

def connect():
    gen.connect()
    gen.write("*IDN?")
    status.set("Waiting for reply...")
    root.after(1000, show_idn)  # no sleep(): let the GUI keep running

def show_idn():
    status.set(gen.read())

def connect_scope():
    scope.connect()
    scope.write("*IDN?")
    status_scope.set("Waiting for reply...")
    root.after(1000, show_idn_scope)

def show_idn_scope():
    status_scope.set(scope.read())

def read_scope_all():
    print("Reading all values")
    status_all.set("reading all values")

    for i, fn in enumerate([read_scope, read_scope_vmax, read_scope_vamp, read_scope_duty,
                            read_scope_rtime, read_scope_ftime, read_scope_vavg, read_scope_vrms]):
        root.after(i * 200, fn)
    root.after(8 * 200, lambda: status_all.set("update all values"))


def read_scope():
    scope.measure("FREQuency")  # ask the scope for the CH1 frequency
    status_scope.set("measuring freq waiting for reply")
    root.after(20, show_scope_freq)

def read_scope_vmax():
    scope.measure("VMAX")  # ask the scope for the CH1 frequency
    status_scope.set("measuring vmax waiting for reply...")
    root.after(20, show_scope_vmax)

def read_scope_vamp():
    scope.measure("VAMP")  # ask the scope for the CH1 VAMP
    status_scope.set("measuring vamp waiting for reply...")
    root.after(20, show_scope_vamp)

def read_scope_duty():
    scope.measure("PDUTy")  # ask the scope for the CH1 frequency
    status_scope.set("measuring Duty Waiting for reply...")
    root.after(20, show_scope_pduty)

def read_scope_ftime():
    scope.measure("FTIMe")  # ask the scope for the CH1 frequency
    status_scope.set("measuring fall time Waiting for reply...")
    root.after(20, show_scope_ftime)

def read_scope_rtime():
    scope.measure("RTIMe")  # ask the scope for the CH1 frequency
    status_scope.set("measuring rise time Waiting for reply...")
    root.after(20, show_scope_rtime)

def read_scope_vavg():
    scope.measure("VAVG")  # ask the scope for the CH1 frequency
    status_scope.set("measuring vavg Waiting for reply...")
    root.after(20, show_scope_vavg)

def read_scope_vrms():
    scope.measure("VRMS")  # ask the scope for the CH1 frequency
    status_scope.set("measuring vrms Waiting for reply...")
    root.after(20, show_scope_vrms)

#here start setting the values
def show_scope_freq():
    value = float(scope.read())
    clean_value = f"{value:.2f} Hz"
    status_freq.set(clean_value)
    status_scope.set(f"Scope CH1 freq: {clean_value}")
    print("Scope frequency:", clean_value)  # also in the console

def show_scope_vmax():
    value = float(scope.read())
    clean_value = f"{value:.2f} V"
    status_vmax.set(clean_value)
    status_scope.set(f"Scope CH1 Vmax: {clean_value}")
    print("Scope Vmax:", clean_value)  # also in the console

def show_scope_pduty():
    value = float(scope.read())
    clean_value = f"{value * 100:.2f} %"  # the scope answers with a ratio (0-1)
    status_duty.set(clean_value)
    status_scope.set(f"Scope CH1 Duty: {clean_value}")
    print("Scope Duty:", clean_value)  # also in the console

def show_scope_vamp():
    value = float(scope.read())
    clean_value = f"{value:.2f} V"
    status_vamp.set(clean_value)
    status_scope.set(f"Scope CH1 Amplitude: {clean_value}")
    print("Scope Ampl:", clean_value)  # also in the console

def show_scope_ftime():
    value = float(scope.read())
    clean_value = f"{value * 1e6:.4f} us" if value < 9e37 else "N/A"  # 9.9E37 = scope could not measure
    status_ftime.set(clean_value)
    status_scope.set(f"Scope CH1 Fall time: {clean_value}")
    print("Scope ftime:", clean_value)  # also in the console

def show_scope_rtime():
    value = float(scope.read())
    clean_value = f"{value * 1e6:.4f} us" if value < 9e37 else "N/A"  # 9.9E37 = scope could not measure
    status_rtime.set(clean_value)
    status_scope.set(f"Scope CH1 Rise time: {clean_value}")
    print("Scope rtime:", clean_value)  # also in the console

def show_scope_vavg():
    value = float(scope.read())
    clean_value = f"{value:.2f} V"
    status_vavg.set(clean_value)
    status_scope.set(f"Scope CH1 Vavg: {clean_value}")
    print("Scope Vavg:", clean_value)  # also in the console

def show_scope_vrms():
    value = float(scope.read())
    clean_value = f"{value:.2f} V"
    status_vrms.set(clean_value)
    status_scope.set(f"Scope CH1 Vrms: {clean_value}")
    print("Scope Vrms:", clean_value)  # also in the console

def send():
    p = float(phase.get())
    if p > 180:  # the DG1022 accepts -180->180 
        p -= 360
    gen.apply(signal.get(), freq.get(), amplitude.get(), offset.get(), p)
    status.set("Sent")
    
    #gen.write("FREQ?")  # ask the generator what frequency it really has
    #root.after(1000, print_freq)

def print_freq():
    print("Frequency read back:", gen.read(), "Hz")  # console only


ttk.Button(root, text="Connect", command=connect).grid(row=50, column=90, padx=5, pady=5)
ttk.Button(root, text="Send", command=send).grid(row=45, column=90, padx=5, pady=5)
ttk.Label(root, textvariable=status).grid(row=50, column=100, columnspan=20, padx=5, pady=5, sticky="w")

ttk.Button(root, text="Connect scope", command=connect_scope).grid(row=60, column=90, padx=5, pady=5)
ttk.Label(root, textvariable=status_scope).grid(row=60, column=100, columnspan=20, padx=5, pady=5, sticky="w")

#buttonsfor  reading scope values
ttk.Button(root, text="Read scope ALL",   command=read_scope_all).grid(row=65, column=90, padx=5, pady=5)
ttk.Button(root, text="Read scope freq",  command=read_scope).grid(row=65, column=100, padx=5, pady=5)
ttk.Button(root, text="Read scope VMAX",  command=read_scope_vmax).grid(row=65, column=110, padx=5, pady=5)
ttk.Button(root, text="Read scope Vamp",  command=read_scope_vamp).grid(row=70, column=90, padx=5, pady=5)
ttk.Button(root, text="Read scope pDuty", command=read_scope_duty).grid(row=70, column=100, padx=5, pady=5)
ttk.Button(root, text="Read scope Fall Time", command=read_scope_ftime).grid(row=70, column=110, padx=5, pady=5)
ttk.Button(root, text="Read scope Rise Time", command=read_scope_rtime).grid(row=75, column=90, padx=5, pady=5)
ttk.Button(root, text="Read scope Vavg", command=read_scope_vavg).grid(row=75, column=100, padx=5, pady=5)
ttk.Button(root, text="Read scope Vrms", command=read_scope_vrms).grid(row=75, column=110, padx=5, pady=5)
#labels for reading scope values 
ttk.Label(root, textvariable=status_all).grid(row=66, column=90, padx=5, pady=5)
ttk.Label(root, textvariable=status_freq).grid(row=66, column=100, padx=5, pady=5)
ttk.Label(root, textvariable=status_vmax).grid(row=66, column=110, padx=5, pady=5)
ttk.Label(root, textvariable=status_vamp).grid(row=71, column=90, padx=5, pady=5)
ttk.Label(root, textvariable=status_duty).grid(row=71, column=100, padx=5, pady=5)
ttk.Label(root, textvariable=status_ftime).grid(row=71, column=110, padx=5, pady=5)
ttk.Label(root, textvariable=status_rtime).grid(row=76, column=90, padx=5, pady=5)
ttk.Label(root, textvariable=status_vavg).grid(row=76, column=100, padx=5, pady=5)
ttk.Label(root, textvariable=status_vrms).grid(row=76, column=110, padx=5, pady=5)

#Bode plot amplitude and phase, on the right of the controls
fgBode = Figure(figsize=(5,6), dpi=100)
fgBode.suptitle('Bode plot', fontsize=12)
fgBode.subplots_adjust(hspace=0.28)
spAmpl = fgBode.add_subplot(211)
spAmpl.set_title('Amplitude', fontdict={'fontsize':10})
spPhas = fgBode.add_subplot(212)
spPhas.set_title('Phase', fontdict={'fontsize':10})

frPlt = ttk.Frame(root)
frPlt.grid(row=0, column=130, rowspan=80, padx=5, pady=5)
cvPlot = FigureCanvasTkAgg(fgBode, master=frPlt)
cvPlot.draw()
cvPlot.get_tk_widget().pack(side="top", fill="both", expand=1)
tbPlot = NavigationToolbar2Tk(cvPlot, frPlt)
tbPlot.update()

root.mainloop()