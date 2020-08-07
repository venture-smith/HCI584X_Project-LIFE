# HCI584X_Project-LIFE
LIFE (Learning Important Factual Equivalents) Food & Exercise is a POC (proof of concept) app that allows the user to select a specific fast food entree/item and compare it to up to three physical activities. The user will see how certain many minutes of a particular physical activity is required to offset the equivalent calories of a specific food item. 

The program has 4 simple steps: 1. Choosing up to 3 physical activities, 2. Specifying weight, 3. Selecting a fast food restaurant and food item, and 4. Reviewing the results and MemeCards.

MemeCards are pithy sayings overlaid on an image of the food item, an example "The horrible realization that this (the food item) is the equivalent of XX minutes of YY (activity)"

The Cards are meant to be fun and entertaining - with the original intent of the POC to be able to share the Cards through Social Media and email (not implemented). 

# Requirements
- Python 3.7 or higher
- [tkinter]https://docs.python.org/3/library/tkinter.html)
- [pillow](https://pypi.org/project/Pillow/) 7.2 or higher 

# Installation 
- No additional packages required on install.
Pillow==7.0.0

# Usage
- `main.py`: run in the project root folder, "python main.py"

# Known issues
1. MOST OF THE POTENTIAL ERRORS ARE TRAPPED AT STEP 3: The majority of possible error conditions have been accounted for and a check is made at Step 3. You will be unable to see the Results or MemeCards without correctly 1. Selecting at least one activity, 2. Specifying a weight between 25 - 250 kgs or 50 and 500 lbs, and 3. Selecting a restaurant and food item. 

2. TEXT FORMATTING OF FOOD ITEM IN STEP 3: There was insufficient time to fix the formatting of the text in Step 3. for the selected Food Items. In several cases, the selected food item string is too long, and is truncated at the front and the back. This has no effect on the ability of the program to show the correct equivalency values and to display the Meme Card.

3. MEME CARD TEXT TRUNCATION: There may be some iterations of the Meme Cards where the text strings are insufficiently formatted, and are also truncated in rendering.

4. BACKGROUND CONTRAST: There may be some backgrounds where the contrast between the text and the background clash badly. A possibe future feature would be to allow the user to change the color of the text and shadow/outline.

5. IMAGE CENTERING/PLACEMENT: Because of the diverse sources of the food images, some of the items may not be correctly centered and may be too low or too high. In some cases the images may be too small or of insufficient resolution.

6. DISCLAIMER: The program does not include text that gives more accurate advice regarding the average number of calories burned in a daily wakeful activity (e.g. - walking, breathing, sitting still). The equivalent values given assume that any other net calories in or out are zero, and that the food item is excess beyond the required calories an average individual needs to maintain homeostasis. In addition, the program does not specify that the burn rate is based on the average calories burned using a heart rate monitor during specific activities, assuming specific weights of individuals. Genetic variation as well as the exact amount of exertion in each activity may vary greatly. The descripton of the amount of exertion is also fairly subjective. As a result, the results given here are for directional use only, and not to be used as medical advice.

# Acknowledgments
Thanks to Professor Harding, Iowa State University for his guidance and troubleshooting on this project.
