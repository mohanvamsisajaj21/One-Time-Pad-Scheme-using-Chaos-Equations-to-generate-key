import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Pendulum rod lengths (L1, L2 in meters), bob masses (in kg), rod suspension angles(degrees), Key Length(KeyLength).
L1, L2 = 1.2, 1
m1, m2 = 8, 3
ang1, ang2 = 120, 220
KeyLength = 256
# The above values are parameters shared between Alice and Bob.


def derivative(y, t, L1, L2, m1, m2):
    alpha, z1, beta, z2 = y
    c, s = np.cos(alpha-beta), np.sin(alpha-beta)
    dalpha = z1
    dz1 = (m2*9.81*np.sin(beta)*c - m2*s*(L1*z1**2*c + L2*z2**2) - (m1+m2)*9.81*np.sin(alpha)) / L1 / (m1 + m2*s**2)
    dbeta = z2
    dz2 = ((m1+m2)*(L1*z1**2*s - 9.81*np.sin(beta) + 9.81*np.sin(alpha)*c) + m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return dalpha, dz1, dbeta, dz2

# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = KeyLength*0.1, 0.01
t = np.arange(0, tmax+dt, dt)
# Initial conditions: alpha, dalpha/dt, beta, dbeta/dt.
y0 = np.array([ang1*np.pi/180, 0, ang2*np.pi/180, 0])
# Do the numerical integration of the equations of motion
y = odeint(derivative, y0, t, args=(L1, L2, m1, m2))
# Unpack z and theta as a function of time
alpha, beta = y[:,0], y[:,2]
# Convert to Cartesian coordinates of the two bob positions.
x1, y1 = L1 * np.sin(alpha), -L1 * np.cos(alpha)
x2, y2 = x1 + L2 * np.sin(beta), y1 - L2 * np.cos(beta)
# Plot a trail of the m2 bob's position for the last trail_secs seconds.
trail_secs = 10
# This corresponds to max_trail time points.
max_trail = int(trail_secs / dt)

def make_plot(i):
    ax.plot([0, x1[i], x2[i]], [0, y1[i], y2[i]], lw=2, c='k')
    c0 = Circle((0, 0), 0.05/2, fc='k', zorder=10)
    c1 = Circle((x1[i], y1[i]), 0.05, fc='b', ec='b', zorder=10)
    c2 = Circle((x2[i], y2[i]), 0.05, fc='r', ec='r', zorder=10)
    ax.add_patch(c0)
    ax.add_patch(c1)
    ax.add_patch(c2)
    ns = 60
    s = max_trail // ns

    for j in range(ns):
        imin = i - (ns-j)*s
        if imin < 0:
            continue
        imax = imin + s + 1
        ax.plot(x2[imin:imax], y2[imin:imax])

    ax.set_xlim(-L1-L2-0.05, L1+L2+0.05)
    ax.set_ylim(-L1-L2-0.05, L1+L2+0.05)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig('frames'+str(i)+'.png'.format(i//di), dpi=96)
    plt.cla()

fig = plt.figure(figsize=(5, 5), dpi=96)
ax = fig.add_subplot(111)
fps = 10
di = int(1/fps/dt)

alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
Key = ''

for i in range(0, t.size, di):
    print('coordinates: ', x2[i], y2[i])
    # X and Y co-ordinates of the bob2 are added and digits from index 8 to 11 are choosen.
    key = alphabets[int(str(x2[i] + y2[i])[8:11])%26]
    Key += key
    print(i // di, 'character of the Key: ', key)
    make_plot(i)

# Final generated key.
print('\nGenerated Key: ', Key)