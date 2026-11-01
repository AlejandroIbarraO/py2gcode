import numpy as np
import matplotlib.pyplot as plt

# little helper functions to create hilbert curves in 2D


def hilbert_curve(order):
    hilbert_seq = "a"
    for _ in range(order):
        new_seq = ""
        for char in hilbert_seq:
            if char == "a":
                new_seq += "-bF+aFa+Fb-"
            elif char == "b":
                new_seq += "+aF-bFb-Fa+"
            else:
                new_seq += char
        hilbert_seq = new_seq   
    return hilbert_seq
def translate(secuence_string,output ="vectors"):
    array = [np.array([0, 0])]
    vector = np.array([0, 1])
    for char in secuence_string:
        if char == "F":
            array.append(vector)
        elif char == "+":
            vector = np.dot(np.array([[0, -1], [1, 0]]),vector)
        elif char == "-":
            vector = np.dot(np.array([[0, 1], [-1, 0]]),vector)
    if output == "vectors":
        return np.array(array)
    else:
        return np.array(array).cumsum(axis=0)

def plot_hilbert_curve(order):
    secuence = hilbert_curve(order)
    print(secuence)
    points = translate(secuence,output="points")
    plt.figure(figsize=(6, 6))
    plt.plot(points[:, 0], points[:, 1], marker='o')
    plt.title(f'Hilbert Curve of Order {order}')
    plt.axis('equal')
    plt.grid(True)
    plt.show()
    
if __name__ == "__main__":
    plot_hilbert_curve(3)