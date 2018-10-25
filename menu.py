class Option:
    def __init__(self, text, function_handler=None, sub_menu=None):
        self.text = text
        self.function_handler=function_handler
        self.sub_menu = sub_menu
    def __call__(self):
        if self.function_handler is None:
            return
        self.function_handler()




class Menu:
    def __init__(self, options=None):
        self.options=[]
        if options is None:
            options = []
        self.add_option(options)
    def __call__(self):
        self.display()
    def display(self):
        os.system('cls')
        for option_response, option in enumerate(self.options):
            print('[' + str(option_response) + ']' + ' -- ' + option.text)
        choice = int(input(">> "))
        self.options[choice]()
        
    def add_option(self, options):
        for option in options:
            self.options.append(option)
            
    def start(self):
        self.display()