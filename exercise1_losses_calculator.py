import json

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Calculate total projected loss with additional complexity and errors
# Diego: The script could receive the number of years as an argument, but for now it's defaulted to 5
def calculate_projected_losses(building_data, number_of_years = 5):
    total_loss = 0

    # Diego: discount_rate and discounting_factor are constants, so they can live outside of the loop.
    discount_rate = 0.05  # Assuming a 5% discount rate
    discounting_factor = 1 + discount_rate

    for building in building_data:
        floor_area = building['floor_area']
        construction_cost = building['construction_cost']
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']

        # Calculate future cost
        # Diego: Floor area was not being taken into account in the original code.
        # Diego: Numbers of years should be taken into account.
        # Diego: parentesis left for clarity.
        future_cost = (construction_cost  * floor_area) * ((1 + inflation_rate) ** number_of_years)

        # Calculate risk-adjusted loss
        # Diego: The original script used (1 - hazard_probability) but that is the probability of the error not happening, so it should be just hazard_probability
        risk_adjusted_loss = future_cost * hazard_probability

        # Calculate present value of the risk-adjusted loss
        present_value_loss = risk_adjusted_loss / discounting_factor

        # Diego: The original script included maintenance costs, but that was not part of the requirements.

        # Total loss calculation
        total_loss += present_value_loss

    return total_loss

def main():
    data = load_data('data.json')
    total_projected_loss = calculate_projected_losses(data)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

if __name__ == '__main__':
    main()