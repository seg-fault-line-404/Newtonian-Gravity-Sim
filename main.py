import time

try:
    from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label
    from tkinter.constants import NORMAL, DISABLED
    from vpython import *
    from PIL import Image, ImageTk
    from keyboard import is_pressed, on_release_key
except:
    print("Can't run program. Please install the following dependencies:\n"
          "- TkInter\n"
          "- Vpython\n"
          "- keyboard\n"
          "- Pillow\n"
          "\n"
          "You can install them by opening the command line (windows key + r, enter 'cmd'\n"
          "Run the following commands:\n"
          "pip3 install tkinter\n"
          "pip3 install vpython\n"
          "pip3 install keyboard\n"
          "pip3 install pillow\n"
          "\n")
    x = input("Enter Y to install: ").upper()
    if x == "Y":
        import os
        os.system("pip3 install tkinter")
        os.system("pip3 install vpython")
        os.system("pip3 install keyboard")
        time.sleep(3)

# =================================== SIMULATION =================================== #

# Define Class used for simulation
class Body:
    def __init__(self, render, velocity, mass):
        self.render = render
        self.mass = mass
        self.velocity = velocity


# Define constants
G = 6.6743015  # Gravity
k = 1  # Do we implement this on charged particles as well?
bodies = []

# User-defined Constants / To be implemented
dt, dt_mem = 1000, 1000  # Lower = More accurate simulation, but uses more resources
sim_speed = 720          # Higher = Faster simulation speed, but uses more resources
# end_time = 12 * (10 ** 50)          # How long to run the program for; In seconds
fact = 100               # Trail factor: Higher = Longer Trails
m0 = 10 ** 27            # Default object mass
ax_l = 600               # Axis length


# Simulation Functions
def grav_acc(obj1=vec(0, 0, 0), obj2=vec(0, 0, 0), obj2_mass=0):
    if obj1 == obj2:  # Because we don't want to calculate the object's acceleration
        return vec(0, 0, 0)  # on itself

    # Input factor: r units = 1 million km, mass units = 10^26 kg, velocity units = 1 km/s
    return (G * obj2_mass * hat(obj2 - obj1) / (mag(obj2 - obj1) ** 2)) * (10 ** -6)
    # This function returns a dv in km/s


def dv_calc(obj):  # Input will be of the class [Body] defined above

    # effective_bodies = bodies       # This code recreates a copy of the list of bodies
    # effective_bodies.remove(obj)    # with the removal of the one we're calculating for
    # ------------------------------- # Code cancelled

    # This is where all the magic happens -------------------------------------------------

    position = obj.render.pos  # Extract the object's position
    dv = vec(0, 0, 0)  # Create a zero dv to return when there are no other bodies
    global bodies

    for thing in bodies:                                    # Loops over the entire list of bodies
        item_position = thing.render.pos                    # Extract the other object's position
        item_mass = thing.mass                              # Extract the other object's mass
        dv += grav_acc(position, item_position, item_mass)  # Adds this object's contribution to dv

    return dv


def save_bodies(raw_list):
    processed_list = []
    for item in raw_list:
        xp, yp, zp, xv, yv, zv, m = (item[0].get(), item[1].get(), item[2].get(), item[3].get(),
                                     item[4].get(), item[5].get(), item[6].get())

        body = Body(render=sphere(pos=vec(float(xp), float(yp), float(zp)), radius=10,
                                  make_trail=True, retain=fact
                                  ),
                    velocity=vec(float(xv),
                                 float(yv),
                                 float(zv)
                                 ),
                    mass=float(m)
                    )
        
        processed_list.append(body)
    global bodies
    bodies = processed_list


def pause_animation(self):
    global animation_playing, dt, dt_mem
    animation_playing = not animation_playing
    if animation_playing:
        dt = 0
        self.text = "Play"
    else:
        dt = dt_mem
        self.text = "Pause"


