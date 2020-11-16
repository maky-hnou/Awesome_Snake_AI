import argparse

from generate_data import GenerateData
from test_model import TestSnakeModel
from train_model import TrainSnake

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', required=True,
                    help='Run training mode or testing mode')
parser.add_argument('-w', '--width', default=600,
                    help='The width of the scene')
parser.add_argument('-l', '--height', default=400,
                    help='The height of the scene')
parser.add_argument('-b', '--block', default=10,
                    help='The size of the blocks forming the snake and the'
                    'borders')
parser.add_argument('-z', '--zone', default=60,
                    help='the height of the info zone')
parser.add_argument('-c', '--clock', default=100,
                    help='The clock rate used for pygame')
args = parser.parse_args()
mode = args.mode
width = args.width
height = args.height
block = args.block
info_zone = args.zone
clock_rate = args.clock

if mode == 'train':
    print('[INFO]: Starting the training process...\nCollecting the data...')
    data = GenerateData(height=height, width=width, block=block,
                        info_zone=info_zone, clock_rate=clock_rate)
    training_data_x, training_data_y = data.generate_training_data()
    print('[INFO]: Running the training...')
    train_snake = TrainSnake(train_x=training_data_x, train_y=training_data_y)
    train_snake.create_training_model()
    print('[INFO]: Training finished, the models are saved in models folder')
elif mode == 'test':
    print('[INFO]: Starting the testing process...\nTo exit, press Ctrl+c')
    test = TestSnakeModel(model_path='models/model.h5',
                          json_path='models/model.json',
                          width=width, height=height, block=block,
                          info_zone=info_zone, clock_rate=clock_rate)
    test.run_test()
else:
    print('Please select between train or test modes!')
