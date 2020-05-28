import os
import tkinter as tk
from io import BytesIO
from tkinter import filedialog

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
import numpy as np
import requests
from PIL import Image
from keras.models import load_model


model = load_model('Model/Object_Model.h5')
url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

default_directory = os.path.abspath(os.curdir)


class MainWindow(Screen):
    def identify(self):
        labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        tk.Tk().withdraw()
        input_path = filedialog.askopenfilename()
        input_image = Image.open(input_path).resize((32, 32), resample=Image.LANCZOS)
        image_array = np.array(input_image).astype('float32')
        image_array /= 255.0
        image_array = image_array.reshape(1, 32, 32, 3)
        answer = model.predict(image_array)
        self.ans.text = str(labels[np.argmax(answer)]).title()
        answer = self.ans.text
        if answer != "Dog":
            self.ans.text = "Not A Dog\n\nPlease Select a Dog's Picture for Classification"
        else:
            try:
                if self.ans.text == "Dog":
                    path = input_path
                    data = {'file': open(path, 'rb'), 'modelId': ('', '052e52ea-845f-4b4a-9fe1-b27dd2eb19d6')}
                    response = requests.post(url,
                                             auth=requests.auth.HTTPBasicAuth('5Ner4sKSl0ikoPQ074_35YoNk9JBX__W', ''),
                                             files=data)
                    a = response.text.replace("{\"message\":\"Success\",\"result\":[{\"message\":\"Success\","
                                              "\"prediction\":[{\"label\":\"", "").split("\"")
                    label = a[0].replace("_", " ").title()
                    self.ans.text = "Dog\nBreed - " + label
            except:
                self.ans.text = "Dog\nConnect to Internet for breed"

    def identify_url(self, url_given):
        if url_given:
            labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
            input_path = requests.get(self.url_entry.text)
            input_image = Image.open(BytesIO(input_path.content)).resize((32, 32), resample=Image.LANCZOS)
            image_array = np.array(input_image).astype('float32')
            image_array /= 255.0
            image_array = image_array.reshape(1, 32, 32, 3)
            answer = model.predict(image_array)
            self.ans.text = str(labels[np.argmax(answer)]).title()
            answer = self.ans.text
            if answer != "Dog":
                self.ans.text = "Not A Dog\n\nPlease Select a Dog's Picture for Classification"
            else:
                try:
                    if self.ans.text == "Dog":
                        path = input_path
                        data = {'file': open(path, 'rb'), 'modelId': ('', '052e52ea-845f-4b4a-9fe1-b27dd2eb19d6')}
                        response = requests.post(url,
                                                 auth=requests.auth.HTTPBasicAuth('5Ner4sKSl0ikoPQ074_35YoNk9JBX__W',
                                                                                  ''),
                                                 files=data)
                        a = response.text.replace("{\"message\":\"Success\",\"result\":[{\"message\":\"Success\","
                                                  "\"prediction\":[{\"label\":\"", "").split("\"")
                        label = a[0].replace("_", " ").title()
                        self.ans.text = "Dog\nBreed - " + label
                except:
                    self.ans.text = "Dog\nConnect to Internet for breed"


class WindowManager(ScreenManager):
    pass


class Gui(App):
    def build(self):
        return Builder.load_file("gui.kv")


if __name__ == '__main__':
    Gui().run()
