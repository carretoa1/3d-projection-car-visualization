import math
import numpy as np
import matplotlib.pyplot as plt

D = np.array([
    [-6.5, -6.5, -6.5, -6.5, -2.5, -2.5, -0.75, -0.75,
      3.25, 3.25, 4.5, 4.5, 6.5, 6.5, 6.5, 6.5],
    [-2.0, -2.0, 0.5, 0.5, 0.5, 0.5, 2.0, 2.0,
      2.0, 2.0, 0.5, 0.5, 0.5, 0.5, -2.0, -2.0],
    [-2.5, 2.5, 2.5, -2.5, -2.5, 2.5, -2.5, 2.5,
     -2.5, 2.5, -2.5, 2.5, -2.5, 2.5, 2.5, -2.5],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
], dtype=float)

C = np.array([
    [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0]
], dtype=int)


def perspective_matrix(b, c, d):
    return np.array([
        [d, 0, -b, 0],
        [0, d, -c, 0],
        [0, 0,  0, 0],
        [0, 0, -1, d]
    ], dtype=float)


def project_points(D_in, b, c, d):
    P = perspective_matrix(b, c, d)
    H = P @ D_in
    x_p = H[0, :]
    y_p = H[1, :]
    w = H[3, :]
    xs = x_p / w
    ys = y_p / w
    return xs, ys


def rotation_y(theta_deg):
    theta = math.radians(theta_deg)
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([
        [ c, 0,  s, 0],
        [ 0, 1,  0, 0],
        [-s, 0,  c, 0],
        [ 0, 0,  0, 1]
    ], dtype=float)


def rotation_z(theta_deg):
    theta = math.radians(theta_deg)
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([
        [ c, -s, 0, 0],
        [ s,  c, 0, 0],
        [ 0,  0, 1, 0],
        [ 0,  0, 0, 1]
    ], dtype=float)


def zoom_matrix(factor):
    return np.array([
        [factor, 0,      0,      0],
        [0,      factor, 0,      0],
        [0,      0,      factor, 0],
        [0,      0,      0,      1]
    ], dtype=float)


def plot_car(xs, ys, C, ax, title):
    n = len(xs)
    for i in range(n):
        for j in range(i + 1, n):
            if C[i, j] == 1:
                ax.plot([xs[i], xs[j]], [ys[i], ys[j]])
    ax.set_aspect('equal', 'box')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)


def main():
    b1, c1, d1 = -5, 10, 10
    P1 = perspective_matrix(b1, c1, d1)
    print("Q1) Projection matrix P1 =")
    print(P1)
    xs1, ys1 = project_points(D, b1, c1, d1)
    fig1, ax1 = plt.subplots()
    plot_car(xs1, ys1, C, ax1, "Q1: Projection (b,c,d)=(-5,10,10)")
    plt.tight_layout()

    b2, c2, d2 = 0, 10, 25
    P2 = perspective_matrix(b2, c2, d2)
    print("\nQ2) Projection matrix P2 =")
    print(P2)
    xs2, ys2 = project_points(D, b2, c2, d2)
    fig2, ax2 = plt.subplots()
    plot_car(xs2, ys2, C, ax2, "Q2: Projection (b,c,d)=(0,10,25)")
    plt.tight_layout()

    Ry30 = rotation_y(30)
    print("\nQ3) Rotation matrix R_y(30°) =")
    print(Ry30)
    D_rot_y = Ry30 @ D
    xs3, ys3 = project_points(D_rot_y, b2, c2, d2)
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(10, 4))
    plot_car(xs2, ys2, C, ax3a, "Q2: Original (no rotation)")
    plot_car(xs3, ys3, C, ax3b, "Q3: Rotated 30° about y")
    plt.tight_layout()

    Rz45 = rotation_z(45)
    print("\nQ4) Rotation matrix R_z(45°) =")
    print(Rz45)
    D_rot_z = Rz45 @ D
    xs4, ys4 = project_points(D_rot_z, b2, c2, d2)
    fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(10, 4))
    plot_car(xs2, ys2, C, ax4a, "Q2: Original (no rotation)")
    plot_car(xs4, ys4, C, ax4b, "Q4: Rotated 45° about z")
    plt.tight_layout()

    Z = zoom_matrix(1.5)
    print("\nQ5) Zoom matrix (150%) =")
    print(Z)
    D_zoom = Z @ D
    xs5, ys5 = project_points(D_zoom, b2, c2, d2)
    fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(10, 4))
    plot_car(xs2, ys2, C, ax5a, "Q2: Original (no zoom)")
    plot_car(xs5, ys5, C, ax5b, "Q5: 150% zoom")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
