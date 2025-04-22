# Project Icaras - Group_09

## Description

This is a group project for the Advanced Programming Summer 2024 course at NOVA SBE. The python-based tool is designed for comprehensive analysis of commercial air travel data, with a focus on sustainability. Developed for the International Air Transport Association's dataset, it provides insights into flight patterns, airplane usage, and potential decarbonization strategies. 

Please check the project outline at the bottom for a more detailed description.

## Project Documentation

For more detailed information about Project Icarus, including architecture, function descriptions, class details, and usage examples, please visit our project documentation:

You can find the index.html file for that here: /docs/_build/html/index.html

Our documentation is designed to help users and developers understand the inner workings of Project Icarus, making it easier to utilize or contribute to the project. It includes:

## Usage

### Environment Setup & Showcase Notebook

To get started with our project, follow these steps to set up your environment and run the showcase notebook, which demonstrates the project's capabilities.

**Step 1: Clone the Repository**
First, clone the repository to your local machine using Git. Open your terminal (or command prompt) and run the following command:

    git clone https://gitlab.com/adpro3080008/group_09

**Step 2: Navigate to the Project Directory**
Change into the project directory using the cd command:

    cd group_09

**Step 3: Install Dependencies**

Our project uses a Conda environment to manage dependencies. 

Create and install the project's dependencies by running:

    conda env create -f environment.yml

This command reads the environment.yml file and sets up an environment with all the necessary Python packages.

**Step 4: Activate the Environment**

Once the environment is created, activate it with:

    conda activate adpro_group09

**Step 5: Run the Showcase Notebook**

In order to run in the entire notebook, including LLM based methods (aircraft_info and airport_info) via ChatOpenAI, here's how to setup a system variable:

Windows
https://support.microsoft.com/pt-pt/topic/how-to-manage-environment-variables-in-windows-xp-5bf6725b-655e-151c-0b55-9a8c9c7f747d

MAC
https://phoenixnap.com/kb/set-environment-variable-mac

Use a system variable name called OPENAI_API_KEY with the value of your key.


### Unit Test for distance Function in distances.py

This suite tests the distance function located in source/Functions/distances.py through three scenarios using pytest:

- Input Validation Test: Verifies that a TypeError is raised if any input is not a number, ensuring robust error handling.
- Intercontinental Distance Test: Calculates the distance between Duesseldorf Airport and San Diego Airport, expecting a specific value in kilometers (precision to the nearest kilometer). This test assesses the function's accuracy over long distances.
- Identical Points Test: Confirms that the function returns a distance of 0 when both input points are identical, testing the function's handling of edge cases.

**Preparation:**

Ensure pytest and any other required libraries are installed.
Navigate to the project root directory.

**Execution:**
Run the tests by executing pytest source/Test/test_distances.py in your terminal. Review the output to verify that all tests pass.

## Files

We have added our input files from Gitlab Project AdPro2024.

https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false


## Authors and acknowledgment

Adam Bernard - 60865 - 60865@novasbe.pt

Hendrik Künnemann - 57995 - 57995@novasbe.pt

Moritz Lind - 61230 - 61230@novasbe.pt

Luc Marc Pellinger - 58611 - 58611@novasbe.pt

## License

Project Icarus is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3, dated 19 November 2007. This license allows you to:

- Use: You are free to use Project Icarus for personal, academic, or commercial purposes.
- Modify: You can alter and extend the source code for your needs.
- Distribute: You are allowed to share the software in its original or modified form.

However, there are conditions you must follow:

- Disclose Source: If you modify and distribute the software, you must also disclose your source code under the same license.
- Network Use Is Distribution: If you run a modified version of the software on a server and allow others to use it, you are required to provide the source code under this license.
- Same License: Modified versions must be licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3 or later.

For a detailed explanation of the license and your rights under it, please refer to the LICENSE file included with this project or visit the GNU AFFERO GENERAL PUBLIC LICENSE Version 3 official page: https://www.gnu.org/licenses/agpl-3.0.en.html

## Project status
Completed

______

## Part 1

### Structure of the project
You are going to build a Showcase Notebook that doubles as a presentation for your analysis.
Keep all the .py files in separate directories. The only files in the main directory of the project should be the Showcase Notebook and the several configuration files (.yml, .gitignore, and others). Everything else should have their own directories.