def start_simulation(self):

    global entries

    try:
        save_bodies(entries)
    except ValueError:
        messagebox.showerror("Simulation Failed", "Cannot simulate null values.\nPlease enter the complete "
                                                  "initial state(s).")
        return None

    self.destroy()
    arrow(pos=vec(-ax_l / 2, 0, 0), axis=vec(ax_l, 0, 0), shaftwidth=0.5, headwidth=.5, headlength=1,
                   color=color.red)
    arrow(pos=vec(0, -ax_l / 2, 0), axis=vec(0, ax_l, 0), shaftwidth=0.5, headwidth=.5, headlength=1,
                   color=color.green)
    arrow(pos=vec(0, 0, -ax_l / 2), axis=vec(0, 0, ax_l), shaftwidth=0.5, headwidth=.5, headlength=1,
                   color=color.blue)

    global bodies

    button(text="Pause", pos=scene.title_anchor, bind=pause_animation)
    t = 0
    scene.width, scene.height = window_width * 0.8, window_height * 0.8
    scene.camera.pos = vec(100, 50, 100)

    reticle = sphere(pos=vec(0, 0, 0), radius=1)
    scene.camera.follow(reticle)
    move_speed = 1
    while True: #t <= end_time:
        rate(sim_speed)

        trigger_timer = 0

        if trigger_timer != 0:
            trigger_timer -= 1

        elif is_pressed("shift"):
            if move_speed == 1:
                move_speed = 3
            else:
                move_speed = 1
            trigger_timer += 3 * sim_speed

        if is_pressed("w"):
            scene.center += scene.forward * move_speed/ 10
        if is_pressed("s"):
            scene.center -= scene.forward * move_speed / 10

        # Can't implement yet
        """
        up = rotate(vec(1, 0, 0), angle=(pi/2 - abs(diff_angle(scene.forward, vec(0, 1, 0)))), axis=scene.forward)
        left = rotate(scene.forward, angle=pi / 2, axis=up)
        if is_pressed("a"):
            scene.center += left / 10
        if is_pressed("d"):
            scene.center -= left / 10
        """

        t += dt
        reticle.pos = scene.center
        # Here's the tricky part
        for item in bodies:
            item.render.pos += item.velocity * dt / (10 ** 6)
            item.velocity += dv_calc(item) * dt


# ================================= SIMULATION END ================================= #


# ====================================== GUI. ====================================== #

# Standardizing Color Scheme
entry_cont_highlight_bg = "#5d667c"
entry_cont_highlighted = "#8b99ba"
entry_cont_bg = "#3e4453"
entry_space_bg = "#"
entry_space_text = "#abbadf"
entry_space_text_dark = "#2b2f3a"

# Global variables
entries = []
entry_space = []
window_height = 0
window_width = 0


# Defining main function
def transition(self, to):
    if self is not None:
        self.destroy()
    if not to:
        main_menu()
    else:
        launcher_settings()


