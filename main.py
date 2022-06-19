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
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory, Protocol
import json
from kivy.clock import Clock
from kivy.garden import mapview

""" to use android functions like notifications, flash, battery and sensors >> use plyer module
 audio.file_path = "Music/pristine-609.ogg" # only for android
 asking user to open microphone (example) (make it in final step)
 from android.permissions import request_permissions, Permission
 request_permissions([Permission.RECORD_AUDIO, Permission.NOTIFICATION]) """

# Get the ip address of the computer

# From the ip address, get the hostname
import socket
IP = socket.gethostbyname(socket.gethostname())
Network = ".".join(IP.split('.')[:3]) + '.0'
Router = ".".join(IP.split('.')[:3]) + '.1'
FORMAT = "utf-8"
print("IP Address",IP)
print("Network",Network)
print("Router",Router)

# # GPS module in kivy
# from kivy.garden.gps import GPS, GPSMarker
# from kivy.garden.mapview import MapView, MapMarker, MapSource


class Client(Protocol):
    def __init__(self):
        self.widget = None
        self.host = None
        self.port = None
        self.transport = None
        self.data = b""

    def send_msg(self, order, data):
        msg = json.dumps({"ORDER": order, "DATA": data})
        self.transport.write(msg.encode(FORMAT))

    def connectionMade(self):
        self.widget = self.factory.widget
        self.host = self.factory.host
        self.port = self.factory.port
        print("Connection made")
        self.transport.write(b"Hello World!")
        self.widget.transport = self.transport
        self.widget.stop_waiting_popup()
        self.widget.current = "display_screen"

    def dataReceived(self, data):
        self.data = data
        print("Data received:", data)


class ClientFactory(ReconnectingClientFactory):
    protocol = Client

    def __init__(self, host, port, widget):
        self.widget = widget
        self.host = host
        self.port = port

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


    
class Main_widget(ScreenManager):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        # to access GROUND_STATIONApp class
        self.app = app
        self.data_ids = ["pressure_graph", "temperature_graph", "gas_graph", "velocity_graph", "battery_graph", "altitude_graph"]
        self.data_names = ["Pressure", "Temperature", "Velocity", "Battery", "Altitude"]
        self.data_units = ["hPa", "°C", "m/s", "%", "m"]
        self.transport = None
        self.open_popup = False


    def send_msg(self, order, data):
        msg = json.dumps({"ORDER": order, "DATA": data})
        self.transport.write(msg.encode(FORMAT))

    def check_connection(self):
        self.host = self.ids["ip_address"].text
        self.port = self.ids["port_number"].text
        if not self.host and not self.port:
            self.warning_popup("Please enter valid ip address and port number")
        else:   
            self.port = int(self.port)
            reactor.connectTCP(self.host, self.port, ClientFactory(self.host,self.port,self))
            # self.update_graph(self.data_ids)
            self.start_waiting_popup("Connecting to Ground Station", (0, 0, 0, 0))
            # self.current = "display_screen"

    def scan_for_devices(self):
        pass

    def update_graph(self, data_ids):
        for i in data_ids:
            self.ids[i].add_plot(LinePlot(color=[0, 0, 1, 1], points=[(x, y**0.5) for x, y in zip(range(0, 50), range(0, 50))],line_width=1.5))

    def change_data(self):
        for i in self.data_ids:
            self.ids[i].xmax = self.ids[i].xmax + 5

    # ========== waiting popup.
    def start_waiting_popup(self, *args, title=" ", separator_color=(0, 0, 0, 0)):
        if not self.open_popup:
            self.waiting_popup(title, separator_color)
            self.wait_schedule = Clock.schedule_interval(self.wait_clock, 1)
            self.open_popup = True

    def wait_clock(self, *args):
        widget = self.wait_text
        if widget.text == ". . . ":
            widget.text = ""
        else:
            widget.text += ". "

    def waiting_popup(self, title, separator_color):
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.wait_text = Label(text=". ", color=(0, 0, 1), font_size="34sp")
        box.add_widget(Label(text="", size_hint_y=0.1))
        box.add_widget(Label(text="Please Wait", size_hint_y=0.1, font_size="30sp"))
        box.add_widget(self.wait_text)
        self.popup_wait = Popup(content=box, size_hint=(0.75, 0.3), auto_dismiss=False, title=title,
                                separator_color=separator_color, title_align="center")
        self.popup_wait.background_color = (0, 0, 0.1)
        self.popup_wait.open()

    def stop_waiting_popup(self, *args):
        if self.open_popup:
            self.wait_schedule.cancel()
            self.popup_wait.dismiss()
            self.open_popup = False

    # =========

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
        # audio.start()  # only for android
        pass


class GROUND_STATIONApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_location(self, **kwargs):
        self.lat = kwargs.get('lat')
        self.lon = kwargs.get('lon')


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

