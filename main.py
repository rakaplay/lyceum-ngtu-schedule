#     ––––––––––––––––––
#    |    SOME IMPORTS     |
#     ––––––––––––––––––
        

# Importing some material design elements (labels, buttons, cards)
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDFillRoundFlatButton, MDIconButton, MDFlatButton, MDRoundFlatButton, MDRoundFlatIconButton, MDFillRoundFlatButton, MDRoundFlatButton, MDFillRoundFlatIconButton 
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label

# Importing StringProperty to save strings between screens
from kivy.properties import StringProperty

# Importing widgets-containers
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.floatlayout import MDFloatLayout
FloatLayout = MDFloatLayout

# Importing window 
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# Importing MDApp object to run our app with Material Design 
from kivymd.app import MDApp

# Importing ScheduleGet parser, time module, datetime for lesson's time monitoring, colorsys for color manipulations
import schedule_get as sg
import os
import time
import colorsys 
import datetime
import random as rd
# Material Design color definitions and HEX converter
from kivymd.color_definitions import colors
from kivy.utils import get_color_from_hex 

#     ––––––––––––––––––––
#    |DESIGN PREPARATIONS|
#     ––––––––––––––––––––
        


# Color converter for dark theme
def blacked(rgb_color, coef=0.3):
    if isinstance(rgb_color, str): 
        rgb = get_color_from_hex(rgb_color)
    else:
        rgb = rgb_color
    rgb = [color for color in rgb]
    hsv = list(colorsys.rgb_to_hsv(*rgb[:3])) 
    print(hsv)
    hsv[-1] = hsv[-1]*coef
    blckd = list(colorsys.hsv_to_rgb(*hsv)) 
    return blckd
print(blacked("FF5722")) 




# Kivy window 
from kivy.core.window import Window


 
 # Color palletes
pallete = [[1,1,1]]
pallete_dark = [[0,0,0], [1,1,1], [1, 0.8,0.8], blacked(colors['DeepOrange']['200'], coef=0.15), blacked(colors['DeepOrange']['200'], coef=0.4), blacked(colors['DeepOrange']['400'], coef=0.4), blacked(colors['DeepOrange']['300'], coef=0.6)]




# Version 
ver = '''
Версия: 1.1 (β) 30.04.2024
Выполнена в рамках НПК 2025
'''



# Lesson label 
class TimeLabel(Label):
    def update_time(self, *args):
        self.text = sg.check_lesson_time()

                
# Special print() for callbacks
def printC(*args):
    print("[MainCallback]", *args)

# Hints for MDRoundFlatIconButton: ['_animation_fade_bg', '_default_icon_color', '_default_text_color', '_default_theme_icon_color', '_default_theme_text_color', '_disabled_color', '_doing_ripple', '_fading_out', '_finishing_ripple', '_icon_color', '_line_color', '_line_color_disabled', '_md_bg_color', '_md_bg_color_disabled', '_min_height', '_min_width', '_no_ripple_effect', '_radius', '_ripple_rad', '_round_rad', '_text_color', '_theme_icon_color', '_theme_text_color', 'always_release', 'anchor_x', 'anchor_y', 'center', 'center_x', 'center_y', 'children', 'cls', 'device_ios', 'disabled', 'disabled_color', 'font_name', 'font_size', 'font_style', 'halign', 'height', 'icon', 'icon_color', 'icon_size', 'id', 'ids', 'last_touch', 'lbl_ic', 'lbl_txt', 'line_color', 'line_color_disabled', 'line_width', 'md_bg_color', 'md_bg_color_disabled', 'min_state_time', 'motion_filter', 'opacity', 'opposite_colors', 'padding', 'parent', 'pos', 'pos_hint', 'right', 'ripple_alpha', 'ripple_canvas_after', 'ripple_color', 'ripple_duration_in_fast', 'ripple_duration_in_slow', 'ripple_duration_out', 'ripple_func_in', 'ripple_func_out', 'ripple_rad_default', 'ripple_scale', 'rounded_button', 'size', 'size_hint', 'size_hint_max', 'size_hint_max_x', 'size_hint_max_y', 'size_hint_min', 'size_hint_min_x', 'size_hint_min_y', 'size_hint_x', 'size_hint_y', 'state', 'text', 'text_color', 'theme_cls', 'theme_icon_color', 'theme_text_color', 'top', 'valign', 'widget_style', 'width', 'x', 'y'] 

