"""Set parameters and run training and data generation."""
from generate_data import GenerateData

if __name__ == '__main__':
    # Set parameters
    # TODO: Set the needed parameters
    height = 400
    width = 600
    block = 10
    info_zone = 60
    clock_rate = 500
    # Run data generation and get traing data
    gd = GenerateData(height=height, width=width,
                      block=block, info_zone=info_zone, clock_rate=clock_rate)
    training_data_x, training_data_y = gd.generate_training_data()
    print(training_data_x)
    print(training_data_x)
