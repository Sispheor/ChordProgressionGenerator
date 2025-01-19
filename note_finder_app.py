import asyncio

import flet as ft

from note_detector import NoteDetector
from statics import NOTES_SHARP


class Chronometer(ft.Text):
    def __init__(self):
        super().__init__()
        self.seconds = 0
        self.visible = False
        self.running = False

    def start(self):
        self.seconds = 0
        self.running = True
        self.visible = True
        self.page.run_task(self.update_timer)

    def stop(self):
        self.running = False

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.running:
            mins, secs = divmod(self.seconds, 60)
            self.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds += 1

class NoteFinderApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.note_detector = None
        self.chronometer = Chronometer()
        self.note_detector = NoteDetector()
        self.list_note_to_find = list()
        self.current_note_to_find = None
        self.instruction_text = ft.Text(value="Press start button", color="blue")
        self.note_to_find_text = ft.Text(value="", color="black", visible=False)
        self.current_to_find_text = ft.Text(value="", color="black", visible=False)
        self.start_button = ft.ElevatedButton("Start", on_click=self.start_new_series_clicked)
        self.stop_button = ft.ElevatedButton("Stop", on_click=self.stop_current_series_clicked, visible=False)
        self.controls = [self.instruction_text, self.start_button, self.stop_button, self.chronometer, self.note_detector, self.note_to_find_text,
                         self.current_to_find_text]

    def stop_current_series_clicked(self, e):
        self.chronometer.stop()
        self.note_detector.stop()
        self.instruction_text.value = "Press start button"
        self.start_button.visible = True
        self.stop_button.visible = False
        self.note_detector.visible= False
        self.note_to_find_text.visible= False
        self.current_to_find_text.visible= False
        self.page.update()

    def callback_note_found(self):
        if len(self.list_note_to_find) > 0:
            self.current_note_to_find = self.list_note_to_find.pop(0)
            self.note_detector.current_note_to_find = self.current_note_to_find
            self.page.update()
        else:
            # we stop the current series
            self.chronometer.stop()

    def start_new_series_clicked(self, e):
        self.chronometer.start()
        self.start_button.visible = False
        self.stop_button.visible = True
        self.instruction_text.value = "Complete the series or clik stop"
        # TODO random
        self.list_note_to_find = NOTES_SHARP
        self.current_note_to_find = self.list_note_to_find.pop(0)
        self.note_to_find_text.visible = True
        self.note_to_find_text.value = str(self.list_note_to_find)
        self.current_to_find_text.visible = True
        self.current_to_find_text.value = f"Current note: {self.current_note_to_find}"
        # start audio record
        self.note_detector.visible = True
        self.note_detector.start(current_note_to_find=self.current_note_to_find, callback_note_found=self.callback_note_found)
        # loop show notes
        self.page.update()

def main(page: ft.Page):
    page.title = "Note finder"
    page.horizontal_alignment  = ft.CrossAxisAlignment.CENTER
    page.add(NoteFinderApp())

ft.app(main)