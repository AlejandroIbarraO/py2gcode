import math
import matplotlib.pyplot as plt

def generate_consecutive_hatch_lines(L, d, theta_degrees):
    theta = math.radians(theta_degrees)
    A = -math.sin(theta)
    B = math.cos(theta)
    
    corners = [(0, 0), (L, 0), (L, L), (0, L)]
    rhos = [A * x + B * y for x, y in corners]
    
    rho_min, rho_max = min(rhos), max(rhos)
    k_min = math.floor(rho_min / d)
    k_max = math.ceil(rho_max / d)
    
    lines = []
    eps = 1e-9 
    
    for k in range(k_min, k_max + 1):
        C = -k * d
        pts = []
        
        # Check horizontal edges
        if abs(A) > eps:
            x_bottom = -C / A
            if -eps <= x_bottom <= L + eps: pts.append((x_bottom, 0.0))
            x_top = -(C + B * L) / A
            if -eps <= x_top <= L + eps: pts.append((x_top, L))
                
        # Check vertical edges
        if abs(B) > eps:
            y_left = -C / B
            if -eps <= y_left <= L + eps: pts.append((0.0, y_left))
            y_right = -(C + A * L) / B
            if -eps <= y_right <= L + eps: pts.append((L, y_right))
                
        # Deduplicate
        unique_pts = []
        for p in pts:
            if not any(math.hypot(p[0] - up[0], p[1] - up[1]) < eps for up in unique_pts):
                unique_pts.append(p)
                
        if len(unique_pts) == 2:
            # 1. Uniformly sort points left-to-right (and bottom-to-top if vertical)
            unique_pts.sort(key=lambda pt: (pt[0], pt[1]))
            lines.append(unique_pts)
            
    # 2. Zig-Zag Optimization: Reverse every alternate line to make the path continuous
    for i in range(len(lines)):
        if i % 2 != 0:
            lines[i].reverse()
            
    return lines


# --- Example Usage & Visualization ---
if __name__ == "__main__":
    L = 10.0       # Side length of the rectangle
    d = 1.25       # Distance between lines
    theta = 0     # Angle in degrees

    segments = generate_consecutive_hatch_lines(L, d, theta)

    # Plot the results using Matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-1, L + 1)
    ax.set_ylim(-1, L + 1)

    # Draw the bounding box
    rect = plt.Rectangle((0, 0), L, L, fill=False, color='red', linewidth=2, zorder=3)
    ax.add_patch(rect)

    # Draw the generated lines
    for pt1, pt2 in segments:
        ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color='blue', linewidth=1.5)

    plt.title(f"Hatch Pattern: L={L}, d={d}, Angle={theta}°")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()