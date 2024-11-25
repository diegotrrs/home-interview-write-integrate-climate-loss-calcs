import json
import numpy as np

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Diego: The script could receive the number of years as an argument, but for now it's defaulted to 5
# Diego: I went for numpy arrays because it would be more efficient than python's lists as the dataset grows. 
# Although, at this point it can be an overkill for this small dataset.
def calculate_projected_losses(building_data, number_of_years = 5):
    discount_rate = 0.05
    discounting_factor = 1 + discount_rate

    floor_area = np.array([building['floor_area'] for building in building_data])
    construction_cost = np.array([building['construction_cost'] for building in building_data])
    hazard_probability = np.array([building['hazard_probability'] for building in building_data])
    inflation_rate = np.array([building['inflation_rate'] for building in building_data])

    future_cost = construction_cost * np.exp(inflation_rate * floor_area / 1000)
    # Diego: parentesis left for clarity.
    loss_estimates = (future_cost * hazard_probability) / (discounting_factor ** number_of_years)

    total_loss = np.sum(loss_estimates)
    return loss_estimates, total_loss

def main():
    data = load_data('data.json')
    total_projected_loss = calculate_projected_losses(data)
    print(f"Total Projected Loss: ${total_projected_loss}")

if __name__ == '__main__':
    main()