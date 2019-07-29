from kivy.app import App
from kivy.garden.calendar_widget import Calendar


class ExampleCalendar(Calendar):
    pass


class ExampleApp(App):
    def build(self):
        pass


if __name__ == '__main__':
    ExampleApp().run()
