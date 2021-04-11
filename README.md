# Smartwardrobe
CMU ECE 18500 Capstone - Smart Wardrobe 

There will be some dependencies on running this code. 

User Interface - We will be using Flask for backend so in order to run we need to pip3 install -U Flask
After this, we would do export FLASK_APP:flask_practice.py


Retriever -> we will be using pyserial to communicate with the arduino
pip3 install -U pyserial

Hardware -> servo needs to be able to rotate hanger with 35kg

stuff that I need to do today
-> implement center of mass function to find optimal place of clothing
-> debug the servo and the get angle function
-> retriever doesn't need to be in a while loop
-> flask debug
