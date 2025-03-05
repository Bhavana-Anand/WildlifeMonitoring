'''import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Read the CSV file
df = pd.read_csv("C:\\Users\\Bhavana\\Desktop\\Sensors\\optics1.csv")

    
# Create time array (assuming readings were taken at 1-second intervals)
start_time = datetime.now()
#times = [start_time + timedelta(seconds=i) for i in range(len(df))]
times = [i for i in range(len(df))]  # Convert seconds to minutes
    
# Create the plot
plt.figure(figsize=(12, 6))
    
# Plot photocurrent vs time
plt.plot(times, df['Photocurrent'], 'b-', linewidth=2, label='Photocurrent')
plt.scatter(times, df['Photocurrent'], color='blue', alpha=0.5, s=30)
    
# Customize the plot
plt.title('Photocurrent vs Time', fontsize=14, pad=15)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Photocurrent (A)', fontsize=12)
    
# Format y-axis in scientific notation
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    
# Rotate x-axis labels for better readability
plt.xticks(rotation=45)
    
# Add grid
plt.grid(True, linestyle='--', alpha=0.7)
    
# Add legend
plt.legend()
    
# Adjust layout to prevent label cutoff
plt.tight_layout()
    
    # Save the plot
    #plt.savefig('photocurrent_vs_time.png', dpi=300, bbox_inches='tight')
    
# Display the plot
plt.show()'''

