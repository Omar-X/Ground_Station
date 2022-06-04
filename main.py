# ! /usr/bin/env python3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy import Config
from kivy.core.text import LabelBase
from plyer import notification, audio
from kivy.uix.image import Image
from kivy_garden.graph import Graph, LinePlot
# to use android functions like notifications, flash, battery and sensors >> use plyer module
# audio.file_path = "Music/pristine-609.ogg" # only for android
# asking user to open microphone (example) (make it in final step)
# from android.permissions import request_permissions, Permission
# request_permissions([Permission.RECORD_AUDIO, Permission.NOTIFICATION])


class Main_widget(ScreenManager):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        # to access GROUND_STATIONApp class
        self.app = app

        self.graph_1 = Graph(size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5},font_size="12sp",
                             y_ticks_major=2.5, x_ticks_major=10, y_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=0, xmax=100, ymin=-10, ymax=10)
        self.graph_2 = Graph(size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              y_ticks_major=2.5, x_ticks_major=10, y_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-10, ymax=10)
        self.graph_3 = Graph(size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              y_ticks_major=2.5, x_ticks_major=10, y_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-10, ymax=10)
        self.graph_4 = Graph(size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              y_ticks_major=2.5, x_ticks_major=10, y_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-10, ymax=10)
        self.graph_5 = Graph(size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              y_ticks_major=2.5, x_ticks_major=10, y_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-10, ymax=10)
        self.graph_6 = Graph(size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              y_ticks_major=2.5, x_ticks_major=10, y_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-10, ymax=10)

        self.ids.pressure_box.add_widget(self.graph_1)
        self.ids.temperature_box.add_widget(self.graph_2)
        self.ids.gas_box.add_widget(self.graph_3)
        self.ids.velocity_box.add_widget(self.graph_4)
        self.ids.battery_box.add_widget(self.graph_5)
        self.ids.altitude_box.add_widget(self.graph_6)

        self.update_graph([[(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))], [(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))],
                           [(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))], [(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))],
                           [(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))], [(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))]])

    def update_graph(self, data):
        self.graph_1.add_plot(LinePlot(color=[0, 0, 1, 1], points=data[0],line_width=1.5))
        self.graph_2.add_plot(LinePlot(color=[0, 0, 1, 1], points=data[1],line_width=1.5))
        self.graph_3.add_plot(LinePlot(color=[0, 0, 1, 1], points=data[2],line_width=1.5))
        self.graph_4.add_plot(LinePlot(color=[0, 0, 1, 1], points=data[3],line_width=1.5))
        self.graph_5.add_plot(LinePlot(color=[0, 0, 1, 1], points=data[4],line_width=1.5))
        self.graph_6.add_plot(LinePlot(color=[0, 0, 1, 1], points=data[5],line_width=1.5))

    def warning_popup(self, text,title="Warning"):
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        button = Button(text="okay", size_hint_y=0.3,
                        font_size="20sp")
        box.add_widget(Label(text="", size_hint_y=0.1))
        box.add_widget(
            Label(text=text,
                  size_hint_y=0.3,
                  font_size="20sp"))
        box.add_widget(button)
        popup = Popup(title=title, content=box,
                      size_hint=(0.75, 0.35))
        popup.open()
        button.bind(on_release=popup.dismiss)

    def notify(title="Notification", message = "notification message", timeout = 5):
        # notification.notify(title = title, message=message,timeout=timeout,app_icon="Images/icon.png",app_name="NOTIFICATION",ticker = "1")
        # use notification with
        # audio.start()  #only for android
        pass


class GROUND_STATIONApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)    

    def build(self):
        widget = Main_widget(self)
        return widget

if __name__ == "__main__":
    # adding fonts, you can call them using font_name property.
    LabelBase.register('fonts', 'Fonts/ArialUnicodeMS.ttf')
    LabelBase.register("shapes", "Fonts/modernpics.otf")

    # to adjust the app when the keyboard rises
    from kivy.core.window import Window

    Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
    Window.softinput_mode = "below_target"
    # to add a color in the background of the app.
    Window.clearcolor = (169.0 / 255, 172.0 / 255, 175.0 / 255, 0)
    GROUND_STATIONApp().run()

