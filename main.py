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
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from kivy.support import install_twisted_reactor
from kivy.clock import Clock
# to use android functions like notifications, flash, battery and sensors >> use plyer module
# audio.file_path = "Music/pristine-609.ogg" # only for android
# asking user to open microphone (example) (make it in final step)
# from android.permissions import request_permissions, Permission
# request_permissions([Permission.RECORD_AUDIO, Permission.NOTIFICATION])

install_twisted_reactor()
# Get the ip address of the computer
import socket
ip = socket.gethostbyname(socket.gethostname())


class Client(DatagramProtocol):
    def __init__(self, host, port,widget):
        self.widget = widget
        self.host = host
        self.port = port
        self.transport = None
        self.data = b""
    
    def startProtocol(self):
        self.transport.connect(self.host, self.port)
        self.transport.write(b"Hello World!")
        
    def datagramReceived(self, data, host):
        print("Datagram received: ", data)
        self.data = data

    
class Main_widget(ScreenManager):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        # to access GROUND_STATIONApp class
        self.app = app
        self.data_ids = ["pressure_graph", "temperature_graph", "gas_graph", "velocity_graph", "battery_graph", "altitude_graph"]
        self.data_names = ["Pressure", "Temperature", "Gas", "Velocity", "Battery", "Altitude"]
        self.data_units = ["hPa", "°C", "ppm", "m/s", "%", "m"]
        self.transport = None

    def check_connection(self):
        self.host = self.ids["ip_address"].text
        self.port = int(self.ids["port_number"].text)
        reactor.connectTCP(self.host, self.port, Client(self.host, self.port, self))
        self.update_graph(self.data_ids)

    def update_graph(self, data_ids):
        for i in data_ids:
            self.ids[i].add_plot(LinePlot(color=[0, 0, 1, 1], points=[(x, y**0.5) for x, y in zip(range(0, 100), range(0, 100))],line_width=1.5))

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

