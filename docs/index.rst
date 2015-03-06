
* import module

* Use as any other widget

```
from kivy.app import App
from KivyCalendar import CalendarWidget

class MyApp(App):
    
    def build(self):
        return CalendarWidget()

MyApp().run()
```

```
from kivy.app import App
from KivyCalendar import DatePicker

class MyApp(App):
    
    def build(self):
        return DatePicker()

MyApp().run()
```
