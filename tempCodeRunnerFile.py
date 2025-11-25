class UElement:
    def __init__(self, x_percent=0, y_percent=0, width_percent=1, height_percent=1, 
                 text='', color=None, clickable=False, font_size_percent=0.1, 
                 outline_size=5, subelements=None):
        
        # ... resto do código inicial (conversões para pixels, etc) ...
        
        # Armazena as porcentagens para redimensionamento
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        self.font_size_percent = font_size_percent
        
        # Processa subelementos se for um dicionário
        self.subelements = {}
        if subelements is not None:
            converted_subelements = {}
            for subelement_key, subelement_dict in subelements.items():
                # Cria o UElement a partir do dicionário
                converted_subelements[subelement_key] = UElement(
                    x_percent=self.x_percent + subelement_dict.get('x_percent', 0) * self.width_percent,
                    y_percent=self.y_percent + subelement_dict.get('y_percent', 0) * self.height_percent,
                    width_percent=self.width_percent * subelement_dict.get('width_percent', 1),
                    height_percent=self.height_percent * subelement_dict.get('height_percent', 1),
                    font_size_percent=subelement_dict.get('font_size_percent', 0.1),
                    text=subelement_dict.get('text', ''),
                    color=subelement_dict.get('color', None),
                    clickable=subelement_dict.get('clickable', False),
                    outline_size=subelement_dict.get('outline_size', 5),
                    subelements=subelement_dict.get('subelements', None)  # Processa recursivamente
                )
            self.subelements = converted_subelements