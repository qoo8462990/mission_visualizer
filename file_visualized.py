import sys
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button

def format_csv_lines(input_file_path, output_file_path):
    path = output_file_path+".csv"
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    formatted_lines = []
    for line in lines:
        # Check if the line is empty or contains only commas and starts with '#'
        if line.strip() == "" or all(char == ',' for char in line.strip()) or line.strip().startswith('#'):
            continue  # Skip this line
        formatted_lines.append(','.join(line.replace(' ', '').split(',')))

    output_text = ''.join(formatted_lines)

    with open(path, 'w') as output_file:
        output_file.write(output_text)

    print("Mission Arrangement to", path)


def convert_to_mission(mission_name):
    path = mission_name+".csv"
    # Read the CSV file
    with open(path, 'r') as csv_file:
        csv_data = csv_file.read()

    # Define the JSON structure
    json_data = {
        "pkg_type": "0",
        "pkg_id": "vioUploadMission",
        "timestamp": 0,
        "file_name": mission_name,
        "csv": csv_data,
        "ack": 0
    }

    # Convert the JSON data to a JSON string
    json_string = json.dumps(json_data)
    path = mission_name+".json"
    with open(path, 'w') as output_file:
        output_file.write(json_string)

    # Print or save the JSON string as needed
    print('-------------------------------------------------------------------------------------')
    print('Your mission upload command with filename: ', mission_name)
    print('-------------------------------------------------------------------------------------')
    print(json_string)
    print('-------------------------------------------------------------------------------------')


def plot_xyz_coordinates(csv_file_path, num_points):
    df = pd.read_csv(csv_file_path, header=None)
    x_values = df.iloc[:, 0]
    y_values = df.iloc[:, 1]
    z_values = df.iloc[:, 2]
    angles = df.iloc[:, 3]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create slider axes
    slider_ax = plt.axes([0.25, 0.02, 0.65, 0.03])
    slider = Slider(slider_ax, 'Num Points', 1, len(x_values), valinit=num_points)
    def on_mousewheel(event):
        if event.inaxes is None:
            return
        if event.key == 'up':
            slider.set_val(slider.val + 1)
        elif event.key == 'down':
            slider.set_val(slider.val - 1)

    # Connect mousewheel event to the figure
    fig.canvas.mpl_connect('scroll_event', on_mousewheel)
    def update(val):
        num_points = int(slider.val)
        ax.clear()

        # Scatter plot with different marker size for the first point
        ax.scatter(x_values[1:num_points], y_values[1:num_points], z_values[1:num_points], marker='o', c='blue', label='Other Points')
        ax.scatter(x_values[0], y_values[0], z_values[0], s=50, marker='o', c='green', label='First Point')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        for i, (x, y, z, angle) in enumerate(zip(x_values[:num_points], y_values[:num_points], z_values[:num_points], angles[:num_points]), start=0):
            # Calculate direction vector for arrow
            arrow_length = 0.2
            arrow_x = x + arrow_length * np.cos(np.radians(angle))
            arrow_y = y + arrow_length * np.sin(np.radians(angle))
            arrow_z = z

            # Plot arrow for points other than the first one
            ax.quiver(x, y, z, arrow_x - x, arrow_y - y, arrow_z - z, color='blue', arrow_length_ratio=0.5)

            # Add number text on the end of the arrow
            ax.text(arrow_x, arrow_y, arrow_z, str(i + 1), color='red')

        plt.legend()

        fig.canvas.draw_idle()

    slider.on_changed(update)

    # Create buttons for incrementing and decrementing points
    ax_increment = plt.axes([0.15, 0.92, 0.1, 0.06])
    ax_decrement = plt.axes([0.25, 0.92, 0.1, 0.06])
    button_increment = Button(ax_increment, '+')
    button_decrement = Button(ax_decrement, '-')

    def increment(event):
        slider.set_val(slider.val + 1)

    def decrement(event):
        slider.set_val(slider.val - 1)

    button_increment.on_clicked(increment)
    button_decrement.on_clicked(decrement)

    update(num_points)  # Initial plot

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input_file output_file num_points")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        format_csv_lines(input_file_path, output_file_path)
        convert_to_mission(output_file_path)

        csv_file_path = sys.argv[2]+".csv"
        num_points = int(sys.argv[3])
        plot_xyz_coordinates(csv_file_path, num_points)


