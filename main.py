from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
import menu 
from utils import getPipeNames
from utils import showPipes

class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Outer horizontal BoxLayout for title and authors
        title_author_layout = BoxLayout(orientation='vertical', spacing=10)

        # Title label
        self.title_label = Label(text='Water leakage Detection \nusing Machine Learning ',
                                 font_size='40sp',halign='center', max_lines=2)
        title_author_layout.add_widget(self.title_label)

        # Inner horizontal BoxLayout for authors
        authors_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Author labels
        self.author1_label = Label(text='Jaime Joel Romero Mozota', font_size='20sp')
        authors_layout.add_widget(self.author1_label)

        self.author2_label = Label(text='Mia Obralic', font_size='20sp')
        authors_layout.add_widget(self.author2_label)

        title_author_layout.add_widget(authors_layout)

        layout.add_widget(title_author_layout)

        # Continue button
        self.continue_button = Button(text='Continue', size_hint=(1, None), height='40sp')
        self.continue_button.bind(on_release=self.goToMenu)
        layout.add_widget(self.continue_button)

        self.add_widget(layout)

    
    def goToMenu(self,instance):
        screen_manager = self.manager 
        screen_manager.current = 'screenMenu'

class ScreenMenu(Screen):
    
    def __init__(self, **kwargs):

        super(ScreenMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        createDatasetBtn = Button(text='Create Dataset')
        createDatasetBtn.bind(on_release=self.switchToScreenCases)
        layout.add_widget(createDatasetBtn)

        trainNNBtn = Button(text='Train Neural Network')
        trainNNBtn.bind(on_release=self.processTrainNeuralnetwork)
        layout.add_widget(trainNNBtn)

        tryModelBtn = Button(text='Try Model')
        tryModelBtn.bind(on_release=self.switchToScreenYN)
        layout.add_widget(tryModelBtn)

        exitBtn = Button(text='Exit')
        exitBtn.bind(on_release=self.exitApp)
        layout.add_widget(exitBtn)

        self.add_widget(layout)

    
    def switchToScreenCases (self,instance):
        screen_manager = self.manager  # Access the ScreenManager instance
        screen_manager.current = 'screenCases'



    def processTrainNeuralnetwork(self,instance):
        menu.trainNeuralNetwork()

    def switchToScreenResuts(self,text, instance):
        screen_manager = self.manager  # Access the ScreenManager instance
        screen_manager.current = 'resultScreen'
        screen_manager.get_screen('resultScreen').updateText(str(text))

    def switchToScreenYN (self,instance):
        screen_manager = self.manager  # Access the ScreenManager instance
        screen_manager.current = 'screenYN'


    def exitApp(self, instance):
        App.get_running_app().stop()


class ScreenCases(Screen):
    def __init__(self, **kwargs):
        super(ScreenCases, self).__init__(**kwargs)
        
        # Create a BoxLayout for the screen
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Create the TextInput widget and make it an attribute of the class
        self.text_input = TextInput(hint_text='Number of cases', multiline=False)

        # Add the widgets to the layout
        layout.add_widget(self.text_input)

        submitBtn = Button(text='Submit')
        submitBtn.bind(on_release=lambda btn: self.processResult(self.text_input.text))
        layout.add_widget(submitBtn)

        # Set the layout as the content of the screen
        self.add_widget(layout)

    def processResult(self, nCases):
        menu.createDataset(nCases)
        self.manager.current = 'screenMenu'

class ScreenYN(Screen):
    def __init__(self, **kwargs):
        super(ScreenYN, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Create a labeled switch
        switch_label = Label(text='Add a Leak?')
        switch = Switch(active=False)
        layout.add_widget(switch_label)
        layout.add_widget(switch)

        # Create a button
        button = Button(text='Submit')
        button.bind(on_release=lambda btn: self.processResult(switch.active))
        layout.add_widget(button)

        self.add_widget(layout)

    def processResult(self, is_active):
        if is_active:
            screen_manager = self.manager  # Access the ScreenManager instance
            screen_manager.current = "screenSelectPipe"
        else:
            resultReal,resultPred, resultRealMulti,resultPredMulti=menu.tryModel("n")
            result_screen = self.manager.get_screen('resultScreen')
            result_screen.update_label_text(resultReal, resultPred, resultRealMulti,resultPredMulti)
            self.manager.current = 'resultScreen'

class ScreenSelectPipe(Screen):
    def __init__(self, **kwargs):
        super(ScreenSelectPipe, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Create a labeled dropdown
        pipeSelectLabel = Label(text='In which pipe do you want the leak?:')
        self.pipeSelectButton = Button(text='Select Pipe', size_hint=(None, None))
        self.pipeSelectButton.bind(on_release=self.show_pipe_dropdown)
        layout.add_widget(pipeSelectLabel)
        layout.add_widget(self.pipeSelectButton)

        # Create a labeled slider input
        whereSelectLabel = Label(text='Where in the pipe do you want the leak?:')
        whereSlider = Slider(min=0.011, max=0.99, step=0.01)
        layout.add_widget(whereSelectLabel)
        layout.add_widget(whereSlider)
        
        pipeButton = Button(text='Show pipes')
        pipeButton.bind(on_release=lambda btn:showPipes())
        layout.add_widget(pipeButton)

        # Create a button
        button = Button(text='Submit')
        button.bind(on_release=lambda btn: self.processResult(self.pipeSelectButton.text,whereSlider.value))
        layout.add_widget(button)

        self.add_widget(layout)

    def processResult(self, pipeSelect,whereSelect): 
        resultReal,resultPred , resultRealMulti,resultPredMulti=menu.tryModel("y", pipeSelect, float(whereSelect))
        result_screen = self.manager.get_screen('resultScreen')
        result_screen.update_label_text(resultReal, resultPred, resultRealMulti,resultPredMulti)
        self.manager.current = 'resultScreen'


    def show_pipe_dropdown(self, instance):
        dropdown = DropDown()
        #pipe_names =["23","25","26","27","24","38","39"]
        pipe_names = getPipeNames()

        for pipe_name in pipe_names:
            btn = Button(text=pipe_name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.set_pipe_select(btn.text))
            dropdown.add_widget(btn)

        dropdown.open(instance)

    def set_pipe_select(self, pipe_name):
        self.pipeSelectButton.text = pipe_name
        


class ResultScreen(Screen):
    def __init__(self,labelPre='', labelReal='', **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        labelPre = Label(text='Predicted')
        layout.add_widget(labelPre)

        self.labelPreRes = Label(text = str(labelPre))
        layout.add_widget(self.labelPreRes)

        labelReal = Label(text='Real')
        layout.add_widget(labelReal)

        self.labelRealRes = Label(text=str(labelReal))
        layout.add_widget(self.labelRealRes) 

        
        pipeButton = Button(text='Show pipes')
        pipeButton.bind(on_release=lambda btn:showPipes())
        layout.add_widget(pipeButton)
        
        buttonBackToMenu = Button(text='Continue')
        buttonBackToMenu.bind(on_release=self.backToMenu)
        layout.add_widget(buttonBackToMenu )

        self.add_widget(layout)

    def update_label_text(self ,labelPre, labelReal,labelPipeReal,labelPipePred):

        self.labelPreRes.text = str(labelPre[0])
        self.labelRealRes.text =str(labelReal[0])
        self.showMulti = str(labelReal[0])
        
        self.pipeReal = labelPipeReal
        self.pipePred = labelPipePred


    def backToMenu(self, instance):
        if self.showMulti == "[1.]":
            pipes = getPipeNames()
            self.labelPreRes.text = f"Predicted pipe {pipes[self.pipePred]}"
            self.labelRealRes.text =f"Real pipe {pipes[self.pipeReal]}"
            self.showMulti = "0"

        else :
            self.manager.current = 'screenMenu'



class MyApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()

        titleScreen = TitleScreen(name='titleScreen')
        sm.add_widget(titleScreen)

        # Create screens
        screenMenu = ScreenMenu(name='screenMenu')
        sm.add_widget(screenMenu)

        screenCases = ScreenCases(name = "screenCases")
        sm.add_widget(screenCases)

        screenYN = ScreenYN(name = "screenYN")
        sm.add_widget(screenYN)

        screenSelectPipe = ScreenSelectPipe(name = "screenSelectPipe")
        sm.add_widget(screenSelectPipe)

        resultScreen = ResultScreen(name='resultScreen')
        sm.add_widget(resultScreen)
         
        return sm


if __name__ == "__main__":
    MyApp().run()
