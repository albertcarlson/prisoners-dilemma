
import tkinter
import tkinter.messagebox
import customtkinter
import time
import random

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Prisoner's Dilemma Simulation")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Latest Leaderboard", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # the stuff on the right
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Settings")
        self.scrollable_frame.grid(row=0, column=2, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        
        # choose starting population for each species
        STARTING_POPULATION = 10  # TODO FIXME get directly from config.ini
        self.starting_pop_label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Starting populatio = {STARTING_POPULATION}")
        self.starting_pop_label.grid(row=0, column=0, padx=10, pady=(0, 20))
        self.starting_pop = customtkinter.CTkSlider(self.scrollable_frame, from_=0, to=25, number_of_steps=25, command=self.starting_pop_slider)
        self.starting_pop.set(STARTING_POPULATION)
        self.starting_pop.grid(row=1, column=0, padx=10, pady=(0, 20))

        # choose number of rounds
        STARTING_AVG = 100  # TODO FIXME get directly from config.ini
        self.rounds_label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Number of rounds, μ = {STARTING_AVG}")
        self.rounds_label.grid(row=2, column=0, padx=10, pady=(0, 20))
        self.rounds = customtkinter.CTkSlider(self.scrollable_frame, from_=50, to=200, number_of_steps=150, command=self.num_rounds_slider)
        self.rounds.set(STARTING_AVG)
        self.rounds.grid(row=3, column=0, padx=10, pady=(0, 20))

        # choose number of rounds stddev
        STARTING_STDDEV = 0  # TODO FIXME get directly from config.ini
        self.rounds_stddev_label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Number of rounds, σ = {STARTING_STDDEV}")
        self.rounds_stddev_label.grid(row=4, column=0, padx=10, pady=(0, 20))
        self.rounds_stddev = customtkinter.CTkSlider(self.scrollable_frame, from_=0, to=50, number_of_steps=50, command=self.num_rounds_stddev_slider)
        self.rounds_stddev.set(STARTING_STDDEV)
        self.rounds_stddev.grid(row=5, column=0, padx=10, pady=(0, 20))

        # switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch 1")
        # switch.grid(row=3, column=0, padx=10, pady=(0, 20))
        # self.scrollable_frame_switches.append(switch)


        # # create checkbox and switch frame
        # self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        # self.checkbox_slider_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.checkbox_1.select()
        
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


    def sidebar_button_event(self):
        print("sidebar_button click")

    def starting_pop_slider(self, value):
        value = int(value)
        self.starting_pop_label.configure(text=f"Starting population = {value}")

    def num_rounds_slider(self, value):
        value = int(value)
        self.rounds_label.configure(text=f"Number of rounds, μ = {value}")

    def num_rounds_stddev_slider(self, value):
        value = int(value)
        self.rounds_stddev_label.configure(text=f"Number of rounds, σ = {value}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
    
