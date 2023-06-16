# VITAMIN

VITAMIN is an open-source model checker tailored to the verification of Multi-Agent Systems (MAS). MAS descriptions are given by means of labelled transition systems.
VITAMIN supports a set of specifications, including Computation Tree Logic (CTL) and Alternating-time Temporal Logic (ATL) operators. 

The VITAMIN tool operates on Streamlit, an open-source app framework used for creating web apps. Thus, VITAMIN runs on all architectures (e.g., Linux, Mac, and Windows). 

The tool takes as input:
- A text file representing the model. This file can be manually created by the user, or interactively deployed via VITAMIN’s user interface.
- A text box representing the logical formula under exam. Such a text box is part of the graphical user interface.
Then, VITAMIN applies the corresponding model checking algorithm for the chosen temporal logic. 

Currently, VITAMIN supports Concurrent Game Structures (CGSs) as models, and CTL, ATL, and ATLF as specifications. 
The CGS consists of states of the MAS and transitions that are labeled with actions taken by each agent. 

## How to use

VITAMIN can be accessed at the following link: https://vitamin.streamlit.app/

In the dashboard (on the left side), you can find three options:
- Model Checking for MAS
- Case Studies
- Parser

## Model Checking for MAS

There are two options:
- Create MAS
- Upload File

If the latter is selected, then a text file describing the model (i.e., the MAS) can be uploaded. 
To do so, first the "Browse files" button needs to be pressed. This allows you to select the text file to upload. After that, the "Upload Data" button can be pressed. This will perform the actual upload of the file.

Once the file has been uploaded, in the "Logic Selection" section, you can type the logical formula to verify.

To perform the model checking of the model w.r.t. to the typed formula, you can press the "Next: To Model Checking" button. This will execute the model checker.