# Each entry will consume a space spanning 1/10 of the total window
def add_entry(parent):
    global entry_space, entries, window_height, window_width

    if len(entry_space) > 4:
        return None

    container = Canvas(
        parent,
        background=entry_cont_bg,
        highlightthickness=parent.winfo_height() * 0.12 * 0.025,
        highlightbackground=entry_cont_highlight_bg,
        highlightcolor=entry_cont_highlighted
    )

    container.place(
        relx=0.05,
        rely=0.2 + len(entry_space) * 0.15,
        relwidth=0.75,
        relheight=0.12,
        anchor="nw"
    )

    # Position
    xpos = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    ypos = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    zpos = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    # Velocity
    xvel = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    yvel = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    zvel = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    # Mass
    mass = Entry(
        container,
        bd=0,
        bg="#D9D9D9",
        fg=entry_space_text_dark,
        highlightthickness=0,
    )

    # Render the entries field on the frame
    xpos.place(relx=0.25, rely=0.075,
               relwidth=0.15, relheight=0.4,
               anchor="nw")
    ypos.place(relx=0.25 + 0.175, rely=0.075,
               relwidth=0.15, relheight=0.4,
               anchor="nw")

    zpos.place(relx=0.25 + 0.35, rely=0.075,
               relwidth=0.15, relheight=0.4,
               anchor="nw")

    xvel.place(relx=0.25, rely=0.925,
               relwidth=0.15, relheight=0.4,
               anchor="sw")

    yvel.place(relx=0.25 + 0.175, rely=0.925,
               relwidth=0.15, relheight=0.4,
               anchor="sw")

    zvel.place(relx=0.25 + 0.35, rely=0.925,
               relwidth=0.15, relheight=0.4,
               anchor="sw")

    mass.place(relx=0.995, rely=0.075,
               relwidth=0.15, relheight=0.4,
               anchor="ne")

    # Labels!!!
    # Create general use constants to be used throughout
    cont_height = window_height * 0.12
    cont_width = window_width * 0.75
    font_size = int(cont_height * 0.12)

    container.create_text(
        cont_width * 0.025,
        cont_height * 0.5,
        anchor="w",
        text=("Object " + str(len(entry_space) + 1)),
        fill=entry_space_text,
        font=("LeagueSpartan Regular", int(cont_height * 0.2)),
        justify="left"
    )
    container.create_text(
        cont_width * 0.21,
        cont_height * 0.275,
        anchor="e",
        text="Position",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="right"
    )

    container.create_text(
        cont_width * 0.21,
        cont_height * 0.725,
        anchor="e",
        text="Velocity",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="right"
    )

    container.create_text(
        cont_width * 0.245,
        cont_height * 0.275,
        anchor="e",
        text="x",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    container.create_text(
        cont_width * 0.245,
        cont_height * 0.725,
        anchor="e",
        text="x",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    container.create_text(
        cont_width * 0.42,
        cont_height * 0.275,
        anchor="e",
        text="y",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    container.create_text(
        cont_width * 0.42,
        cont_height * 0.725,
        anchor="e",
        text="y",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    container.create_text(
        cont_width * 0.595,
        cont_height * 0.275,
        anchor="e",
        text="z",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    container.create_text(
        cont_width * 0.595,
        cont_height * 0.725,
        anchor="e",
        text="z",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    container.create_text(
        cont_width * 0.835,
        cont_height * 0.275,
        anchor="e",
        text="Mass",
        fill=entry_space_text,
        font=("LeagueSpartan Regular", font_size),
        justify="left"
    )

    # Append to entries list, in the correct order: [ pos x, y, z, vel x, y, z, mass]
    entries.append([xpos, ypos, zpos, xvel, yvel, zvel, mass])
    entry_space.append(container)


def remove_entry():
    global entries, entry_space
    if not len(entry_space):
        return None
    for item in entries[-1]:
        item.place_forget()
    entries.pop(-1)

    entry_space[-1].place_forget()
    entry_space.pop(-1)


# ====================================== GUI. ====================================== #


# Windows here
def main_menu():
    window = Tk()
    window.resizable(False, False)

    global window_width, window_height
    window_width = int(window.winfo_screenwidth() * 0.8)
    window_height = int(window.winfo_screenheight() * 0.8)

    window.title("Gravitational Interaction Simulator")

    window.geometry(f"{int(window_width)}x{int(window_height)}")

    btn_wdt = window_width / 10
    btn_ht = window_height / 10

    # Load all window images
    main_bg_image_setup = ImageTk.PhotoImage(Image.open("Assets/bg/main.png").resize((window_width + 10, window_height)))
    # main_bg = Label(window, image=main_bg_image_setup)
    # main_bg.image = main_bg_image_setup

    start_btn = PhotoImage(file="Assets/btn/start.png")
    exit_btn = PhotoImage(file="Assets/btn/exit.png")

    main_menu_bg = Canvas(
        window,
        width=window_width,
        height=window_height,
        bd=0,
        highlightthickness=0
    )

    main_menu_bg.place(x=0, y=0)
    main_menu_bg.create_image(0, 0, anchor="nw", image=main_bg_image_setup)
    # main_bg.place(x=-5, y=0, anchor="nw")

    # Exit button
    exit_b = Button(
        image=exit_btn,
        bg="#3F506A",
        activebackground="#7ea0d4",
        borderwidth=0,
        highlightthickness=0,
        command=window.quit,
        relief="flat"
    )

    exit_b.place(x=0, y=window_height - btn_ht, width=btn_wdt, height=btn_ht)

    # Start Button
    start_b = Button(
        image=start_btn,
        bg="#3e4453",
        activebackground="#7c88a6",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: transition(window, 1),
        relief="flat"
    )

    start_b.place(x=window_width - btn_wdt, y=window_height - btn_ht, width=btn_wdt, height=btn_ht)

    # Justified text (description)
    main_menu_bg.create_text(
        window_width/2,
        window_height * 5/9,
        anchor="center",
        text="The Gravitational Interaction Simulator is a tool designed to explore the complex dynamics "
             "of celestial bodies in space. By simulating gravitational forces, users can visualize planetary orbits, "
             "predict trajectories, and analyze interactions between celestial objects.",
        fill="#dddddd",
        width=window_width * 2/3,
        font=("LeagueSpartan Regular", min(int(window_width/45), int(window_height/20))),
        justify="center"
    )

    window.mainloop()


def launcher_settings():
    window = Tk()
    window.resizable(False, False)

    window.title("Newtonian Gravity Simulator")

    window.geometry(f"{window_width}x{window_height}")
    window.configure(bg="#000000")

    # For buttons
    btn_size = int(window_width / 20)

    # Again, load all images
    rem_ent = Image.open("Assets/btn/remove_entry.png").resize((btn_size, btn_size))
    add_ent = Image.open("Assets/btn/add_entry.png").resize((btn_size, btn_size))

    bg_img = PhotoImage(file="Assets/bg/bg.png")
    add_entry_btn = ImageTk.PhotoImage(add_ent)  # , master=add_obj)
    remove_entry_btn = ImageTk.PhotoImage(rem_ent)

    # Button Colors
    btn_onClick = "#7c88a6"
    btn_inactive = "#4a5264"

    launcher_bg = Canvas(
        window,
        bg="#FFFFFF",
        height=window_height,
        width=window_width,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    launcher_bg.create_image(window_width / 2, window_height / 2, image=bg_img)
    launcher_bg.place(relx=0, rely=0)

    # Justified text (description)
    launcher_bg.create_text(
        window_width / 2,
        window_height / 10,
        anchor="center",
        text="Simulation Bodies",
        fill="#FFFFFF",
        font=("LeagueSpartan Regular", int(window_height / 20)),
        # width=1000,
        justify="center"
    )
    launcher_bg.create_text(
        window_width / 2,
        window_height * (1/10+1/15),
        text="position in million km,   velocity in km/s,   mass in 10^26 kg",
        anchor="center",
        font=("LeagueSpartan Regular", int(window_height / 60)),
        fill="#FFFFFF",
        justify="left"
    )

    add_obj = Button(
        text="Add Object",
        bg=btn_inactive,
        activebackground=btn_onClick,
        borderwidth=btn_size/50,
        command=lambda: add_entry(window),
        relief="flat",
        image=add_entry_btn
    )

    remove_obj = Button(
        text="Remove Last Object",
        command=lambda: remove_entry(),
        borderwidth=btn_size / 50,
        relief="flat",
        bg=btn_inactive,
        activebackground=btn_onClick,
        image=remove_entry_btn
    )

    simulate = Button(
        text="Start",
        command=lambda: start_simulation(window),
        borderwidth=btn_size / 50,
        bg=btn_inactive,
        foreground=entry_space_text,
        font=("LeagueSpartan Regular", int(btn_size/5)),
        activebackground=btn_onClick,
        relief="flat"
    )

    add_obj.place(x=window_width * (37 / 40) - btn_size, y=window_height * 27 / 60 - btn_size,
                  width=btn_size, height=btn_size)

    remove_obj.place(x=window_width * (37 / 40) - btn_size, y=window_height * 35 / 60 - btn_size,
                     width=btn_size, height=btn_size)

    simulate.place(x=window_width * (37 / 40) - btn_size, y=window_height * 43 / 60 - btn_size,
                   width=btn_size, height=btn_size)



    window.mainloop()


if __name__ == "__main__":
    animation_playing = True
    transition(None, 0)
