from __future__ import annotations as _annotation
import tkinter as _tk
from tkinter import ttk as _ttk
import subprocess as _subprocess
import time as _time
import threading as _threading
from typing import Union as _Union

_LARGEFONT = ("Verdana", 35)
_MEDIUMFONT = ("Verdana", 20)
_SMALLFONT = ("Verdana", 12)

_PADDING20 = (20, 20, 20, 20)


class IHSRunner(_tk.Tk):
    """Instantiate and run a runner window.

    Args:
        bot: (BotController): An instance of the `BotController` object.
        light_port (int): Port number of the light sensor.
        reset_file_path (str): File path of the 'reset' program. Leave as empty string if not applicable.
    """
    def __init__(self, bot: _BotController, light_port: int, reset_file_path: str):
        _tk.Tk.__init__(self)

        self._k = bot.k

        self._light_port = light_port
        self._reset_file_path = reset_file_path

        self._finished_calibration = False
        self._calibrated_light_thresh = 1000

        _ttk.Style().configure("Small.TButton", font=_SMALLFONT)

        container = _tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._frames = {}

        for F in (_StartPage, _ResetPage, _RunPage):

            frame = F(container, self)

            self._frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self._show_frame(_StartPage)
        self.mainloop()

    def _stop_updating_sensor_values(self):
        self._finished_calibration = True

    def _set_calibrated_light_thresh(self, new_value: int):
        self._calibrated_light_thresh = new_value

    def _show_frame(self, page: _Union[type[_StartPage], type[_ResetPage], type[_RunPage]]):
        frame = self._frames[page]
        frame.tkraise()


class _StartPage(_tk.Frame):
    def __init__(self, parent: _tk.Frame, controller: IHSRunner):
        _tk.Frame.__init__(self, parent)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        title_label = _ttk.Label(
            self,
            text="Welcome to IHS Runner.\n#define your future",
            font=_LARGEFONT,
            anchor="center",
        )
        title_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        info_label = _ttk.Label(
            self,
            text= f"light port: {controller._light_port}\nreset proram: {controller._reset_file_path}",
            font=_SMALLFONT,
        )
        info_label.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        buttons_label = _ttk.Label(
            self, text="Please make a decidion: ", font=_MEDIUMFONT, anchor="center"
        )
        buttons_label.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        
        def quit() -> None:
            controller._stop_updating_sensor_values()
            print("quit")
            self.master.quit()
            exit()
        
        quit_button = _ttk.Button(
            self,
            text="Quit",
            command= quit,
            padding=_PADDING20,
            style="Small.TButton",
        )
        quit_button.grid(row=3, column=0, padx=10, pady=10)

        reset_button = _ttk.Button(
            self,
            text="Run Reset",
            command=lambda: controller._show_frame(_ResetPage),
            padding=_PADDING20,
            style="Small.TButton",
        )
        reset_button.grid(row=3, column=1, padx=10, pady=10)

        start_button = _ttk.Button(
            self,
            text="Start",
            command=lambda: controller._show_frame(_RunPage),
            padding=_PADDING20,
            style="Small.TButton",
        )
        start_button.grid(row=3, column=2, padx=10, pady=10)


class _ResetPage(_tk.Frame):
    def __init__(self, parent: _tk.Frame, controller: IHSRunner):

        _tk.Frame.__init__(self, parent)

        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        info_label = _ttk.Label(
            self,
            text=f"command: python3 {controller._reset_file_path}",
            font=_SMALLFONT,
        )
        info_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        output_box = _tk.Text(self, height=10, font=_SMALLFONT)
        output_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)

        def run_reset():
            result = _subprocess.run(
                ["python3", controller._reset_file_path], capture_output=True, text=True
            )
            output_box.delete(1.0, _tk.END)
            output_box.insert(_tk.END, result.stdout)
            output_box.insert(_tk.END, result.stderr)

        back_button = _ttk.Button(
            self,
            text="Back",
            command=lambda: controller._show_frame(_StartPage),
            style="Small.TButton",
            padding=_PADDING20,
        )
        back_button.grid(row=2, column=0, padx=10, pady=10)

        reset_button = _ttk.Button(
            self,
            text="Run Reset",
            command=run_reset,
            style="Small.TButton",
            padding=_PADDING20,
        )
        reset_button.grid(row=2, column=1, padx=10, pady=10)