'''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import time
from datetime import datetime

# Set up the figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.2)

# Forest area dimensions (in grid cells)
GRID_WIDTH = 50
GRID_HEIGHT = 40

# Initialize data structures
# Temperature grid for CCD thermal sensor (forest fire detection)
temperature_grid = np.ones((GRID_HEIGHT, GRID_WIDTH)) * 25  # Base temperature 25°C

# Heat signature grid for AFIR sensor (animal tracking)
animal_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))

# Status indicators for alerts
fire_alert = False

# Animal types and their heat signatures
animal_type = {
    "Deer": {"count": 5, "heat_signature": 38, "color": "green", "size": 30}
}

# Animal positions (x, y coordinates)
animals = []
for i in range(animal_type["Deer"]["count"]):
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    animals.append({"x": x, "y": y, "direction": random.uniform(0, 2*np.pi)})

# Fire hotspots
fire_spots = []

# Create initial heatmap for CCD thermal sensor (forest fire)
ccd_heatmap = ax1.imshow(temperature_grid, cmap='inferno', vmin=20, vmax=100)
ax1.set_title('CCD Thermal Sensor - Forest Fire Detection')
fig.colorbar(ccd_heatmap, ax=ax1, label='Temperature (°C)')


# Create initial visualization for AFIR sensor (animal tracking)
afir_plot = ax2.imshow(animal_grid, cmap='viridis', vmin=0, vmax=45)
ax2.set_title('AFIR Sensor - Wildlife Tracking')
fig.colorbar(afir_plot, ax=ax2, label='Heat Signature (°C)')


# Add a text area for alerts and information
alert_text = fig.text(0.5, 0.05, '', ha='center', va='center', fontsize=12, 
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Add a timestamp
timestamp_text = fig.text(0.5, 0.12, '', ha='center', va='center', fontsize=10)

# Scatter plot for animal visualization (will be updated in animation)
scatter_animals = ax2.scatter([], [], s=animal_type["Deer"]["size"], 
                              c=animal_type["Deer"]["color"], label="Deer")

# Add legend for animal types
ax2.legend(loc='upper right')

# Simulate fire outbreak randomly
def start_fire():
    if random.random() < 0.02 and len(fire_spots) < 3:  # 2% chance to start a new fire
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        intensity = random.uniform(65, 90)  # Fire temperature
        fire_spots.append({"x": x, "y": y, "intensity": intensity, "spread": 1})
        return True
    return False

# Update animal positions with realistic movement patterns
def update_animals():
    for animal in animals:
        # Change direction occasionally
        if random.random() < 0.1:
            animal["direction"] += random.uniform(-np.pi/4, np.pi/4)
        
        # Move in the current direction
        speed = 0.3
        dx = speed * np.cos(animal["direction"])
        dy = speed * np.sin(animal["direction"])
        
        # Update position with boundary checking
        animal["x"] = max(0, min(GRID_WIDTH - 1, animal["x"] + dx))
        animal["y"] = max(0, min(GRID_HEIGHT - 1, animal["y"] + dy))
        
        # Animals avoid fire areas
        for fire in fire_spots:
            dist = np.sqrt((animal["x"] - fire["x"])**2 + (animal["y"] - fire["y"])**2)
            if dist < 10:  # If animal is close to fire
                # Move away from fire
                angle = np.arctan2(animal["y"] - fire["y"], animal["x"] - fire["x"])
                animal["direction"] = angle

# Animation update function
def update(frame):
    global fire_alert
    
    # Update timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_text.set_text(f"Timestamp: {current_time}")
    
    # Create temperature diffusion effect
    kernel = np.array([[0.1, 0.15, 0.1], 
                       [0.15, 0, 0.15], 
                       [0.1, 0.15, 0.1]])
    
    # Apply slight natural temperature variations
    temperature_grid_new = temperature_grid.copy()
    for i in range(1, GRID_HEIGHT-1):
        for j in range(1, GRID_WIDTH-1):
            temp_sum = 0
            for ki in range(3):
                for kj in range(3):
                    ni, nj = i + ki - 1, j + kj - 1
                    temp_sum += temperature_grid[ni, nj] * kernel[ki, kj]
            
            # Add some natural variation
            temperature_grid_new[i, j] += temp_sum + random.uniform(-0.1, 0.1)
    
    # Limit temperature to natural range
    temperature_grid_new = np.clip(temperature_grid_new, 20, 100)
    
    # Start new fires randomly
    new_fire = start_fire()
    
    # Update existing fires
    for fire in fire_spots:
        # Increase fire spread
        fire["spread"] = min(7, fire["spread"] + 0.1)
        
        # Apply fire temperature to surrounding area (Gaussian spread)
        x, y = int(fire["x"]), int(fire["y"])
        spread = int(fire["spread"])
        
        for i in range(max(0, y-spread), min(GRID_HEIGHT, y+spread+1)):
            for j in range(max(0, x-spread), min(GRID_WIDTH, x+spread+1)):
                dist = np.sqrt((j-x)**2 + (i-y)**2)
                if dist <= fire["spread"]:
                    # Temperature decreases with distance from center
                    temp_increase = fire["intensity"] * np.exp(-0.3 * dist)
                    temperature_grid_new[i, j] = max(temperature_grid_new[i, j], temp_increase)
    
    # Check if fire alert should be triggered (temp > 60°C)
    if np.max(temperature_grid_new) > 60:
        fire_alert = True
    
    # Update animal positions
    update_animals()
    
    # Update animal grid based on animal positions
    animal_grid_new = np.zeros((GRID_HEIGHT, GRID_WIDTH))
    
    # Update scatter plots for animals
    x_coords = []
    y_coords = []
    
    for animal in animals:
        x, y = int(animal["x"]), int(animal["y"])
        x_coords.append(x)
        y_coords.append(y)
        
        # Add heat signature to grid
        heat_sig = animal_type["Deer"]["heat_signature"]
        
        # Add animal heat signature with falloff
        spread = 2
        for i in range(max(0, y-spread), min(GRID_HEIGHT, y+spread+1)):
            for j in range(max(0, x-spread), min(GRID_WIDTH, x+spread+1)):
                dist = np.sqrt((j-x)**2 + (i-y)**2)
                if dist <= spread:
                    intensity = heat_sig * np.exp(-0.5 * dist)
                    animal_grid_new[i, j] = max(animal_grid_new[i, j], intensity)
    
    # Update scatter plot
    scatter_animals.set_offsets(np.column_stack((x_coords, y_coords)))
    
    # Set alert text
    if fire_alert:
        # Get coordinates of hottest point
        y_max, x_max = np.unravel_index(np.argmax(temperature_grid_new), temperature_grid_new.shape)
        max_temp = temperature_grid_new[y_max, x_max]
        alert_msg = f" FIRE ALERT! Detected temperature of {max_temp:.1f}°C at coordinates ({x_max}, {y_max})."
        
        # If temperature drops, reset alert
        if max_temp < 55:
            fire_alert = False
    else:
        alert_msg = "System operational - No alerts active"
    
    alert_text.set_text(alert_msg)
    
    # Update visualizations
    ccd_heatmap.set_array(temperature_grid_new)
    afir_plot.set_array(animal_grid_new)
    
    # Update current temperature grid for next iteration
    temperature_grid[:] = temperature_grid_new
    
    return [ccd_heatmap, afir_plot, alert_text, timestamp_text, scatter_animals]

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=500, blit=True)

plt.tight_layout()
plt.show()'''

