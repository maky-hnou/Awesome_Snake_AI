# Awesome_Snake_AI

![Python version][python-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

## About this repo:  
An implementation of various algorithms and techniques (graph theory, Machine Learning...) all
combined together to create an AI that outperforms human skills in playing the Snake game.

## Content of the repo:  
The project has been organized as follows:  
- `requirements.txt`: a text file containing the needed packages to run the repo.  
- `a_star_algorithm/`:  folder containing the Snake game implemented using the A Star graph approach.  
- `ml/`: a folder containing the Snake game implemented using ML (Tensorflow and Keras).  
- `snake/`: a folder containing the usual Snake game, needs human interaction to be played.  

## Run the app:  
*N.B:* use Python 3.8  

**1. Clone the repo:**  
on your terminal, run `git clone https://github.com/maky-hnou/Awesome_Snake_AI.git`  
Then get into the project folder: `cd Awesome_Snake_AI/`  
We need to install some dependencies:  
`sudo apt install python3-pip libpq-dev python3-dev`  

**2. Install requirements:**  
Before running the app, we need to install some packages.  
- *<ins>Optional</ins>* Create a virtual environment:  To do things in a clean way, let's create a virtual environment to keep things isolated.  
Install the virtual environment wrapper: `pip3 install virtualenvwrapper`  
Add the following lines to `~/.bashrc`:  
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh
```
Run `source ~/.bashrc`  
Run `mkvirtualenv snake`  
Activate the virtual environment: `workon snake` (To deactivate the virtual environment, run `deactivate`)  
- Install requirements: To install the packages needed to run the application, run `pip3 install -r requirements.txt`  

*N.B:* If you don't have GPU, or don't have Cuda and Cudnn installed, replace `tensorflow-gpu` by `tensorflow` in requirements.txt.  

**3- Run the game:**  
### Run the A Star snake game:  
To run the A star snake game, get into the a_star_algorithm folder `cd a_star_algorithm` then run `python a_star_graph.py`  

*Demo:*  
<a href="https://github.com/maky-hnou/Dog_Breed_Classifier_API/blob/master/demo/demo.gif"><img src="https://github.com/maky-hnou/Awesome_Snake_AI/blob/master/demo/a_star.gif" title="astar-demo-gif"/></a>

### Run the ML snake game:  
The ml snake game has two modes:  
- *Training mode*: used to make the snake play random games and generate the data that will be used to train the snake model.  
- *Testing mode*: used to run the snake game using the pre-trained model (which exist in `ml/models/`).  
To run one of the modes, you need to get into the `ml/` folder (`cd ml/`)then run the following command:  
```
python main.py --mode <train/test>
```
Choose the mode you want to run.  
Alternatively, you can add other arguments (width, height, block, info_zone).

*Demo:*  
*Demo:*  
<a href="https://github.com/maky-hnou/Dog_Breed_Classifier_API/blob/master/demo/demo.gif"><img src="https://github.com/maky-hnou/Awesome_Snake_AI/blob/master/demo/ml.gif" title="ml-demo-gif"/></a>

[python-version]:https://img.shields.io/badge/python-3.8-brightgreen.svg
[issues-image]:https://img.shields.io/github/issues/maky-hnou/Awesome_Snake_AI.svg
[issues-url]:https://github.com/maky-hnou/Awesome_Snake_AI/issues
[fork-image]:https://img.shields.io/github/forks/maky-hnou/Awesome_Snake_AI.svg
[fork-url]:https://github.com/maky-hnou/Awesome_Snake_AI/network/members
[stars-image]:https://img.shields.io/github/stars/maky-hnou/Awesome_Snake_AI.svg
[stars-url]:https://github.com/maky-hnou/Awesome_Snake_AI/stargazers
[license-image]:https://img.shields.io/github/license/maky-hnou/Awesome_Snake_AI.svg
[license-url]:https://github.com/maky-hnou/Awesome_Snake_AI/blob/master/LICENSE
