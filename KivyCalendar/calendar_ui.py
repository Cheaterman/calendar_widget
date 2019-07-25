'''
Date Picker - Kivy Calendar
====

Calendar & Date Picker for Kivy based on KivyCalendar made by Oleg Kozlov
This Calendar include a new UI, and properties handlers:

- foreground_color: ListProperty to change the color of the text.
- background_color: ListProperty to change the color of the background.

- event_date: Getting the selected date.
    based on Oleg's one it add an event dispatcher.

'''

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ReferenceListProperty,
)
from kivy.uix.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import (
    Screen,
    ScreenManager,
)
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButtonBehavior

from KivyCalendar import calendar_data as cal_data


Builder.load_string("""
<CalendarWidget>:
    background_color: 0, 0, 0, 1

    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size

<ArrowButton>:
    font_size: sp(21)
    color: 1, 1, 1, 1
    size_hint: .1, .1

    canvas.before:
        Color:
            rgba: rgba('#ffffff44') if self.state == 'down' else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size

<MonthYearLabel>:
    bold: True
    halign: "center"
    pos_hint: {"top": 1, "center_x": .5}
    size_hint: None, 0.1

<MonthsManager>:
    pos_hint: {"top": .9}
    size_hint: 1, .9

<ButtonsGrid>:
    cols: 7
    rows: 7
    size_hint: 1, 1
    pos_hint: {"top": 1}

<DayAbbrLabel>:
    bold: True
    text_size: self.size[0], None
    halign: "center"

<DayAbbrWeekendLabel>:
    # Useful to set a specific UI to week abbreviation labels

<DayButton>:
    group: "day_num"

    canvas.before:
        Color:
            rgba: self.color[:3] + [.4 if self.state == 'down' else 0]
        Rectangle:
            size: self.size
            pos: self.pos

<DayNumButton>:
    # Useful to set a specific UI to regular Day buttons

<DayNumWeekendButton>:
    # Useful to set a specific UI to week ends' Day buttons

""")


