import io 
import webbrowser # provides a high-level interface that allows displaying Web-based documents to users = CLI tool
import requests
from tkinter import * # GUI library for python
from urllib.request import urlopen
from PIL import ImageTk,Image # PIL- python imaging Library

class NewsApp:

    def __init__(self):

        # fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=8964a43e059440179d9adeb53259c14f').json()
        # initial GUI load
        self.load_gui()
        # load the 1st news item
        self.load_news_item(0)

    # we can choose any variable name that is valid in Python for this purpose. The important thing is to be consistent with the variable name you use throughout your code when interacting with the main window and its widgets.
    def load_gui(self):
        self.root = Tk() # this class it will create a class level variable root and initialize it with Tk() object and whenever you want to access this variable in the class you will call it with self.root
        self.root.geometry('350x600')
        self.root.resizable(0,0)
        self.root.title('Daily News App')
        self.root.configure(background='black')
    
    # its function is to blank the gui window so that the next news item can be loaded.
    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self,index):

        # clear the screen for the new news item
        self.clear()

        # image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350,250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)


        label = Label(self.root,image=photo)
        label.pack()


        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', wraplength=350, justify='center')
        heading.pack(pady=(10,20))
        heading.config(font=('verdana',15))

        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        frame = Frame(self.root,bg='black')
        frame.pack(expand=True,fill=BOTH)

        if index != 0:
            prev = Button(frame,text='Prev',width=16,height=3,command=lambda :self.load_news_item(index-1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=16, height=3,command=lambda :self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index != len(self.data['articles'])-1:
            next = Button(frame, text='Next', width=16, height=3,command=lambda :self.load_news_item(index+1))
            next.pack(side=LEFT)

        self.root.mainloop()

    def open_link(self,url):
        webbrowser.open(url)


obj = NewsApp()