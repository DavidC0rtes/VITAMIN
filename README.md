# VITAMIN

VITAMIN is an open-source model checker tailored to the verification of Multi-Agent Systems (MAS). MAS descriptions are given by means of labelled transition systems.
VITAMIN supports a set of specifications, including Computation Tree Logic (CTL), Alternating-time Temporal Logic (ATL), and more. 

The VITAMIN tool operates on Streamlit, an open-source app framework used for creating web apps. Thus, VITAMIN runs on all architectures (e.g., Linux, Mac, and Windows). 

The tool takes as input:
- A text file representing the model. This file can be manually created by the user (in a guided way), or interactively deployed via VITAMIN’s user interface.
- A text box representing the logical formula under exam. Such a text box is part of the graphical user interface.

Then, VITAMIN applies the corresponding model checking algorithm for the chosen temporal logic. 

<!-- Currently, VITAMIN supports Concurrent Game Structures (CGSs) as models, and CTL, ATL, and ATLF as specifications. 
The CGS consists of states of the MAS and transitions that are labeled with actions taken by each agent.  -->

## User guide

<!-- VITAMIN can be accessed at the following link: https://vitamin.streamlit.app/ -->

In the dashboard (on the left side), two options can be found:
- Non-Expert User
- Expert User

### Non-Expert Users

You can interact with the user interface to generate the model and the formula to be model checked. 
<!-- The system will ask you a sequence of questions to populate the MAS. Such a sequence starts with the number of agents to include in the MAS to analyse. In this step, you can also decide which name to give to each of the agents so created. After that, the system will ask for the number of states to have in the CGS. Again, like before, it will be possible for you to decide which names to give to the states so added. Finally, the system will ask for the actions to be performed by the agents, which you can customise, moreover, the system will also require you to specify which actions -- in which states -- the agent will be able to perform (i.e., by defining in this way the transition function amongst states in the CGS). -->
The following steps will happen:
- The system will prompt the user to specify the number of agents to include in the MAS for analysis.
- Users will have the option to assign names to each agent created during this step.
- Following the agent creation, the system will request the number of states to be included in the model.
- Users will once again have the opportunity to assign names to the states added to the model.
- Finally, the system will ask users to define the actions to be performed by the agents.
- Users can customize these actions according to their requirements.
- Additionally, users will need to specify which actions, in which states, the agents will be able to perform, thus defining the transition function among states in the model.

Once the system has gathered all the above mentioned information, a graph will be shown to the user to be checked.

The last step now is to perform the actual verification of the MAS created previously. This will be achieved by deciding which formalism -- amongst the available ones in VITAMIN -- to use to specify the formula of interest. After that, inside a specific text box, it will be possible to insert the formula (according to the formalism chose in the previous step).

The process concludes with the verification of the formula and the reporting of the verification result in VITAMIN's GUI.
Such result comprises the following: 
- the states from which the formula holds;
- the model checking result, that is the verification outome considering the initial state(s) of the model;
- the time the verification process required to conclude.

### Expert Users

A text file describing the model (i.e., the MAS) can be uploaded (see in more detail the section 'Input Model'). 
To do so, first the "Browse files" button needs to be pressed. This allows selecting the text file to upload. After that, the "Upload Data" button can be pressed. This will perform the actual upload of the file.

Once the file has been uploaded, in the "Logic Selection" section, the logical formula to verify can be typed.

To perform the model checking of the model w.r.t. the typed formula, the "Next: To Model Checking" button can be pressed. This will execute the model checker.
The verification result comprises the following: 
- the states from which the formula holds;
- the model checking result, that is the verification outome considering the initial state(s) of the model;
- the time the verification process required to conclude.

<!-- ### Case Studies

In this section there are some examples to interact with the VITAMIN tool. -->

### Input Model

The text file given in input is a TXT file with the following attributes:
- Transition: a matrix where row and columns denote the transitions involved in the MAS.
- Unknown_by: a matrix where the indistinguishability relations are defined (it is optional).  
- Name_State: a list of states that follows the same order of the transition matrix (i.e., the i-th element represents the i-th row and i-th column in the matrix).
- Initial_State: the unique initial state of the MAS.
- Atomic_propositions: a list of atomic propositions used in the MAS.
- Labelling: a matrix where the rows represent the states, while the columns represent the atomic propositions. Also in this case the columns are ordered w.r.t. the atomic propositions (i.e., the i-th atomic proposition truth values can be derived by the i-th column in the labelling matrix).
- Number_of_agents: the number of agents in the MAS.

## Developer Guide

VITAMIN is compositional and divided in three main components:
- Logic component
- Model component
- Model Checking component

### Logic component

In the logics folder, all the Python scripts regarding the support of all the logics in VITAMIN are present. 

In case a developer wants to extend VITAMIN with a new logic formalism, all that is needed is to add a corresponding folder inside the logics folder. Inside such a folder then, the developers can implement -- as they prefer -- the parsers for the new logics to be included in VITAMIN.

Note that, even though the supported logics' parsers have been implemented via yacc, new logics' parsers can be implemented freely (for example, with ANTLR, and so on).

### Model component

In the models folder, all the Python scripts regarding the support of all the models in VITAMIN are present.

In case a developer wants to extend VITAMIN with a new model formalism, all that is needed is to add a corresponding folder inside the models folder. Inside such a folder then, the developers can implement -- as they prefer -- the parsers for the new models to be included in VITAMIN.

### Model Checker Interface component

In the model_checker_interface folder, all the Python scripts to perform the actual verification of the logics and models supported in VITAMIN are present.

In case a developer wants to extend VITAMIN with a new verification mechanism, all that is needed is to add a corresponding folder inside the model_checker_interface folder. Inside such a folder then, the developers can implement -- as they prefer -- the algorithms to achieve the verification of models against formulas.
Notice that, in this folder there is a directory for each verification approach. For example, directories for implicit, explicit, and abstract approaches can be found.

Note that, the addition of a verification mechanism may not be tied to the addition of a corresponding new logic or model formalism. Indeed, new verification mechanisms can be added to handle existing logics and models in VITAMIN as well.

### How to integrate the modification in VITAMIN

Here, the public repository containing the skeleton architecture of VITAMIN can be found: ....

After the logics and models are added in VITAMIN, the last step is to make such logics and models available to end-users (both non-expert and expert ones). To do so, it is necessary to modify the front_end_CS.py Python script. Specifically, such modification requires the following.

In the callback function attached to the 'Next : To Model Checking' button, the developer needs to add an additional case to handle the newly introduced logic in the corresponding dropdown menu.

For example, the code to add would look like this:
```python
elif Logic == 'NEWLOGIC':
    from model_checker_interface.NEWLOGIC import NEWLOGIC
    result  = NEWLOGIC.model_checking(formula, filename)
    del NEWLOGIC
    st.write(result['res'])
    st.write(result['initial_state'])
```
where NEWLOGIC is the name of the logic which has been introduced by the developer.