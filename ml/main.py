"""Set parameters and run training and data generation."""
from generate_data import GenerateData
from train import TrainSnake

if __name__ == '__main__':
    # Set parameters
    # TODO: Set the needed parameters
    height = 400
    width = 600
    block = 10
    info_zone = 60
    clock_rate = 500000
    # Run data generation and get traing data
    gd = GenerateData(height=height, width=width,
                      block=block, info_zone=info_zone, clock_rate=clock_rate)
    training_data_x, training_data_y = gd.generate_training_data()
    train_snake = TrainSnake(train_x=training_data_x, train_y=training_data_y)
    train_snake.create_training_model()