### Day 1, Phase 1.1


- [ ] One of you will create a gitlab/github repository (it does not matter who). THE NAME OF THE REPOSITORY MUST BE "Group_XX" where XX is the number of your group! If you are group 3, then XX must be 03. Always use two digits and an underscore!
- [ ] Initialize the repo with a README.md file, a proper license, and a .gitignore for the programming language you will use. The README.md file MUST have your emails in a way that it is possible to copy and paste it into an email.
- [ ] The one who created the repository will then give Maintainer permissions to the rest of the group. Check under "Project Information" > "Members".
- [ ] Every element of the group clones the repository to their own laptops.


### Day 1, Phase 2


- [ ] The class you decide the create for the project has finally been named after a brief internal fight and is PEP8 compliant, like the entire project.

The class will have several methods, which you will not develop in the master branch.
Document everything!
Make your calls compliant with pydantic and static type checking when appliable.

- [ ] During the init method, your class must download the data file into a downloads/ directory in the root directory of the project (main project directory). If the data file already exists, the method will not download it again.
- [ ] The init method must also read the datasets into a corresponding pandas dataframe which become attributes for your class. Remove superfluous columns.
- [ ] Develop a function to calculate the real distances between airports in kilometers in its own .py file with the information in the datasets. Approximate the earth to a sphere (it is safe to disregard altitude). Develop a unit test to this function with three cases, where one must be between two airports in different continents. Implement a way to make the distances between airports part of the information contained in your future class instance.


### Day 1, Phase 3


- [ ] Develop a first method that takes a country as an input and plots a map with the locations of its airports (as well as a map for that country). If the country does not exist, return a useful error message. DO NOT USE INTERACTIVE PROMPTS; IT SHOULD REALLY JUST BE AN ARGUMENT!
- [ ] Develop a second method called distance_analysis. This should plot the distribution of flight distances for all flights.
- [ ] Develop a third method that receives an airport as an input and an optional argument called internal with a value of False by default. If internal is True, then this method should plot only the flights leaving this airport with a destination in the same country. Otherwise, it plots all flights.
- [ ] Develop a fourth method that may receive a string with a country or a list of country strings but has None by default. This method should plot the N most used airplane models by number of routes. If the input argument is None it should plot for all dataset. If it receives only a country or list of countries, it should plot just for that subset.
- [ ] Develop a fifth method that receives a country name as an input and an optional argument called internal with a value of False by default. If internal is True, then this method should plot only the flights leaving the country with a destination in the same country. Otherwise, it plots all flights. This is analogous to the third method, but for country now.


### Day 1, Phase 4


 - [ ] Make a "showcase notebook" where you import your Class and showcase all the methods you developed. Tell a story about your analysis and findings in the showcase notebook. Use all methods with several complementary options. If you feel lost about what story to tell, don't hesitate to contact the professor.


     REMEMBER: The first delivery is until March 4 23:59:59 and it is not graded. It is used as course correction. The delivery is the git repo link.
     The notebook must RUN from start to finish. If one runs all cells again, the output must be the same.
     REMEMBER: IT IS OK TO PROTOTYPE CODE IN NOTEBOOKS, BUT THE FINAL CLASS MUST BE IN A SINGLE .py FILE!  
     The final delivery of the project is the "showcase" notebook from Phase 4. Don't place this notebook together with prototyping notebooks.
     Prototyping notebooks must have their own separate directory.
     We will only consider contents in your "master" repository. 
     
     When in doubt, ask.