# schedule update
try: 
    sg.js_sure_download() # forced install
    printC("Расписание успешно скачано") # if success
except Exception as e: # if internet bugs
    print('Ошибка при загрузке данных:', e) # catching error



# Own ScreenManager to use StringProperty()
class MyScreenManager(ScreenManager):
    selected_class = StringProperty('')


#     ––––––––––––––––––                                                                                                                                                                                                            
#    |      APPLICATION       |
#     ––––––––––––––––––
# Screen1: main screen. 
class Screen1(Screen):
    #     ––––––––––––––––––
    #    |       INITIALIZING       |
    #     ––––––––––––––––––
    
    def __init__(self, **kwargs):
        super(Screen1, self).__init__(**kwargs)  # Giving Screen1 parent widget permissions 
        
        
        
        
        
        #     ––––––––––––––––––
        #    |      DESIGN PART        |
        #     ––––––––––––––––––
        global pallete_dark
        layout = FloatLayout(md_bg_color=pallete_dark[3]) # main layout
        
        # Main card with text and buttons with schedule and exchanges
        card = MDCard(pos_hint={"center_x": 0.5, "top": 0.75}, size_hint=(0.8, 0.5), md_bg_color=pallete_dark[4])
        global blacked
        # Version card
        about = MDCard(pos_hint={"center_x": 0.5, "top": 0.82}, size_hint=(0.8, 0.06), ripple_behavior=True, ripple_alpha=0.3, on_release=self.about_screen, md_bg_color=blacked(pallete_dark[4], coef=0.8)) 
        # Version label
        about.add_widget(MDLabel(text="О программе", halign="center"))
        
        # Adding "about" widget 
        layout.add_widget(about)
        card_layout = FloatLayout(size_hint=(1, 1))
        time_card = MDCard(pos_hint={"center_x": 0.5, "top": 0.24}, size_hint=(0.8, 0.1), md_bg_color=blacked(pallete_dark[4], 0.6)) 
        card.add_widget(card_layout)
        btn_inside = MDFillRoundFlatIconButton(text="Расписание классов", size_hint=(0.7, 0.1), pos_hint={"center_x": 0.5, "top": 0.4}, on_release=self.go_to_screen2, icon="account-school-outline", md_bg_color=pallete_dark[6]) 
        card_layout.add_widget(btn_inside)
        exchanges = MDFillRoundFlatIconButton(text="Лента изменений", size_hint=(0.7, 0.1), pos_hint={"center_x": 0.5, "top": 0.525}, on_release=self.exchange_tape, icon="newspaper-variant", md_bg_color=pallete_dark[6])
        card_layout.add_widget(exchanges)
        label_inside = MDLabel(text="Расписание\nИЛ НГТУ", size_hint=(0.7, 0.5), font_style="H4", halign="center", pos_hint={"center_x": 0.5, "top": 1})
        printC(datetime.datetime.now().strftime('%H:%M'), type(datetime.datetime.now().strftime('%H:%M')))  
        time_label = TimeLabel(text=sg.check_lesson_time(),  font_size=dp(18), halign="center")
        Clock.schedule_interval(time_label.update_time, 1)
        time_card.add_widget(time_label)
        card_layout.add_widget(label_inside)
        layout.add_widget(time_card)
        layout.add_widget(card)
        self.add_widget(layout)

    def go_to_screen2(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'screen2'
    def about_screen(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "screen4"
    def exchange_tape(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "screen5" 



# Экран 2: Выбор класса
class Screen2(Screen):
    def __init__(self, **kwargs):
        global blacked
        global pallete_dark
        super(Screen2, self).__init__(**kwargs)
        layout = FloatLayout(md_bg_color=pallete_dark[3])
        scroll = ScrollView(size_hint=(1, 0.9), pos_hint={"center_x": 0.5, "center_y": 0.45})
        self.button_back = MDFillRoundFlatIconButton(text='Вернуться', pos_hint={"center_x": 0.5, "center_y": 0.94}, size_hint=(1, 0.06), icon="arrow-left", on_release=self.go_to_screen1, md_bg_color=pallete_dark[6])
        layout.add_widget(self.button_back)
        grid = GridLayout(cols=2, spacing=50, size_hint=(1, 3))
        grid.bind(minimum_height=grid.setter('height'))
        self.some_cards = []
        for i in sg.all_classes():
            self.some_cards.append(MDCard(size_hint=(1, 2), ripple_behavior=True, ripple_alpha=0.2,  md_bg_color=blacked(pallete_dark[3], coef=(rd.randint(20, 24)/10)))) 
            btn = MDFlatButton(text=str(i).strip(), ripple_alpha=0, on_release=self.class_name, size_hint=(1, 1), halign="center")
            self.some_cards[-1].add_widget(btn)
            grid.add_widget(self.some_cards[-1])
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)
    def go_to_screen1(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'screen1'
    def class_name(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.selected_class = instance.text
        self.manager.current = 'screen3'

# Экран 3: Расписание выбранного класса
class Screen3(Screen):
    def __init__(self, **kwargs):
        global blacked
        global pallete_dark
        super(Screen3, self).__init__(**kwargs)
        self.layout = FloatLayout(md_bg_color=pallete_dark[3])
        # Задаем цвет фона
        self.label1 = MDLabel(text="Загрузка..", pos_hint={"center_x": 0.5, "center_y": 0.94}, font_style="H4", halign="center")
        self.layout.add_widget(self.label1)
        self.label = MDLabel(text="", pos_hint={"center_x": 0.5, "center_y": 0.94}, font_style="H4", halign="right")
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)
    def go_to_screen2(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'screen2'
        [self.scrvLayout.remove_widget(i) for i in self.cards] 
        [self.layout.remove_widget(i) for i in (self.button_back, self.label1, self.scrollview)] 
        
    def on_enter(self, *args):
        global blacked
        global pallete_dark
        self.label.text = f"Расписание {str(self.manager.selected_class).upper()} "
        self.button_back = MDFillRoundFlatIconButton(text='Вернуться', pos_hint={"center_x": 0.15, "center_y": 0.94}, icon="arrow-left", on_release=self.go_to_screen2,md_bg_color=pallete_dark[6])
        self.layout.add_widget(self.button_back)
        schedule = sg.translate(sg.class_name_converter(self.manager.selected_class, db=True)) 
        print(self.manager.selected_class)
        self.label1.text = "Загрузка." 
        lesson_arr = sg.everything_class(sg.class_name_converter(self.manager.selected_class, db=True))[-1]
        self.label1.text = "Загрузка..."
        time.sleep(0.1)
        self.label1.text = ""
        self.scrollview = RecycleView(size_hint=(1, 0.9), pos_hint={"center_x":0.5, "center_y":0.45})
        self.scrvLayout = GridLayout(cols=1, size_hint=(1, 6), spacing=50)
        self.scrollview.add_widget(self.scrvLayout)
        self.layout.add_widget(self.scrollview)
        self.cards = []
        self.layouts_inside = []
        printC("Lesson arrangement (аранжировка уроков) у " + self.manager.selected_class + ' класса: ' +str(lesson_arr)) 
        for day in range(len(lesson_arr)):
            self.cards.append(MDCard(ripple_behavior=True, ripple_alpha=0.3, md_bg_color=pallete_dark[4])) 
            self.layouts_inside.append(GridLayout(cols=4, size_hint=(1, 1), spacing=30)) 
            self.layouts_inside[-1].add_widget(Label(text='Урок', halign="left", font_size=dp(12), color=pallete_dark[2]))
            self.layouts_inside[-1].add_widget(Label(text='Предмет', font_size=dp(12), halign="left", color=pallete_dark[2]))
            self.layouts_inside[-1].add_widget(Label(text="Учитель", halign="center", font_size=dp(12), color=pallete_dark[2]))
            self.layouts_inside[-1].add_widget(Label(text="Кабинет", halign="center", font_size=dp(12), color=pallete_dark[2]))
            for i in range(len(lesson_arr[day])):
                self.layouts_inside[-1].add_widget(MDLabel(text=''.join([i for i in str(lesson_arr[day][i]) if i.isnumeric()]), halign="center"))
                temp_lesson = str(schedule[0][day][i]).replace("[", '').replace("]", "").replace("'",'').replace('"', '').replace(",",",\n").replace('методы решения', '\nметоды\nрешения').replace('чтение', '\nчтение').replace('к практике', '\nк практике').replace('олимпиадных','\nолимпиадных\n').replace('математика', '\nматематика').replace("Инженер авиастроительного", "Авиастроение").replace('онная','онная\n').replace('п...','').replace('еский','еский\n').replace('мат. логики','\nмат. логики').replace('решения экономиче...', 'решения экон. задач')
                # MDLabel styles hint: ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Subtitle1', 'Subtitle2', 'Body1', 'Body2', 'Button', 'Caption', 'Overline', 'Icon'] 
                self.layouts_inside[-1].add_widget(MDLabel(text=temp_lesson, font_style="Body2", halign="left", width=dp(100))) 
                self.layouts_inside[-1].add_widget(Label(text=str(schedule[1][day][i]).replace("[", '').replace("]", "").replace("'",'').replace('"', '').replace(',','\n'), halign="center", font_size=dp(12), color=pallete_dark[1])) 
                self.layouts_inside[-1].add_widget(MDLabel(text=str(schedule[2][day][i]).replace("[", '').replace("]", "").replace("'",'').replace('"', '').replace(",", ",\n"), halign="right", color=pallete_dark[1])) 
            self.cards[-1].add_widget(self.layouts_inside[-1]) 
            self.scrvLayout.add_widget(self.cards[-1])
        self.cards.append(MDCard(ripple_behavior=True, ripple_alpha=0.3, size_hint=(1, 0.3), md_bg_color=blacked(pallete_dark[4], coef=0.7)))
        try:
            self.cards[-1].add_widget(MDLabel(text=sg.all_translated_exchanges()[1][sg.class_name_converter(self.manager.selected_class)], halign="center"))
        except:
            self.cards[-1].add_widget(MDLabel(text="Изменений нет.",halign="center"))
        self.scrvLayout.add_widget(self.cards[-1])
            
class Screen4(Screen):
    def __init__(self, **kwargs):
        super(Screen4, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.button_back = MDFillRoundFlatIconButton(text='Вернуться', pos_hint={"center_x": 0.5, "center_y": 0.94}, size_hint=(0.8, 0.06), icon="arrow-left", on_release=self.go_to_screen1, md_bg_color=pallete_dark[6])
        self.layout.add_widget(self.button_back)
        global ver
        self.layout.add_widget(MDCard(MDLabel(text=ver, font_style="H3", halign="center"))) 
        self.add_widget(self.layout)
    def go_to_screen1(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'screen1'
 
class Screen5(Screen):
    def __init__(self, **kwargs):
        super(Screen5, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.view = ScrollView(size_hint=(1, 1))
        self.layout_inside = GridLayout(cols=1, size_hint=(1, 5), spacing=40)
        self.view.add_widget(self.layout_inside)
        self.layout.add_widget(self.view)
        txt = list(sg.all_translated_exchanges()[1].values()) 
        print(txt)
        self.button_back = MDFillRoundFlatIconButton(text='Вернуться', pos_hint={"center_x": 0.5, "center_y": 0.94}, size_hint=(0.8, 0.06), icon="arrow-left", on_release=self.go_to_screen1, md_bg_color=pallete_dark[6])
        self.layout.add_widget(self.button_back)
        cls_names = [sg.class_name_converter(i, db=False) for i in sg.all_translated_exchanges()[-1]]
        for i in range(len(txt)):
            self.layout_inside.add_widget(MDCard( MDLabel(text=cls_names[i], halign="center", font_style="H4"), size_hint=(0.3, 1))) 
            self.layout_inside.add_widget(MDCard(MDLabel(text=txt[i], halign="center"), width=dp(80))) 
        self.add_widget(self.layout)
    def go_to_screen1(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'screen1'

# Основное приложение
class TestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        printC(colors['DeepOrange']['500']) 
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "700"
        sm = MyScreenManager()
        sm.add_widget(Screen1(name='screen1'))
        sm.add_widget(Screen2(name='screen2'))
        sm.add_widget(Screen3(name='screen3'))
        sm.add_widget(Screen4(name='screen4'))
        sm.add_widget(Screen5(name="screen5"))
        return sm

# Запуск приложения
TestApp().run()