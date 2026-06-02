import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import astropy.coordinates as coord
from astropy.time import Time
from datetime import datetime

data_path = "horizons_results.txt"

# 1. Load data
# Loads all data columns in CSV fomat
data = np.loadtxt(data_path, skiprows=166, max_rows=3209, dtype=str, delimiter=",")

# 2. To start with, let's plot the trajectory based on the position of Artemis ii
# Get list of times, reformat from Calendar Date format to isoformat seen in tutorial
artemis_t = [
    datetime.fromisoformat(
        str(t) # Convert float to string
        .replace("A.D. ", "") # Remove "A.D. "
        .lstrip() # Remove whitespace at start
        .replace(" ", "T") # Replace whitespace between date and time with "T"
        .replace("Apr", "04") # Replace "Apr" with month number
        ) for t in data[:, 1]] # For each Calendar Date in the table

# Print first datetime data point as sanity check
print(f"Start datetime: {artemis_t[0]}")

# Get list of vectors, positions in 'REF_FRAME=EME2000' and velocities in kms per second
artemis_vec = [[
    float(val.lstrip()) for val in vec # Remove starting whitespace for each column
] for vec in data[:, 2:-1]] # Ignoring time columns and final column (only whitespace)

# Create trajectory plot (position only) object
ax_pos = plt.figure().add_subplot(projection="3d")

# Set axes of scatter plot
ax_pos.scatter(
    [vec[0] for vec in artemis_vec],
    [vec[1] for vec in artemis_vec],
    [vec[2] for vec in artemis_vec],
)

# Add Earth to origin
ax_pos.plot(0, 0, 0, "g.", markersize=20)

# Show plot
plt.show()

# 3. Now let's add time to the plot
# Get List of times in seconds relative to start of recording (4 minutes between most points)
artemis_t_sec = [(t-artemis_t[0]).total_seconds() for t in artemis_t]

# Create trajectory plot (position and time) object
ax_pos_t = plt.figure().add_subplot(projection="3d")

# Set axes of scatter plot
ax_pos_t.scatter(
    [vec[0] for vec in artemis_vec],
    [vec[1] for vec in artemis_vec],
    [vec[2] for vec in artemis_vec],
    c=artemis_t_sec
)

# Add Earth to origin
ax_pos_t.plot(0, 0, 0, "g.", markersize=20)

# Show plot
plt.show()

# 4. Let's replace time with velocity
# Convert vector to array so it can be sliced correctly,
# was previously a nested list (whoops!)
artemis_vec_array = np.array(artemis_vec)

# Get a list of the resultant velocity vectors in 'REF_FRAME=EME2000'
artemis_v = np.linalg.norm(artemis_vec_array[:, 3:], axis=1)

# artemis_d = np.linalg.norm(artemis_vec_array[:, 3:], axis=1)

# Create trajectory plot (position and time) object
ax_pos_v = plt.figure().add_subplot(projection="3d")

# Set axes of scatter plot
im = ax_pos_v.scatter(
    artemis_vec_array[:, 0],
    artemis_vec_array[:, 1],
    artemis_vec_array[:, 2],
    c=artemis_v
)

# Create plot labels
plt.colorbar(im, ax=ax_pos_v, label='speed [km/s]')
ax_pos_v.set_xlabel('x [km]')
ax_pos_v.set_ylabel('y [km]')
ax_pos_v.set_zlabel('z [km]')

# Add Earth to origin
ax_pos_v.plot(0, 0, 0, "g.", markersize=20, label='Earth')

# Show plot
plt.legend()
plt.show()

# 5. Let's add the moon to our plot
# Get coords for moon at same time as Artemis ii
# GCRS is basically the same as EME2000
moon_coord = coord.get_body('moon', time=Time(artemis_t))

# Convert moon to cartesian coords
moon_coord = moon_coord.represent_as('cartesian')

# Create trajectory plot (position and time) object with Moon
ax_pos_v_plus_moon = plt.figure().add_subplot(projection="3d")

# Add moon
ax_pos_v_plus_moon.plot(
    moon_coord.x.to_value(u.km),
    moon_coord.y.to_value(u.km),
    moon_coord.z.to_value(u.km),
    'k.',
    label='Moon'
)

# Set axes of scatter plot
im = ax_pos_v_plus_moon.scatter(
    artemis_vec_array[:, 0],
    artemis_vec_array[:, 1],
    artemis_vec_array[:, 2],
    c=artemis_v
)

# Create plot labels
plt.colorbar(im, ax=ax_pos_v_plus_moon, label='speed [km/s]')
ax_pos_v_plus_moon.set_xlabel('x [km]')
ax_pos_v_plus_moon.set_ylabel('y [km]')
ax_pos_v_plus_moon.set_zlabel('z [km]')

# Add Earth to origin
ax_pos_v_plus_moon.plot(0, 0, 0, "g.", markersize=20, label='Earth')

# Show plot
plt.legend()
plt.show()