# Tetris pygame

This is a test project where I wanted to learn a bit of pygame just for fun.

The start of this project was inspired byt a chanllenge I set to myself, to build a tetris machine using Arduino. Also the idea was to build it entirely from scratch, including developing the game itself. Despite the vast list of Open Source options found
in GitHub.

Since I was not so experienced with Arduino, I decided to wirte Tetris using pygame which would help me with some decisions of how the game should be written and then I could transfer that knowledge to my Arduino code.

## Running the game on the Desktop

This project uses [poetry](https://python-poetry.org/) as package manager and [pydev](https://www.pydev.org/) to manage the version of python.

Install the dependencies listed in `pyproject.tolm`.

`poetry shell`
`poetry install`

`python src/main.py`


### Running the game on a web browser

The main loop of the application is `async` so it can be coverted to webassembly using pygbag.

`pygbag src`
