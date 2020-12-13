from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

# fig = Figure(figsize=(5, 4), dpi=100)
# canvas = FigureCanvasAgg(fig)
#
# fig.text(.5, .5, r'possibilities $\Omega$', fontsize=40, color="white")
# fig.savefig("possibilities_omega.svg", bbox_inches="tight", facecolor=(1,1,1,0))
#
# fig = Figure(figsize=(5, 4), dpi=100)
# canvas = FigureCanvasAgg(fig)
#
# fig.text(.5, .5, r'$\mathrm{ln}(\Omega)$', fontsize=40, color="white")
# fig.savefig("ln(omega).svg", bbox_inches="tight", facecolor=(1,1,1,0))

fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasAgg(fig)

fig.text(.5, .5, r'$\cdot10^6$', fontsize=40, color="white")
fig.savefig("mal10_6.svg", bbox_inches="tight", facecolor=(1,1,1,0))