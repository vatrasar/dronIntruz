import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

fig:Figure=None
fig,axes=plt.subplots()

plt.ion()
for i in range(50):
    # fig, axs = plt.subplots()
    # axs.set_box_aspect(1)
    #
    # axs=fig.get_axes()[0]
    plt.title("czas: %.2f s" % (i))
    y = np.random.random([10,1])
    plt.scatter(y, y, marker="s", color='r', s=4, )
    #plt.plot(y)
    plt.draw()
    plt.pause(0.0001)
    plt.clf()