import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import astropy.coordinates as coord
from datetime import datetime

data_path = "horizons_results.txt"

data = np.loadtxt(data_path, skiprows=166, max_rows=3209, dtype=str, delimiter=",")

artemis_t = [datetime.fromisoformat(str(t).replace("A.D. ", "").lstrip().replace(" ", "T").replace("Apr", "04")) for t in data[:, 1]]
artemis_t_sec = [(t-artemis_t[0]).total_seconds() for t in artemis_t]

print(artemis_t[0])

print(data[:, 2:-1])

# artemis_vec = [[float(val.lstrip()) for val in vec] for vec in data[:, 2:-1]]

# print([vec[0] for vec in artemis_vec])

# print(artemis_vec[0, 3:])
# artemis_v = np.linalg.norm(artemis_vec[:, 3:], axis=1)
# print(artemis_v.shape)

# ax = plt.figure().add_subplot(projection="3d")
# ax.scatter(
#     [vec[0] for vec in artemis_vec],
#     [vec[1] for vec in artemis_vec],
#     [vec[2] for vec in artemis_vec],
#     c=artemis_t_sec
# )
# ax.plot(0, 0, 0, "g.", markersize=20)
# plt.show()
