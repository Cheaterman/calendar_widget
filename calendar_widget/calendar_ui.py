'''
Kivy Garden - Calendar Widget
====

Calendar for Kivy based on KivyCalendar made by Oleg Kozlov

'''

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ReferenceListProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import (
    Screen,
    ScreenManager,
)
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButtonBehavior

from . import calendar_data as cal_data


Builder.load_string("""
<Calendar>:
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size

<ArrowButton>:
    pos_hint: {'center_y': .5}
    size_hint: None, .65
    width: self.height
    opacity: 1 if self.state == 'normal' else .6

<MonthYearHeader>:
    text: ''
    text_color: 1, 1, 1, 1
    background_color: .4, .45, 1, 1
    padding: dp(10), 0
    pos_hint: {"top": 1, "center_x": .5}
    size_hint_y: 0.1

    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size

    ArrowButton:
        source: root.left_arrow_source
        on_press: root.dispatch('on_arrow_left', root)

    MonthYearLabel:
        text: root.text

    ArrowButton:
        source: root.right_arrow_source
        on_press: root.dispatch('on_arrow_right', root)

<MonthYearLabel>:
    bold: True
    halign: "center"
    pos_hint: {"top": 1, "center_x": .5}

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
        self.cal = Calendar(
            as_popup=True,
            touch_switch=self.touch_switch,
        )
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


class Calendar(RelativeLayout):
    """Basic calendar widget.

    :Class:`Calendar` is a calendar widget for kivy, use :attr:`active_date`
    to get the result of your date selection.
    """

    # logic
    active_date = ListProperty()
    """Selected date.

    :attr:`active_date` is a :class:`ListProperty` wich contains the selected
    date as: [date, month, year]
    """

    locale = StringProperty()
    """Locale date formatting setting.

    :attr:`locale` -- change the default locale used by the :class:`Calendar`.
    If :attr:`locale` is default, '', locale will be you're system default.

    :attr:`locale` is a :class:`StringProperty` and default is ''.
    """

    # design
    background_color = ListProperty([1, 1, 1, 1])
    """Color for the background.

    :attr:`background_color` -- to change the color of the main background.

    :attr: `background_color` is a :class:`ListProperty` and default is
    [1, 1, 1, 1].
    """

    foreground_color = ListProperty([0, 0, 0, 1])
    """Color for the foreground.

    :attr:`foreground_color` -- to change the color of the main label.

    :attr: `foreground_color` is a :class:`ListProperty` and default is
    [0, 0, 0, 1].
    """

    header_color = ListProperty([.4, .45, 1, 1])
    """Color for the header's background.

    :attr:`header_color` -- to change the color of the header's background.

    :attr: `header_color` is a :class:`ListProperty` and default is
    [.4, .45, 1, 1].
    """

    left_arrow_source = StringProperty('icons/left_arrow.png')
    """Left arrow Image.

    :attr:`left_arrow_source` -- to change the default left arrow image path.

    :attr:`left_arrow_source` is a :class:`ListProperty` and default is
    'calendar_widget/icons/left_arrow.png'.
    """

    right_arrow_source = StringProperty('icons/right_arrow.png')
    """Right arrow Image.

    :attr:`right_arrow_source` -- to change the default right arrow image path.

    :attr:`right_arrow_source` is a :class:`ListProperty` and default is
    'calendar_widget/icons/right_arrow.png'.
    """

    def __init__(self, as_popup=False, touch_switch=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.as_popup = as_popup
        self.touch_switch = touch_switch
        self.prepare_data()
        self.init_ui()

    def on_locale(self, *args):
        self.prepare_data()
        self.reset_widget()

    def reset_widget(self):
        """Only use this method if you want to use another default date.

        Example:
        >>> cal = Calandar() #active_date will be now()
        >>> cal.active_date = [05, 02, 1999] #New default date
        >>> cal.reset_widget() # destroy ui & redraw
        """
        self.clear_widgets()
        self.title = "{month} {year}".format(
            month=self.month_names[self.active_date[1] - 1],
            year=self.active_date[2],
        )
        self.get_quarter()
        self.init_ui()

    def init_ui(self):

        # Title
        self.title_label = MonthYearHeader(
            text=self.title,
            left_arrow_source=self.left_arrow_source,
            right_arrow_source=self.right_arrow_source,
            on_arrow_left=self.go_prev,
            on_arrow_right=self.go_next,
        )
        self.bind(
            foreground_color=self.title_label.setter('text_color'),
            header_color=self.title_label.setter('background_color'),
            left_arrow_source=self.title_label.setter('left_arrow_source'),
            right_arrow_source=self.title_label.setter('right_arrow_source'),
        )
        self.add_widget(self.title_label)

        # ScreenManager
        self.screenmanager = MonthsManager()
        self.add_widget(self.screenmanager)

        self.create_month_screen(self.quarter[1])

    def create_month_screen(self, month):
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
        self.month_names = cal_data.get_month_names(locale=self.locale)
        self.month_names_eng = cal_data.get_month_names(locale='en')
        self.days_abrs = cal_data.get_days_abbrs(locale=self.locale)

        if not self.active_date:
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
        """ Get calendar and months/years nums for quarter """

        current_month = self.active_date[1]
        current_year = self.active_date[2]

        self.quarter_nums = cal_data.calc_quarter(
            current_year,
            current_month,
        )

        self.quarter = cal_data.get_quarter(
            current_year,
            current_month,
        )

    def get_btn_value(self, inst):
        """ Get day value from pressed button """

        self.active_date[0] = int(inst.text)

        if self.as_popup:
            self.parent_popup.dismiss()

    def go_prev(self, *args):
        """ Go to screen with previous month """
        max_day = max((
            day[0]
            for week in self.quarter[0]
            for day in week
            if day[2]
        ))
        selected_day = min(self.active_date[0], max_day)

        # Change active date
        self.active_date = [selected_day, self.quarter_nums[0][1],
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

        old_screen = self.screenmanager.current_screen
        self.screenmanager.current = prev_scr_name
        self.screenmanager.transition.direction = "right"
        self.screenmanager.remove_widget(old_screen)

        self.get_quarter()
        self.title = "{month} {year}".format(
            month=self.month_names[self.active_date[1] - 1],
            year=self.active_date[2],
        )

        self.title_label.text = self.title

    def go_next(self, *args):
        """ Go to screen with next month """
        max_day = max((
            day[0]
            for week in self.quarter[2]
            for day in week
            if day[2]
        ))
        selected_day = min(self.active_date[0], max_day)

        # Change active date
        self.active_date = [selected_day, self.quarter_nums[2][1],
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

        old_screen = self.screenmanager.current_screen
        self.screenmanager.current = next_scr_name
        self.screenmanager.transition.direction = "left"
        self.screenmanager.remove_widget(old_screen)

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


class LabelToggleButton(ToggleButtonBehavior, Label):
    pass


class ArrowButton(ButtonBehavior, Image):
    pass


class MonthYearLabel(Label):
    pass


class MonthYearHeader(BoxLayout):
    __events__ = ('on_arrow_left', 'on_arrow_right',)

    left_arrow_source = StringProperty()
    right_arrow_source = StringProperty()
    text = StringProperty()
    text_color = ListProperty()
    background_color = ListProperty()

    def on_arrow_left(self, *args):
        pass

    def on_arrow_right(self, *args):
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
