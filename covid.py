import pandas as pd
import requests
from bs4 import BeautifulSoup
from plyer import notification
from tkinter import *
from tkinter import messagebox, filedialog


def scrap():
    def notifyme(title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon='stay-home.ico',
            timeout=20
        )

    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url,timeout=8)
    # print(r.text)
    soup = BeautifulSoup(r.content, 'html.parser')
    (soup.prettify())
    tablebody = soup.find('tbody')
    # tablebody
    ttt = tablebody.find_all("tr")
    notifycountry=countrydata.get()
    if(notifycountry==''):
        notifycountry='india'
    #variables
    countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases = [], [], [], [], [], [], []
    serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion = [], [], [], [], []

    headers = ['countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
            'serious', 'totalcases_permillion', 'totaldeaths_permillion', 'totaltests', 'totaltests_permillion']
    for i in ttt:
        id = i.find_all('td')
        if (id[1].text.strip().lower() == notifycountry):
            total_cases1=int(id[2].text.strip().replace(',',''))
            total_deaths1=id[4].text.strip()
            new_cases1=id[3].text.strip()
            new_deaths1=id[5].text.strip()
            notifyme('Crona Virus Details in {}'.format(notifycountry),'total_cases : {}\ntotal_death : {}\nnew_cases : {}\nnew_deaths : {}'.format(total_cases1,
                                                                                                                                                   total_deaths1,
                                                                                                                                                   new_cases1,
                                                                                                                                                   new_deaths1))


        countries.append(id[1].text.strip())
        total_cases.append(int(id[2].text.strip().replace(',', '')))
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[7].text.strip())
        serious.append(id[8].text.strip())
        totalcases_permillion.append(id[9].text.strip())
        totaldeaths_permillion.append(id[10].text.strip())
        totaltests.append(id[11].text.strip())
        totaltests_permillion.append(id[12].text.strip())

    df=pd.DataFrame(list(zip(countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases,
                             serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion)),columns=headers)
    sort_values=df.sort_values('total_cases',ascending=False)
    for k in formatlist:
        if(len(formatlist) !=0):
            path2='{}/All Data Save.html'.format(path)
            sort_values.to_html(r'{}'.format(path2))

        if(len(formatlist) !=0):
            path2='{}/All Data Save.jason'.format(path)
            sort_values.to_json(r'{}'.format(path2))

        if(len(formatlist) !=0):
            path2='{}/All Data Save.csv'.format(path)
            sort_values.to_csv(r'{}'.format(path2))

    if(len(formatlist)!=0):
        messagebox.showinfo('Notification',"your data saved {}".format(path2),parent=root)


def download():
    global path
    if (len(formatlist)!= 0):
        path=filedialog.askdirectory()
    else:
        print('Data not save because u not click greens button only show notifcation')
    scrap()
    formatlist.clear()
    InHtml.configure(state='normal')
    InJson.configure(state='normal')
    InCsv.configure(state='normal')

def inhtml():
    formatlist.append('html')
    InHtml.configure(state='disabled')
def incsv():
    formatlist.append('csv')
    InCsv.configure(state='disabled')
def injson():
    formatlist.append('json')
    InJson.configure(state='disabled')



root = Tk()
root.title('Crona Virus Info')
root.geometry('600x300+200+80')
root.config(bg='SeaGreen3')
root.iconbitmap('stay-home.ico')
formatlist = []
path=''
#############################################labels
IntroLabel = Label(root, text='Crona Virus Info', font=('new roman', 30, 'italic bold'), bg='cyan2', width=22,
                   relief=RIDGE).place(x=0, y=0)
EntryLabel = Label(root, text='Search Country', font=('Chillar', 20, 'italic bold'), bg='sky blue', fg='Blue',
                   relief=GROOVE, width=13).place(x=10, y=70)
FormatLabel = Label(root, text='DOWNLOAD IN', font=('chillar', 25, 'bold'), bg='gold2', relief=RIDGE).place(x=10, y=150)

########################################################entry box

countrydata = StringVar()
Ent = Entry(root, textvariable=countrydata, font=("chillar", 20, 'italic bold'), relief=RIDGE, bd=2, width=20).place(
    x=280, y=70)

##########################################################################################################################Buttons

InHtml = Button(root,text='Html',bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=5,command=inhtml)
InHtml.place(x=260,y=150)

InJson = Button(root,text='Json',bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=5,command=injson)
InJson.place(x=355,y=150)

InCsv = Button(root,text='Csv',bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=5,command=incsv)
InCsv.place(x=470,y=150)

submitbtn = Button(root, command=download,text='Subbmit', bg='Sky blue', font=("chillar", 15, "italic bold"),
                   relief=RIDGE, activebackground='blue', bd=5, width=7).place(x=200, y=250)

root.mainloop()