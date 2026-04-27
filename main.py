import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from algorithms.reno import Reno
from algorithms.cubic import Cubic
from algorithms.vegas import Vegas
from architecture.architecture import Network

algo_map = {"Reno": Reno, "Cubic": Cubic, "Vegas": Vegas}
algo = Reno()
net = Network(capacity=50, loss_rate=5)
cwnd_history = []
loss_rounds = []
running = False
after_id = None

root = tk.Tk()
root.title("TCP Congestion Control Simulator")
root.geometry("1060x680")

body = tk.Frame(root)
body.pack(fill="both", expand=True, padx=16, pady=12)

left = tk.Frame(body, width=230)
left.pack(side="left", fill="y", padx=(0, 12))
left.pack_propagate(False)

right = tk.Frame(body)
right.pack(side="left", fill="both", expand=True)


tk.Label(left, text="PARAMETERS", font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(20, 8), padx=4)
capacity_var = tk.IntVar(value=50)
loss_var = tk.IntVar(value=5)

tk.Label(left, text="Network Size").pack(anchor="w", padx=4)
tk.Scale(left, from_=10, to=150, orient="horizontal", variable=capacity_var).pack(fill="x", padx=4)

tk.Label(left, text="Packet Loss Rate").pack(anchor="w", padx=4, pady=(8, 0))
tk.Scale(left, from_=0, to=50, orient="horizontal", variable=loss_var).pack(fill="x", padx=4)



tk.Label(left, text="ALGORITHM", font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(20, 8), padx=4)
algo_var = tk.StringVar(value="Reno")
status_var = tk.StringVar(value="Round: 0   cwnd: 1")

for name in ("Reno", "Cubic", "Vegas"): tk.Radiobutton(left, text=name, variable=algo_var, value=name).pack(anchor="w", padx=4)
tk.Label(left, textvariable=status_var, wraplength=210, justify="left").pack(anchor="w", padx=4, pady=(16, 0))




tk.Label(left, text="CONTROLS", font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(20, 8), padx=4)
btn_frame = tk.Frame(left)
btn_frame.pack(fill="x", padx=4)

fig, ax = plt.subplots(figsize=(7, 4.5))
fig.tight_layout(pad=2)
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

def rebuild():
    global algo, net, cwnd_history, loss_rounds
    algo = algo_map[algo_var.get()]()
    net = Network(capacity=capacity_var.get(), loss_rate=loss_var.get())
    cwnd_history = []
    loss_rounds = []

def redraw():
    ax.cla()
    ax.set_title(f"Congestion Window Over Time")
    ax.set_xlabel("Round Trip Time")
    ax.set_ylabel("cwnd")
    ax.grid(True, alpha=0.4)
    
    
    if cwnd_history:
        xs = list(range(1, len(cwnd_history) + 1))
        ax.plot(xs, cwnd_history, color="blue", linewidth=1.8, label="cwnd")
        ax.axhline(y=net.capacity, color="green", linewidth=1, linestyle="--", label=f"capacity ({net.capacity})")
        
        if loss_rounds:
            lx = [r for r in loss_rounds if r <= len(cwnd_history)]
            ly = [cwnd_history[r - 1] for r in lx]
            ax.scatter(lx, ly, color="red", s=35, zorder=5, label="loss")
    ax.legend(loc="upper left", fontsize=8)
    canvas.draw()

def tick():
    global running, after_id
    if not running:
        return
    loss = net.should_lose(algo.cwnd)
    rtt = net.get_rtt(algo.cwnd)
    
    
    if isinstance(algo, Vegas):
        new_cwnd = algo.step(packet_loss=loss, rtt=rtt)
    else:
        new_cwnd = algo.step(packet_loss=loss)
        
        
    new_cwnd = min(new_cwnd, net.capacity * 2)
    round_num = len(cwnd_history) + 1
    cwnd_history.append(new_cwnd)
    
    
    if loss:
        loss_rounds.append(round_num)
    status_var.set(f"Round: {round_num}   cwnd: {new_cwnd}")
    redraw()
    after_id = root.after(200, tick)

def on_start():
    global running
    if running:
        return
    if not cwnd_history:
        rebuild()
    running = True
    tick()

def on_pause():
    global running, after_id
    running = False
    if after_id:
        root.after_cancel(after_id)

tk.Button(btn_frame, text="Start", width=7, command=on_start).pack(side="left", padx=(0, 4))
tk.Button(btn_frame, text="Pause", width=7, command=on_pause).pack(side="left", padx=(0, 4))

root.mainloop()