####################################################################################################################
# IMPORTS
import tkinter as tk

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from win32api import GetSystemMetrics
from MorseConverter import MorseConverter

from PyUtils.TkInter.ZAGThemeTk import ZAGThemeTk


####################################################################################################################
# CORE
class MorseGUI:
    # ---> CONSTANTS
    INPUT_TEXT_PH = "SOS"
    OUTPUT_TEXT_PH = f"Morse Code:\n"
    DARK_THEME = "dark"
    DEFAULT_THEME = "default"

    # ---> ATTRIBUTES
    screen_width = int(GetSystemMetrics(0) / 2)
    screen_height = int(GetSystemMetrics(1) / 2)

    # ---> CONSTRUCTOR
    def __init__(self, morse_converter, frame_border=False):

        self._morse_converter = morse_converter
        self._frame_border_enabled = frame_border
        self._current_theme = self.DEFAULT_THEME

        # ---> MAIN LAYOUT
        # Root Frame, Toolbar, Explorer Panel, Main Panel, Help Panel
        self._init_root()

        # ---> MENU PANEL
        toolbar_panel = self._root.nametowidget("frame_root.frame_toolbar")
        self._init_toolbar_frame(toolbar_panel)

        # ---> LEFT PANEL
        explorer_panel = self._root.nametowidget("frame_root.frame_explorer")
        self._init_explorer_frame(explorer_panel)

        # ---> CORE PANEL
        main_panel = self._root.nametowidget("frame_root.frame_main")
        self._init_main_frame(main_panel)

        # ---> RIGHT PANEL
        help_panel = self._root.nametowidget("frame_root.frame_help")
        self._init_help_frame(help_panel)

        # ---> APPLY CUSTOM STYLES
        self._zag_tk.apply_theme_recurs(self._root, self._current_theme)

    # ---> FUNCTIONS
    def run_mainloop(self):
        self._root.mainloop()

    def _load_icons(self):
        icon_image = Image.open("res/icons/play.png")
        icon_image = icon_image.resize((25, 25))
        self._icon_play = ImageTk.PhotoImage(icon_image)
        icon_image.close()

        icon_image = Image.open("res/icons/recycle_bin.png")
        icon_image = icon_image.resize((25, 25))
        self._icon_recycle_bin = ImageTk.PhotoImage(icon_image)
        icon_image.close()

        icon_image = Image.open("res/icons/save.png")
        icon_image = icon_image.resize((25, 25))
        self._icon_save = ImageTk.PhotoImage(icon_image)
        icon_image.close()

    def _set_border(self, frame):
        if self._frame_border_enabled:
            frame.configure(borderwidth=2, relief="groove")

    def _switch_theme(self, *args):
        # Selected by String Var of menubutton
        self._current_theme = self._selected_theme.get()

        self._zag_tk.apply_theme_recurs(self._root, self._current_theme)

    def _on_click_ph_input(self, event):
        widget = event.widget
        current_text = widget.get("1.0", "end-1c")

        if current_text.strip() == self.INPUT_TEXT_PH:
            widget.delete("1.0", 'end')

    def _on_leave_ph_input(self, event):
        widget = event.widget
        current_text = widget.get("1.0", "end-1c")

        if not current_text.strip():
            widget.delete("1.0", 'end')
            widget.insert("1.0", self.INPUT_TEXT_PH)

        self._root.focus()

    @staticmethod
    def _update_scrollbar_visibility(scrollbar_widget, text_widget, event=None):
        # event is mandatory because this is also a callback method
        if event:  # Avoid warning
            pass

        if text_widget.yview()[0] == 0:
            scrollbar_widget.grid_forget()
        else:
            scrollbar_widget.grid(row=0, column=1, sticky="ns")
            text_widget.config(yscrollcommand=scrollbar_widget.set)

    def _convert_text(self):
        input_text = self._root.nametowidget("frame_root.frame_main.txt_input").get("1.0", 'end')
        converted_text = self.OUTPUT_TEXT_PH + self._morse_converter.string_to_morse(input_text)

        output_text = self._root.nametowidget("frame_root.frame_main.txt_output")
        output_text.configure(state="normal")
        output_text.delete("1.0", 'end')

        output_text.insert("1.0", converted_text)
        output_text.configure(state="disabled")

        return converted_text

    def _play_morse(self):
        output_text = self._root.nametowidget("frame_root.frame_main.txt_output").get("1.0", "end-1c")
        output_text = output_text.replace(self.OUTPUT_TEXT_PH, " ")
        self._morse_converter.morse_process(output_text, True, False, False)

    def _process_morse(self):
        output_text = self._root.nametowidget("frame_root.frame_main.txt_output").get("1.0", "end-1c")
        output_text = output_text.replace(self.OUTPUT_TEXT_PH, " ")

        popup = tk.Toplevel(self._root)
        popup.title("Select options")

        popup_frame = ttk.Frame(popup)
        popup_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        popup_label = ttk.Label(popup_frame, text="Select operations:")
        popup_label.grid(row=0, column=0, padx=30, pady=10, sticky="ew")

        play_sound_var = tk.IntVar()
        print_plot_var = tk.IntVar()
        export_file_var = tk.IntVar()

        play_sound_var.set(False)
        print_plot_var.set(True)
        export_file_var.set(True)

        play_sound_cb = ttk.Checkbutton(popup_frame, text="Play Sound", variable=play_sound_var)
        play_sound_cb.grid(row=1, column=0, padx=30, pady=5, sticky="ew")

        print_plot_cb = ttk.Checkbutton(popup_frame, text="Print sound plot", variable=print_plot_var)
        print_plot_cb.grid(row=2, column=0, padx=30, pady=5, sticky="ew")

        export_file_cb = ttk.Checkbutton(popup_frame, text="Export File", variable=export_file_var)
        export_file_cb.grid(row=3, column=0, padx=30, pady=5, sticky="ew")

        def get_selections():
            play_sound = False
            print_plot = False
            export_file = False

            if play_sound_var.get():
                play_sound = True
            if print_plot_var.get():
                print_plot = True
            if export_file_var.get():
                export_file = True

            if play_sound or print_plot or export_file:
                self._morse_converter.morse_process(output_text, play_sound, print_plot, export_file)
            else:
                messagebox.showerror("Error", "Choice one at least")

        execute_btn = ttk.Button(popup_frame, text="Execute", command=get_selections)
        execute_btn.grid(row=4, column=0, padx=30, pady=10, sticky="ew")

        zag_tk = ZAGThemeTk()
        zag_tk.apply_theme_recurs(popup, self._current_theme)

    def _clean_input(self):
        input_text = self._root.nametowidget("frame_root.frame_main.txt_input")
        input_text.configure(state="normal")
        input_text.delete("1.0", 'end')
        input_text.insert("1.0", self.INPUT_TEXT_PH)

        output_text = self._root.nametowidget("frame_root.frame_main.txt_output")
        output_text.configure(state="normal")
        output_text.delete("1.0", 'end')
        # ---> Default input ph conversion
        self._convert_text()
        output_text.configure(state="disabled")

    def _init_root(self):
        self._root = tk.Tk()
        self._root.title("Py Morse!")
        self._root.state("zoomed")

        # Icons must have an instance attribute to avoid that garbage collector delete them
        self._load_icons()

        # Theme uses styles, so it need to be called after root instantiation
        self._zag_tk = ZAGThemeTk()

        """
        root_frame = ttk.Frame(self._root, name="frame_root")
        root_frame.pack(padx=20, pady=20)

        toolbar_frame = ttk.Frame(root_frame, name="frame_toolbar")
        toolbar_frame.grid(row=0, column=0, padx=5, pady=5)

        explorer_frame = ttk.Frame(root_frame, name="frame_explorer")
        explorer_frame.grid(row=1, column=0, padx=5, pady=5)

        main_frame = ttk.Frame(root_frame, name="frame_main")
        main_frame.grid(row=1, column=1, padx=5, pady=5)

        help_frame = ttk.Frame(root_frame, name="frame_help")
        help_frame.grid(row=1, column=2, padx=5, pady=5)
        """

        root_frame = ttk.Frame(self._root, name="frame_root")
        root_frame.pack(fill="both", padx=20, pady=20)

        toolbar_frame = ttk.Frame(root_frame, name="frame_toolbar")
        toolbar_frame.pack(side="top", fill="x", padx=5, pady=5)

        explorer_frame = ttk.Frame(root_frame, name="frame_explorer")
        explorer_frame.pack(side="left", fill="both", padx=5, pady=5)

        main_frame = ttk.Frame(root_frame, name="frame_main")
        main_frame.pack(side="left", fill="both", padx=5, pady=5, expand=True)

        help_frame = ttk.Frame(root_frame, name="frame_help")
        help_frame.pack(side="left", fill="y", padx=5, pady=5, expand=True)

        self._set_border(root_frame)
        self._set_border(toolbar_frame)
        self._set_border(explorer_frame)
        self._set_border(main_frame)
        self._set_border(help_frame)

    def _init_toolbar_frame(self, parent):

        # Welcome Label
        welcome_label = ttk.Label(parent, text="Hello There!", anchor=tk.CENTER)
        welcome_label.pack(side="left", fill=tk.BOTH, expand=True)

        # ---> Theme
        menu_btn = ttk.Menubutton(parent, text="Select Theme")
        menu_btn.pack(side="right")

        themes = self._zag_tk.get_loaded_themes()

        # Set var which will trace the selected item menu
        self._selected_theme = tk.StringVar()
        self._selected_theme.set(self._current_theme)
        self._selected_theme.trace("w", self._switch_theme)

        menu_themes = tk.Menu(menu_btn, tearoff=0)
        for theme in themes:
            menu_themes.add(label=theme,
                            variable=self._selected_theme,
                            itemType=tk.RADIOBUTTON)
        menu_btn["menu"] = menu_themes

    def _init_explorer_frame(self, parent):
        pass

    def _init_main_frame(self, parent):
        txt_width = 90
        txt_height = 15

        # ---> Input Text
        input_txt = tk.Text(parent, name="txt_input")
        input_txt.grid(row=0, column=0, padx=5, pady=5)
        input_txt.configure(height=txt_height, width=txt_width)
        input_txt.insert("1.0", self.INPUT_TEXT_PH)

        input_scroll = ttk.Scrollbar(parent, command=input_txt.yview)
        input_txt.config(yscrollcommand=input_scroll.set)

        input_txt.bind("<Button-1>", self._on_click_ph_input)
        input_txt.bind("<Leave>", self._on_leave_ph_input)
        input_txt.bind("<KeyRelease>",
                       lambda event: self._update_scrollbar_visibility(input_scroll, input_txt, event))

        # ---> Output Text
        output_txt = tk.Text(parent, name="txt_output")
        output_txt.configure(height=txt_height, width=txt_width, state="disabled")
        output_txt.grid(row=1, column=0, padx=5, pady=5)

        output_scroll = ttk.Scrollbar(parent, command=output_txt.yview)
        output_txt.config(yscrollcommand=output_scroll.set)

        output_scroll.bind("<KeyRelease>",
                           lambda event: self._update_scrollbar_visibility(output_scroll, output_txt, event))

        # ---> Command Frame
        command_frame = ttk.Frame(parent, name="frame_command")
        command_frame.grid(row=2, column=0)
        self._set_border(command_frame)

        # ---> Button Convert
        convert_btn = ttk.Button(command_frame,
                                 name="btn_convert", text="Convert!",
                                 command=self._convert_text, width=35)
        convert_btn.grid(row=2, column=0, padx=5, pady=5)

        # ---> Button Play Morse
        play_morse_btn = ttk.Button(command_frame, name="btn_play_morse", text="Play Morse!",
                                    command=self._play_morse, image=self._icon_play)
        play_morse_btn.grid(row=2, column=1, padx=5, pady=5)

        # ---> Button Process Morse
        export_morse_btn = ttk.Button(command_frame, name="btn_process_morse", text="Process Morse!",
                                      command=self._process_morse, image=self._icon_save)
        export_morse_btn.grid(row=2, column=2, padx=5, pady=5)

        # ---> Button Clean
        clean_btn = ttk.Button(command_frame, name="btn_clean", text="Clean",
                               command=self._clean_input, image=self._icon_recycle_bin)
        clean_btn.grid(row=2, column=3, padx=5, pady=5)

        # ---> Default input ph conversion
        self._convert_text()

    def _init_help_frame(self, parent):
        ddic_str_to_morse = self._morse_converter.get_ddic_str_to_morse()
        txt_height = 30

        # ---> Chars
        chars_text = tk.Text(parent, width=20, height=txt_height)
        chars_text.grid(row=0, column=0, sticky="ns", pady=5)
        tmp_ddic = " CHARS\n\n"
        for key, value in ddic_str_to_morse['chars'].items():
            tmp_ddic += ' ' + key + ":\t" + value + '\n'
        chars_text.insert("1.0", tmp_ddic)
        chars_text.configure(state="disabled")

        # ---> Digits / Punt. Marks
        digits_pmarks_text = tk.Text(parent, width=20, height=txt_height)
        digits_pmarks_text.grid(row=0, column=1, sticky="ns", pady=5)
        tmp_ddic = " DIGITS\n\n"
        for key, value in ddic_str_to_morse['digits'].items():
            tmp_ddic += ' ' + key + ":\t" + value + '\n'
        tmp_ddic += "\n\n\n PUNT. MARK\n\n"
        for key, value in ddic_str_to_morse['punctuation_marks'].items():
            tmp_ddic += ' ' + key + ":\t" + value + '\n'
        digits_pmarks_text.insert("1.0", tmp_ddic)
        digits_pmarks_text.configure(state="disabled")

        # ---> Special Conventions
        specials_text = tk.Text(parent, width=25, height=txt_height)
        specials_text.grid(row=0, column=2, sticky="ns", pady=5)
        tmp_ddic = " SPECIAL CONVENTIONS\n\n"

        specials_text.insert("1.0", tmp_ddic)
        specials_text.configure(state="disabled")


if __name__ == "__main__":
    mc = MorseConverter()
    gui = MorseGUI(mc, False)
    gui.run_mainloop()