'''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import time
from datetime import datetime

# Set up the figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.2)

# Forest area dimensions (in grid cells)
GRID_WIDTH = 50
GRID_HEIGHT = 40

# Initialize data structures
temperature_grid = np.ones((GRID_HEIGHT, GRID_WIDTH)) * 25  # Base temperature 25°C
animal_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))

# Status indicators for alerts
fire_alert = False

# Create initial heatmap for CCD thermal sensor (forest fire)
ccd_heatmap = ax1.imshow(temperature_grid, cmap='inferno', vmin=20, vmax=100)
ax1.set_title('CCD Thermal Sensor - Forest Fire Detection')
fig.colorbar(ccd_heatmap, ax=ax1, label='Temperature (°C)')

# Create initial visualization for AFIR sensor (animal tracking)
afir_plot = ax2.imshow(animal_grid, cmap='viridis', vmin=0, vmax=45)
ax2.set_title('AFIR Sensor - Wildlife Tracking')
fig.colorbar(afir_plot, ax=ax2, label='Heat Signature (°C)')

# Add a text area for alerts and information
alert_text = fig.text(0.5, 0.05, '', ha='center', va='center', fontsize=12, 
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Add a timestamp
timestamp_text = fig.text(0.5, 0.12, '', ha='center', va='center', fontsize=10)

# Initialize with empty data - fixed to avoid errors
scatter_animals = ax2.scatter([], [], s=30, c='green', label="Deer")

# Add legend for animal types
ax2.legend(loc='upper right')

# Function to read data from CSV files generated by the C program
def read_grid_file(filename, is_temperature=False):
    try:
        # Use the correct path for your files
        filepath = os.path.join("C:\\Users\\Bhavana\\Desktop\\Sensors\\", 
                               "temperature.csv" if is_temperature else "wildlife.csv")
        
        with open(filepath, 'r') as file:
            # Read dimensions
            dimensions = file.readline().strip().split()
            height, width = int(dimensions[0]), int(dimensions[1])
            
            # Read grid data
            grid = np.zeros((height, width))
            for i in range(height):
                line = file.readline().strip().split()
                for j in range(width):
                    grid[i, j] = float(line[j])
            return grid
    except FileNotFoundError:
        print(f"Warning: File {filepath} not found. Using simulation mode.")
        if is_temperature:
            return temperature_grid.copy()
        else:
            return animal_grid.copy()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        if is_temperature:
            return temperature_grid.copy()
        else:
            return animal_grid.copy()

# Function to extract animal positions from heat signature grid
def extract_animal_positions(grid):
    # Find local maxima in the grid as animal positions
    positions = []
    threshold = 30  # Minimum heat signature to consider as an animal
    
    for i in range(1, GRID_HEIGHT-1):
        for j in range(1, GRID_WIDTH-1):
            # Check if this is a local maximum
            if grid[i, j] > threshold:
                is_max = True
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        if i+di < 0 or i+di >= GRID_HEIGHT or j+dj < 0 or j+dj >= GRID_WIDTH:
                            continue
                        if grid[i, j] < grid[i+di, j+dj]:
                            is_max = False
                            break
                    if not is_max:
                        break
                if is_max:
                    positions.append((j, i))  # x, y format for scatter plot
    
    return positions

# Function to check for fire alert based on temperature grid
def check_fire_alert(grid):
    max_temp = np.max(grid)
    if max_temp > 60:
        y_max, x_max = np.unravel_index(np.argmax(grid), grid.shape)
        return True, max_temp, x_max, y_max
    return False, 0, 0, 0

# Animation update function
def update(frame):
    global temperature_grid, animal_grid, fire_alert
    
    # Update timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_text.set_text(f"Timestamp: {current_time}")
    
    # Try to read the grid files
    temperature_grid = read_grid_file("temperature_grid", is_temperature=True)
    animal_grid = read_grid_file("animal_grid", is_temperature=False)
    
    # Extract animal positions from the animal grid
    animal_positions = extract_animal_positions(animal_grid)
    
    # Fixed handling of empty animal positions
    if animal_positions:
        x_coords, y_coords = zip(*animal_positions)
        scatter_animals.set_offsets(np.column_stack((x_coords, y_coords)))
    else:
        # Set empty array correctly
        scatter_animals.set_offsets(np.zeros((0, 2)))
    
    # Check for fire alert
    fire_alert, max_temp, x_max, y_max = check_fire_alert(temperature_grid)
    
    # Set alert text
    if fire_alert:
        alert_msg = f" FIRE ALERT! Detected temperature of {max_temp:.1f}°C at coordinates ({x_max}, {y_max})."
    else:
        alert_msg = "System operational - No alerts active"
    
    alert_text.set_text(alert_msg)
    
    # Update visualizations
    ccd_heatmap.set_array(temperature_grid)
    afir_plot.set_array(animal_grid)
    
    return [ccd_heatmap, afir_plot, alert_text, timestamp_text, scatter_animals]

# Simulation mode with improved fire simulation
def simulate_data():
    global temperature_grid, animal_grid
    
    # 1. Reset temperature to baseline with some variation
    if np.max(temperature_grid) > 90:  # Reset if everything is on fire
        temperature_grid = np.random.normal(25, 1, (GRID_HEIGHT, GRID_WIDTH))
    
    # 2. Add some random fires (but not covering the entire area)
    if np.random.random() < 0.1:
        # Pick a random location for a fire
        x = np.random.randint(5, GRID_WIDTH-5)
        y = np.random.randint(5, GRID_HEIGHT-5)
        intensity = np.random.uniform(65, 90)
        radius = np.random.randint(2, 6)
        
        for i in range(max(0, y-radius), min(GRID_HEIGHT, y+radius+1)):
            for j in range(max(0, x-radius), min(GRID_WIDTH, x+radius+1)):
                dist = np.sqrt((j-x)**2 + (i-y)**2)
                if dist <= radius:
                    temp_increase = intensity * np.exp(-0.3 * dist)
                    temperature_grid[i, j] = min(100, max(temperature_grid[i, j], temp_increase))
    
    # 3. Apply diffusion
    kernel = np.array([[0.1, 0.15, 0.1], [0.15, 0, 0.15], [0.1, 0.15, 0.1]])
    temp_new = temperature_grid.copy()
    
    for i in range(1, GRID_HEIGHT-1):
        for j in range(1, GRID_WIDTH-1):
            temp_sum = 0
            for ki in range(3):
                for kj in range(3):
                    ni, nj = i + ki - 1, j + kj - 1
                    temp_sum += temperature_grid[ni, nj] * kernel[ki, kj]
            temp_new[i, j] = 0.9 * temp_new[i, j] + 0.1 * temp_sum + np.random.uniform(-0.2, 0.2)
    
    # Apply cooling to simulate fire dying out
    temp_new = temp_new - 0.5 * (temp_new > 50)
    temperature_grid = np.clip(temp_new, 20, 100)
    
    # 4. Simulate animal movement
    animal_grid.fill(0)
    num_animals = 5
    for _ in range(num_animals):
        x = np.random.randint(5, GRID_WIDTH-5)
        y = np.random.randint(5, GRID_HEIGHT-5)
        heat_sig = np.random.uniform(35, 40)  # Animal body temperature
        spread = 2
        
        for i in range(max(0, y-spread), min(GRID_HEIGHT, y+spread+1)):
            for j in range(max(0, x-spread), min(GRID_WIDTH, x+spread+1)):
                dist = np.sqrt((j-x)**2 + (i-y)**2)
                if dist <= spread:
                    intensity = heat_sig * np.exp(-0.5 * dist)
                    animal_grid[i, j] = max(animal_grid[i, j], intensity)

# Modified update function that falls back to simulation
def update_with_fallback(frame):
    global temperature_grid, animal_grid
    
    # Always use simulation for this example to ensure proper visualization
    simulate_data()
    
    # The rest of the update function stays the same
    return update(frame)

# Create animation with the fallback mechanism
ani = FuncAnimation(fig, update_with_fallback, frames=100, interval=500, blit=True)

plt.tight_layout()
plt.show()'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import time
from datetime import datetime

# Set up the figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.2)

# Forest area dimensions (in grid cells)
GRID_WIDTH = 50
GRID_HEIGHT = 40

# Initialize data structures
temperature_grid = np.ones((GRID_HEIGHT, GRID_WIDTH)) * 25  # Base temperature 25°C
animal_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))

# Status indicators for alerts
fire_alert = False

# Create initial heatmap for CCD thermal sensor (forest fire)
ccd_heatmap = ax1.imshow(temperature_grid, cmap='inferno', vmin=20, vmax=100)
ax1.set_title('CCD Thermal Sensor - Forest Fire Detection')
fig.colorbar(ccd_heatmap, ax=ax1, label='Temperature (°C)')

# Create initial visualization for AFIR sensor (animal tracking)
afir_plot = ax2.imshow(animal_grid, cmap='viridis', vmin=0, vmax=45)
ax2.set_title('AFIR Sensor - Wildlife Tracking')
fig.colorbar(afir_plot, ax=ax2, label='Heat Signature (°C)')

# Add a text area for alerts and information
alert_text = fig.text(0.5, 0.05, '', ha='center', va='center', fontsize=12, 
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Add a timestamp
timestamp_text = fig.text(0.5, 0.12, '', ha='center', va='center', fontsize=10)

# Initialize deer locations with larger markers and more visibility
scatter_animals = ax2.scatter([], [], s=80, c='green', marker='o', 
                             edgecolors='white', linewidths=1.5, label="Deer")

# Add legend for animal types
ax2.legend(loc='upper right')

# Store deer positions for tracking movement
deer_positions = []
for _ in range(8):  # Create 8 deer initially
    deer_positions.append([
        np.random.randint(5, GRID_WIDTH-5),  # x position
        np.random.randint(5, GRID_HEIGHT-5),  # y position
        np.random.uniform(-0.5, 0.5),        # x velocity
        np.random.uniform(-0.5, 0.5)         # y velocity
    ])

# Function to update deer positions with natural movement patterns
def update_deer_positions():
    global deer_positions
    
    for i, deer in enumerate(deer_positions):
        # Occasionally change direction
        if np.random.random() < 0.1:
            deer[2] = np.random.uniform(-0.7, 0.7)  # New x velocity
            deer[3] = np.random.uniform(-0.7, 0.7)  # New y velocity
        
        # Move deer based on velocity
        deer[0] += deer[2]
        deer[1] += deer[3]
        
        # Keep deer within boundaries
        deer[0] = np.clip(deer[0], 2, GRID_WIDTH-3)
        deer[1] = np.clip(deer[1], 2, GRID_HEIGHT-3)
        
        # Update the deer position
        deer_positions[i] = deer

# Function to generate heat signature grid from deer positions
def generate_animal_grid():
    global animal_grid, deer_positions
    
    # Reset the grid
    animal_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
    
    # Add heat signatures for each deer
    for deer in deer_positions:
        x, y = int(deer[0]), int(deer[1])
        heat_sig = np.random.uniform(37, 42)  # Deer body temperature
        spread = 3  # Larger heat signature spread
        
        for i in range(max(0, y-spread), min(GRID_HEIGHT, y+spread+1)):
            for j in range(max(0, x-spread), min(GRID_WIDTH, x+spread+1)):
                dist = np.sqrt((j-x)**2 + (i-y)**2)
                if dist <= spread:
                    intensity = heat_sig * np.exp(-0.3 * dist)  # Less falloff for more visibility
                    animal_grid[i, j] = max(animal_grid[i, j], intensity)
    
    return animal_grid

# Function to extract animal positions from heat signature grid
def extract_animal_positions():
    global deer_positions
    positions = []
    
    # Use the actual deer positions for better visualization
    for deer in deer_positions:
        positions.append((deer[0], deer[1]))
    
    return positions

# Function to check for fire alert based on temperature grid
def check_fire_alert(grid):
    max_temp = np.max(grid)
    if max_temp > 60:
        y_max, x_max = np.unravel_index(np.argmax(grid), grid.shape)
        return True, max_temp, x_max, y_max
    return False, 0, 0, 0

# Simulate forest fires
def simulate_fires():
    global temperature_grid
    
    # 1. Reset temperature to baseline with some variation
    if np.random.random() < 0.01:  # Occasionally reset
        temperature_grid = np.random.normal(25, 1, (GRID_HEIGHT, GRID_WIDTH))
    
    # 2. Add some random fires (but not covering the entire area)
    if np.random.random() < 0.05:
        # Pick a random location for a fire
        x = np.random.randint(5, GRID_WIDTH-5)
        y = np.random.randint(5, GRID_HEIGHT-5)
        intensity = np.random.uniform(65, 90)
        radius = np.random.randint(3, 7)
        
        for i in range(max(0, y-radius), min(GRID_HEIGHT, y+radius+1)):
            for j in range(max(0, x-radius), min(GRID_WIDTH, x+radius+1)):
                dist = np.sqrt((j-x)**2 + (i-y)**2)
                if dist <= radius:
                    temp_increase = intensity * np.exp(-0.2 * dist)
                    temperature_grid[i, j] = min(100, max(temperature_grid[i, j], temp_increase))
    
    # 3. Apply diffusion
    kernel = np.array([[0.1, 0.15, 0.1], [0.15, 0, 0.15], [0.1, 0.15, 0.1]])
    temp_new = temperature_grid.copy()
    
    for i in range(1, GRID_HEIGHT-1):
        for j in range(1, GRID_WIDTH-1):
            temp_sum = 0
            for ki in range(3):
                for kj in range(3):
                    ni, nj = i + ki - 1, j + kj - 1
                    temp_sum += temperature_grid[ni, nj] * kernel[ki, kj]
            temp_new[i, j] = 0.95 * temp_new[i, j] + 0.05 * temp_sum + np.random.uniform(-0.1, 0.1)
    
    # Apply cooling to simulate fire dying out
    temp_new = temp_new - 0.2 * (temp_new > 50)
    temperature_grid = np.clip(temp_new, 20, 100)

# Animation update function
def update(frame):
    global temperature_grid, animal_grid, fire_alert
    
    # Update timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_text.set_text(f"Timestamp: {current_time}")
    
    # Update deer positions and generate heat signatures
    update_deer_positions()
    animal_grid = generate_animal_grid()
    
    # Simulate forest fires
    simulate_fires()
    
    # Extract animal positions for scatter plot
    animal_positions = extract_animal_positions()
    
    # Update scatter plot with deer positions
    if animal_positions:
        x_coords, y_coords = zip(*animal_positions)
        scatter_animals.set_offsets(np.column_stack((x_coords, y_coords)))
    else:
        scatter_animals.set_offsets(np.zeros((0, 2)))
    
    # Check for fire alert
    fire_alert, max_temp, x_max, y_max = check_fire_alert(temperature_grid)
    
    # Set alert text
    if fire_alert:
        alert_msg = f"🔥 FIRE ALERT! Detected temperature of {max_temp:.1f}°C at coordinates ({x_max}, {y_max})."
    else:
        alert_msg = "System operational - No alerts active"
    
    alert_text.set_text(alert_msg)
    
    # Update visualizations
    ccd_heatmap.set_array(temperature_grid)
    afir_plot.set_array(animal_grid)
    
    # Add animal count to the title
    ax2.set_title(f'AFIR Sensor - Wildlife Tracking ({len(deer_positions)} deer)')
    
    return [ccd_heatmap, afir_plot, alert_text, timestamp_text, scatter_animals]

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=500, blit=True)

plt.tight_layout()
plt.show()