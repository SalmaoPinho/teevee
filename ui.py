from utilities import UElement, Glock,TeeVee
glock=Glock()
tv=TeeVee()
user_interface = {
    "top_bar": UElement(
        x_percent=0.125,
        y_percent=0.0625,
        width_percent=0.75,
        height_percent=0.125,
        color=(255, 255, 255),
        subelements={
            'nav_prev':{
                'width_percent':0.2,
                'text':"<<",
                'clickable':True,
            },
            'title_area': {
                'x_percent':0.2,
                'width_percent':0.6,
                'subelements':{
                    "main_title": {
                        'text':"MENU",
                        'font_size_percent':0.08,
                    },
                }
            },
            "nav_next": {
                'x_percent':0.8,
                'width_percent':0.2,
                'text':">>",
                'clickable':True,
            }
        }
    ),
    "content_panel": UElement(
        x_percent=0.125,
        y_percent=0.175,
        width_percent=0.75,
        height_percent=0.675,
        color=(255, 255, 255),
        subelements={
            "cpu-info": {
                'y_percent':0.0,
                'height_percent':0.2,
                'font_size_percent':0.05,
                'subelements':{
                    "cpu-temp": {
                        'y_percent':0.0,
                        'text':"!cpu_temp",
                        'font_size_percent':0.05,
                    },
                    "cpu-usage": {
                        'y_percent':0.33,
                        'text':"!cpu_usage",
                        'font_size_percent':0.05,
                    },
                    "cpu-freq": {
                        'y_percent':0.66,
                        'text':"!cpu_freq",
                        'font_size_percent':0.05
                    },
                }
            },
        }
    ),
    "bottom_bar": UElement(
        x_percent=0.125,
        y_percent=0.85,
        width_percent=0.75,
        height_percent=0.125,
        color=(255, 255, 255),
        subelements={
            "time_display": {
                'width_percent':0.33,
                'font_size_percent':0.05,
                'text':"!time_24hr",
                'color':(255, 255, 255),
            },
            "date_display": {
                'x_percent':0.33,
                'width_percent':0.33,
                'font_size_percent':0.0425,
                'text':"!short_date",
            },
            "weekday_display": {
                'x_percent':0.67,
                'width_percent':0.33,
                'font_size_percent':0.05,
                'text':"!week_day",
                'color':(255, 255, 255),
            },
        }
    ),
}

def clickable_elements():
    buttons=[]
    
    for element_key in user_interface:
        element = user_interface[element_key]
        if element.clickable:
            buttons.append(element)
        for subelement_key in element.subelements:
            subelement = element.subelements[subelement_key]
            if subelement.clickable:
                buttons.append(subelement)
    return buttons

def render_ui(screen):
    
    for element_key in user_interface:
        element = user_interface[element_key]   
        element.draw(screen)
    return user_interface