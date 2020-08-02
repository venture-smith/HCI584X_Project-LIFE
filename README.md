# Example of a project ReadMe (User's guide)
Start with a simple description of what your project does. This here gives examples of 2 simple project file/folder structures: 
1) main.py: imports from the stuff module (the local stuff.py file)
2) run_testpak.py: uses a simple package (called testpak) that can be installed via pip. 

# HCI584X_Project-LIFE
Learning Important Factual Equivalents (Calorie Edition) - Python
A small test app that translates common fast food menu items (that a User selects) to equivalent physical exercise duration/exertion level and healthy alternatives that people can more easily relate with. This information is meant to educate and entertain by helping the user understand the equivalent effort to offset consumption (provided the consumption is in excess of the minimum amount of calories for normal exertion throughout the day) as well as to share findings through messaging/social media in a consumable format a "Meme Card".


# Requirements
- Python 3.7 or higher
- [rich](https://github.com/willmcgugan/rich)
- [dill](https://dill.readthedocs.io/en/latest/dill.html) 0.3 or higher 

# Installation 
List what the user needs to do __before__ running your app 
for main.py
- use pip to install the required third party packages:  ` pip -r requirements.txt`

Pillow==7.0.0



for run_testpak.py
- use `pip` to build and install testpack as a local package and install required packages
- open a OS terminal, go into the project root folder and type: `pip install .` (<- dot!)

# Usage
Describe how to run your app
- `main.py`: run it in the project root folder, so it can import from the testpack folder
- `testpak.py`: can be run from any folder once it's been installed locally

# Code Examples
If your project code is meant to be integrated into python code, you should list at least a few usage examples that can be copy/pasted and run. For more complex cases, consider writing a separate tutorial (put it and its code into a separate folder called tutorial).
Here, I'll just give one of the functions that my package defines:

```
# use the evenOdd function
from testpak import evenOdd
x = int(input("Enter a number:"))
print(x, "is",  evenOdd(x))
```

# Known issues
List any known bugs and limitations

# Acknowledgments
If some project was instrumental in helping you with this project, consider listing it here.



# How to markdown?

see https://guides.github.com/features/mastering-markdown/ for a guide on markdown. 

Note that images need to be referenced, i.e. you will need to put them into a separate folder, here I've put an image into my docs folder:

![Alt text for image](docs/guido.png)