class DatePicker(TextInput):
    """
    Date picker is a textinput, if it focused shows popup with calendar
    which allows you to define the popup dimensions using pHint_x, pHint_y,
    and the pHint lists, for example in kv:
    DatePicker:
        pHint: 0.7,0.4
    would result in a size_hint of 0.7,0.4 being used to create the popup
    """
    pHint_x = NumericProperty(0.0)
    pHint_y = NumericProperty(0.0)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, touch_switch=False, *args, **kwargs):
        super(DatePicker, self).__init__(*args, **kwargs)

        self.touch_switch = touch_switch
        self.init_ui()

    def init_ui(self):

        self.text = cal_data.today_date()
        # Calendar
        self.cal = CalendarWidget(as_popup=True,
                                  touch_switch=self.touch_switch)
        # Popup
        self.popup = Popup(content=self.cal, on_dismiss=self.update_value,
                           title="")
        self.cal.parent_popup = self.popup

        self.bind(focus=self.show_popup)

    def show_popup(self, isnt, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint = self.pHint
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            self.popup.open()

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False


class CalendarWidget(RelativeLayout):
    """ Basic calendar widget """

    # logic
    active_date = ListProperty()

    # design
    background_color = ListProperty([0, 0, 0, 1])
    foreground_color = ListProperty([1, 1, 1, 1])

    def __init__(self, as_popup=False, touch_switch=False, *args, **kwargs):
        super(CalendarWidget, self).__init__(*args, **kwargs)

        self.as_popup = as_popup
        self.touch_switch = touch_switch
        self.prepare_data()
        self.init_ui()

    def init_ui(self):

        self.left_arrow = ArrowButton(
            text="<", on_press=self.go_prev,
            pos_hint={"top": 1, "left": 0},
        )
        self.bind(foreground_color=self.left_arrow.setter('color'))

        self.right_arrow = ArrowButton(
            text=">", on_press=self.go_next,
            pos_hint={"top": 1, "right": 1},
        )
        self.bind(foreground_color=self.right_arrow.setter('color'))

        self.add_widget(self.left_arrow)
        self.add_widget(self.right_arrow)

        # Title
        self.title_label = MonthYearLabel(
            text=self.title,
        )
        self.bind(foreground_color=self.title_label.setter('color'))
        self.add_widget(self.title_label)

        # ScreenManager
        self.screenmanager = MonthsManager()
        self.add_widget(self.screenmanager)

        self.create_month_screen(self.quarter[1], toogle_today=True)

    def create_month_screen(self, month, toogle_today=False):
        """ Screen with calendar for one month """

        screen = Screen()
        months = self.month_names_eng[self.active_date[1] - 1]
        screen.name = "{month}-{year}".format(
            month=months,
            year=self.active_date[2],
        )  # like march-2015

        # Grid for days
        grid_layout = ButtonsGrid()
        screen.add_widget(grid_layout)

        # Days abbrs
        for i in range(7):
            if i >= 5:  # weekends
                day_label = DayAbbrWeekendLabel(text=self.days_abrs[i])
            else:  # work days
                day_label = DayAbbrLabel(text=self.days_abrs[i])

            day_label.color = self.foreground_color
            self.bind(foreground_color=day_label.setter('color'))

            grid_layout.add_widget(day_label)

        # Buttons with days numbers
        for week in month:
            for day in week:
                if day[1] >= 5:  # weekends
                    day_button = DayNumWeekendButton(text=str(day[0]))
                else:  # work days
                    day_button = DayNumButton(text=str(day[0]))

                day_button.bind(on_press=self.get_btn_value)
                day_button.color = self.foreground_color

                if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        day_button.state = "down"
                # Disable + red colored buttons with days from other months
                if day[2] == 0:
                    day_button.disabled = True
                    day_button.color = 1, 0, 0, 1
                else:
                    self.bind(foreground_color=day_button.setter('color'))

                grid_layout.add_widget(day_button)

        self.screenmanager.add_widget(screen)

    def prepare_data(self):
        """ Prepare data for showing on widget loading """

        # Get days abbrs and month names lists
        self.month_names = cal_data.get_month_names()
        self.month_names_eng = cal_data.get_month_names_eng()
        self.days_abrs = cal_data.get_days_abbrs()

        # Today date
        self.active_date = cal_data.today_date_list()
        # Set title
        self.title = "{month} {year}".format(
            month=self.month_names[self.active_date[1] - 1],
            year=self.active_date[2],
        )

        # Quarter where current month in the self.quarter[1]
        self.get_quarter()

    def get_quarter(self):
        """ Get caledar and months/years nums for quarter """

        self.quarter_nums = cal_data.calc_quarter(self.active_date[2],
                                                  self.active_date[1])
        self.quarter = cal_data.get_quarter(self.active_date[2],
                                            self.active_date[1])

    def get_btn_value(self, inst):
        """ Get day value from pressed button """

        self.active_date[0] = int(inst.text)
        self.property('active_date').dispatch(self)

        if self.as_popup:
            self.parent_popup.dismiss()

    def go_prev(self, inst):
        """ Go to screen with previous month """

        # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[0][1],
                            self.quarter_nums[0][0]]

        # Name of prev screen
        n = self.quarter_nums[0][1] - 1
        prev_scr_name = "{month}-{year}".format(
            month=self.month_names_eng[n],
            year=self.quarter_nums[0][0],
        )

        # If it's doen't exitst, create it
        if not self.screenmanager.has_screen(prev_scr_name):
            self.create_month_screen(self.quarter[0])

        self.screenmanager.current = prev_scr_name
        self.screenmanager.transition.direction = "right"

        self.get_quarter()
        self.title = "{month} {year}".format(
            month=self.month_names[self.active_date[1] - 1],
            year=self.active_date[2],
        )

        self.title_label.text = self.title

    def go_next(self, inst):
        """ Go to screen with next month """

        # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[2][1],
                            self.quarter_nums[2][0]]

        # Name of prev screen
        n = self.quarter_nums[2][1] - 1
        next_scr_name = "{month}-{year}".format(
            month=self.month_names_eng[n],
            year=self.quarter_nums[2][0],
        )

        # If it's doen't exitst, create it
        if not self.screenmanager.has_screen(next_scr_name):
            self.create_month_screen(self.quarter[2])

        self.screenmanager.current = next_scr_name
        self.screenmanager.transition.direction = "left"

        self.get_quarter()
        self.title = "{month} {year}".format(
            month=self.month_names[self.active_date[1] - 1],
            year=self.active_date[2],
        )

        self.title_label.text = self.title

    def on_touch_move(self, touch):
        """ Switch months pages by touch move """

        if self.touch_switch:
            # Left - prev
            if touch.dpos[0] < -30:
                self.go_prev(None)
            # Right - next
            elif touch.dpos[0] > 30:
                self.go_next(None)


class LabelButton(ButtonBehavior, Label):
    pass


class LabelToggleButton(ToggleButtonBehavior, Label):
    pass


class ArrowButton(LabelButton):
    pass


class MonthYearLabel(Label):
    pass


class MonthsManager(ScreenManager):
    pass


class ButtonsGrid(GridLayout):
    pass


class DayAbbrLabel(Label):
    pass


class DayAbbrWeekendLabel(DayAbbrLabel):
    pass


class DayButton(LabelToggleButton):
    pass


class DayNumButton(DayButton):
    pass


class DayNumWeekendButton(DayButton):
    pass
