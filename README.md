# Congo-Market

WHEN RUNNING THIS:

-You will need to setup the virtual machine in python yourself. It is gitignored by default so everyone should make there own and run the command to activate it

venv\Scripts\activate  will start your virtual machine
deactivate             will stop your virtual machine

note: When using pythong version 3.12, the commands for python have shifted from python -> py ex. python -m venv venv -> py - m venv venv
note: Python dependencies installed inside of you virtual machine will not work outside your virtual machine and vice versa. 

-Running requries two terminals open. One should be cd into your react folder where you will -npm start
Ther other one will be cd into the python folder where you will                          uvicorn main:app --reload 

-Two things you might have to install for things to work to work:

npm install axios
npm install react-router-dom --save
pip install sqlalchemy

