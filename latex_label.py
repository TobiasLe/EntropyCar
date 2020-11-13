from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasAgg(fig)

fig.text(.5, .5, r'possibilities $\Omega$', fontsize=40, color="white")
fig.savefig("output.svg", bbox_inches="tight", facecolor=(1,1,1,0))