class _RunPage(_tk.Frame):
    def __init__(self, parent: _tk.Frame, controller: IHSRunner):
        _tk.Frame.__init__(self, parent)

        self._controller = controller

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        info_label = _ttk.Label(
            self,
            text=f"Calibrate for light sensor on port {self._controller._light_port}",
            font=_MEDIUMFONT,
        )
        info_label.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        off_value_text_label = _ttk.Label(
            self, text="light off value: ", font=_MEDIUMFONT
        )
        off_value_text_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        on_value_text_label = _ttk.Label(
            self, text="light on value: ", font=_MEDIUMFONT
        )
        on_value_text_label.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        sensor_value_text_label = _ttk.Label(
            self, text="current sensor value: ", font=_MEDIUMFONT
        )
        sensor_value_text_label.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self._light_on_value = _tk.StringVar()
        self._light_off_value = _tk.StringVar()

        self._live_sensor_value = _tk.StringVar()

        self._ready_string = _tk.StringVar()
        self._ready_string.set("calibrate light values")

        update_thread = _threading.Thread(target=self.update_sensor_value)
        update_thread.daemon = True
        update_thread.start()

        sensor_value_label = _ttk.Label(
            self, textvariable=self._live_sensor_value, font=_MEDIUMFONT
        )
        sensor_value_label.grid(row=3, column=3, padx=10, pady=10)

        light_off_value_label = _ttk.Label(
            self, textvariable=self._light_off_value, font=_MEDIUMFONT
        )
        light_off_value_label.grid(row=1, column=3, padx=10, pady=10)

        light_on_value_label = _ttk.Label(
            self, textvariable=self._light_on_value, font=_MEDIUMFONT
        )
        light_on_value_label.grid(row=2, column=3, padx=10, pady=10)

        back_button = _ttk.Button(
            self,
            text="Back",
            command=lambda: controller._show_frame(_StartPage),
            style="Small.TButton",
            padding=_PADDING20,
        )
        back_button.grid(row=4, column=0, padx=10, pady=10)

        light_off_button = _ttk.Button(
            self,
            text="Set Light Off Value",
            command=self.set_light_off_value,
            style="Small.TButton",
            padding=_PADDING20,
        )
        light_off_button.grid(row=4, column=1, padx=10, pady=10)

        light_on_button = _ttk.Button(
            self,
            text="Set Light On Value",
            style="Small.TButton",
            padding=_PADDING20,
            command=self.set_light_on_value,
        )
        light_on_button.grid(row=4, column=2, padx=10, pady=10)

        start_button = _ttk.Button(
            self,
            text="Start",
            style="Small.TButton",
            padding=_PADDING20,
            command=lambda: self.finish_calibration(update_thread),
        )
        start_button.grid(row=4, column=3, padx=10, pady=10)

        def skip() -> None:
            controller._stop_updating_sensor_values()
            self.master.quit() 

        skip_button = _ttk.Button(
            self,
            text="Skip Light",
            style="Small.TButton",
            padding=_PADDING20,
            command= skip
        )
        skip_button.grid(row=5, column=0, padx=10, pady=10)

        ready_label = _ttk.Label(self, textvariable=self._ready_string, font=_MEDIUMFONT)
        ready_label.grid(row=5, column=1, padx=10, pady=10, columnspan=3)

    def finish_calibration(self, thread: _threading.Thread):
        if self._light_off_value.get() == "" or self._light_on_value.get() == "":
            self._ready_string.set("light calibration incomplete.")
            return

        self._controller._set_calibrated_light_thresh(
            int(
                int(self._light_on_value.get()) * 0.8
                + int(self._light_off_value.get()) * 0.2
            )
        )
        self._ready_string.set(
            f"waiting for light: {self._controller._calibrated_light_thresh}"
        )

        wait_for_light_thread = _threading.Thread(
            target=self.wait_for_light, args=(thread,)
        )
        wait_for_light_thread.daemon = True
        wait_for_light_thread.start()

    def update_sensor_value(self):
        _light_port = self._controller._light_port
        while not self._controller._finished_calibration:
            self._live_sensor_value.set(self._controller._k.analog(_light_port))
            _time.sleep(0.1)

    def wait_for_light(self, thread: _threading.Thread):
        _light_port = self._controller._light_port
        while (
            self._controller._k.analog(_light_port)
            > self._controller._calibrated_light_thresh
        ):
            continue

        print("light")
        start_time = _time.time()

        self.master.quit()
        self._controller._stop_updating_sensor_values()
        thread.join()
        print("reaction time:", _time.time() - start_time)

    def set_light_off_value(self):
        self._light_off_value.set(self._live_sensor_value.get())

    def set_light_on_value(self):
        self._light_on_value.set(self._live_sensor_value.get())


from .bot import BotController as _BotController
