# KivyCalendar

KivyCalendar is module with additional widgets for [Kivy](http://kivy.org/): CalendarWidget and DatePicker. 

**CalendarWidget** based on RelativeLayout. It allow to switch months by buttons in left-top and right-top widget's corners. 

![CalendarWidget](https://lh5.googleusercontent.com/-jX3AJQrONFY/VPkMU9cQ6zI/AAAAAAAAAtU/tfkGrXZRvIg/s1600/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-My-1.png)

**DatePicker** based on TextInput. When textinput field focused shows popup with CalendarWidget. Once data selected popup dismiss and selected date puts into textinput field. 

```
pip install KivyCalendar
```

Oleg Kozlov (xxblx)

2015


# July 19 - improvements (fherbine)

KivyCalendar with improved CalendarWidget.

Félix Herbinet (fherbine)

2019

## New design

We can set `foreground_color` and `background_color`.
- `foreground_color`: Basically fonts color.
- `background_color`: Background color.

## Active date is now a property:

`active_date` is now considered as a property to be dispatch correctly.

## New Screenmanager animation:

`left` / `right` Screenmanager's animation are now reversed.

## Better compatibility with Python3:

- Uses of .format() methods.
- PEP8 Compatible

## Todos:

- PEP257
- Improvements on DatePicker