## Part 2
---
### Rules
1. Be sure that the group submits [the link to the repo on moodle](https://moodle.novasbe.pt/mod/assign/view.php?id=318193).
2. We will pull the existing versions by 0:00, Saturday 16 March 2024. Remember: the pushes have a timestamp!

---
<div class="alert alert-danger">
    <b> NEVER USE USER PROMPTS, IT IS INFINITELY ANNOYING!! </b>
    <br>
    <b> Always use arguments for your methods.</b>
</div>


---
### Scenario (continuation)

Your company was asked to analyse Commercial Airfligh data for a sustainability study. Your group is the best team of Data Scientists in the company's roster and are given the challenge. By undertaking this task, your company expects to contribute to the green transition by having a more savvy taskforce. You decide to create some python tools for the challenge.

You spent the first day doing a lot of the code heavy lifting. It is now time to do some polishing. As you know your project might be picked up for an analysis presentation, you add an introduction about your group on the _README.md_ file. Be sure to add your **names**, **your student numbers** and **your e-mails**. It is time to add more features to the class so you can present the analysis in the showcase notebook.

### Goal
For this project, we will be using data from [International Air Transport Association](https://www.iata.org/). The datasets can be found [here](https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false).

Go over the datasets. You were not given a data dictionary, but the fields can be easily discovered with an online search, as this is heavily used data.

<div class="alert alert-danger">
    <b> THE MOST IMPORTANT TOOLS FOR A DATA SCIENTIST IS PATIENCE AND COMMUNICATION</b>
    <br>
    <b> Discuss the contents of the dataset with your colleagues. Understanding the data is a priority. </b>
</div>

Use whatever python tools you find apropriate.


### Day 2, Phase 1: Add Info with an LLM

- [ ] Define a new method called **aircrafts** that receives no arguments and prints only the list of aircraft models (Names)i r c r a f .
- [ ] Define a new method called **aircraft_info** that receives a string called _aircraft_name_. If the string is **NOT** in the list of aircrafts in the data, it should return an exception and present a way to guide the user into how they could choose a correct aircraft name.
- [ ] The latter method should use an LLM to print out a table of specifications about the aircraft model in Markdown.
- [ ] Define a new method called **airport_info** that does the same but for airports (don't make checks in this method, you are already demonstrating you understood it in the case for aicrafts).

<div class="alert alert-danger">
    <b> Do not include the API KEY in the project. Declare the API KEY as a system variable.</b>
    <br>
    <b> If the API KEY is not working, let me know ASAP. </b>
</div>

### Day 2, Phase 2: Decarbonisation

For this project, and for the sake of simplicity, flights under 1000km can be considered short-haul flights, although [there are several definitions](https://en.wikipedia.org/wiki/Flight_length).  
Let's do a mini-case study: Choose a country with more than 20 internal routes. This already accounts for "A to B" and "B to A".

- [ ] Refine the fifth method from Day 1: it should now also receive a float, which will be the cutoff distance for short-haul flight definition. The plot should now reflect the difference between long-haul and short-haul flights (use color, be considerate to color blind people), using the cutoff distance selected in the argument.
- [ ] How many flight routes could be considered short-haul for your country of choice? What is the total distance between airports considered short-haul flights? Print this info as a plot annotation. (Please note we want total distances, don't double count routes "A to B" and "B to A").
- [ ] Research question: a plan to cut emissions is to replace short-haul flights with rail services. Find a reference for the ratio between emissions from flights and your alternative (just a ballpark number from a credible source, include a link to your source in the showcase notebook). Taking into account all flights from your country, both internal and external, by how much would you lower flight emissions? Refine the method to also add this as an annotation onto the plot. 

### Day 2, Phase 3: Cleaning up

- [ ] Add a yaml file to git with all the packages you used, a conda environment file. This file will be used to generate an environment where your code will be ran. Remember to make it OS independent.
- [ ] Use sphinx to generate a __docs__ directory that will showcase the documentation of your code. Remember to comment .gitignore appropriately so everything is included. Update README.md to tell the user how to start using the project.

---
## Grading

Between the two parts, there are 20 gradable items in both Part 1 and 2. All items are 1 point out of 20 except for Day 1, Phase 1, which is 1 point total for the 4 items (correctly setting up git remote).

<div class="alert alert-danger">
    <b> REMEMBER: IT IS OK TO PROTOTYPE CODE IN NOTEBOOKS, BUT THE FINAL CLASS MUST BE IN A SINGLE .py FILE! </b>
    <br>
    <b> The final delivery of the project is the "showcase" notebook. Don't place this notebook together with prototyping notebooks.</b>
    <br>
    <b> Prototyping notebooks must have their own separate directory.</b>
    <br>
    <b> We will only consider contents in your "master" repository before the end of the deadline.</b>
</div>
