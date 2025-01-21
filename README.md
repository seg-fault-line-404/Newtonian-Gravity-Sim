# Newtonian-Gravity-Sim

The title is pretty self explanatory.

This is my group's attempt to simulate movement of objects in free space using goold ol' Newtonian physics
paired with Euler integration. It is a very crude attempt at being accurate to the actual movements of
such bodies as would be predicted with modern physics (namely relativity), but the focus of this work is not
accuracy to modern physics (even to Newtonian), but the actual programming:

- How to create an object that would contain all the data required to completely describe the state of a
    heavenly body under Newtonian physics (position and momentum).
- How to make a function that would take an arbitrary number of said objects and simulate their interactions'
    effects on their state.
- How to create an engine that would continuously perform these simulations and update the objects' data
    accordingly.
- How to create a window where the engine could draw to visually display the events.
- How to create and customize a GUI that would intuitively allow users to interact with the engine.

This initial upload is the exact program we submitted as a final requirement on our basic computer programming
class. It has been tested to run on Windows 10 and Windows 11, provided the requirements below are met.

# Requirements
- Python 3.12 or higher
  - TkInter
  - Pillow
  - keyboard
  - vpython
  
# How to run the program
First, install python from the website https://www.python.org/ . 

Then, clone this repository anywhere on your Windows device using
either git, or by downloading this in a zip then extracting.

QUICK NOTE: If you're not familiar with python, running a python file will open cmd. This is normal in this context
            and does not mean it's a virus. One indicator is that it does not ask for admin permissions when running.
            If you want further proof, you can try programming your own simple python program and run that. You will
            immediately notice the cmd window open when you run it from the File Explorer.

From here, you can do two things:
1. Run main.py. If any of the dependencies are not found, the program would prompt you if you want
     to install them. Type Y then press Enter and they'll automatically be installed for you.

2. Run cmd by pressing WindowsKey + R. Run the following commands
   - pip3 install vpython
   - pip3 install pillow
   - pip3 install keyboard
   
   If installation of all three were successful, you should be able to run main.py without any problems.

# Simulating
Running main.py should take you to the user interface. **Do not close the cmd window in the background** as that
will end the program.
1. Press start on the lower right corner.
2. Use the buttons on the right to add or remove bodies in the simulation
3. Input the initial details required. Only integers and floating point values are accepted. *Hint: there is no rule that checks for negative mass, so have fun with it!*
4. Press start. This should open a window on your default browser that shows the simulation. Its URL should be localhost (i.e. your computer's IP, not an internet IP).
5. Watch your spheres move.

You can control your view by holding the right mouse button and dragging. You can also move your camera forward
and backward by pressing W and S, respectively, and move faster by holding shift while moving.

Left and right movement haven't been implemented as they were too hard for me to formulate within reasonable time
back then.

Credits:

- Simulation Engine ------------------------------- Me
- Simulation Graphics ----------------------------- Me, Anonymous
- UI (Window) ------------------------------------- John Carl Camacho, 2 Anonymous
- Derivation and Accuracy of the formulas used ---- 2 Anonymous
