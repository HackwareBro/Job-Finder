import requests,os, colorama, webbrowser
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

colorama.init()
#takes data from user directly or from file
def take_user_data():
    #Take input from user for first time
    data = []
    if not os.path.isfile('data.bin'):
        data.append(input('Input skill names to find job: '))
        data.append(input('Input your city or country or both: '))
        data.append(input('Input your your experience in numbers of years (0 for no experience): '))
        with open('data.bin','w') as f:
            f.write(f'{data[0]}\n{data[1]}\n{data[2]}\n')
    #Take input from file
    else:
        with open('data.bin','r') as f:
            values = f.read()
            data.extend(values.split('\n')[:-1])
    
    return {'jobs':data[0],'location':data[1],'exp':data[2]}

#Simply returns BeautifulSoup object of a given URL to directly play with html tags
def get_webpage(web_url, data): #data var to send in params of link
    input_values = {
        'searchType':'personalizedSearch',
        'from':'submit',
        'txtKeywords': data['jobs'],
        'txtLocation': data['location'],
        "cboWorkExp1": data['exp']
    }
    try:
        response = requests.get(web_url,params=input_values)
        assert response.status_code == 200
    except Exception:
        print("Check your Internet Connection!")
        exit()
    return BeautifulSoup(response.text,'lxml')

def extract_data(html_page):
    jobs = html_page.find_all('li',class_='clearfix job-bx wht-shd-bx')
    #data to be extract
    complete_data = []
    single_data = (        
        'job',
        'company' ,
        'location',
        'skills',
        'link',
    )
    single_data = dict.fromkeys(single_data,'') #to create dict having empty string values
    for job in jobs:
        posted_day = job.find('span',class_='sim-posted').text
        if 'few' in posted_day:
            h2 = job.find('h2')
            single_data['job'] = h2.a.text.strip('\n \r')
            single_data['link'] = h2.a['href'].strip('\n \r')
            single_data['company'] = job.find('h3').text.strip('\n \r')   
            single_data['location'] = job.find('ul', class_='top-jd-dtl clearfix').span.text.strip('\n \r')
            single_data['skills'] = job.find('span',class_='srp-skills').text.strip('\n \r')
            complete_data.append(single_data)
            single_data = dict.fromkeys(single_data,'') # to reset the data
    return complete_data  

if __name__=='__main__':
    print("""   ___       _      ______ _           _
  |_  |     | |     |  ___(_)         | |
    | | ___ | |__   | |_   _ _ __   __| | ___ _ __
    | |/ _ \| '_ \  |  _| | | '_ \ / _` |/ _ \ '__|
/\__/ / (_) | |_) | | |   | | | | | (_| |  __/ |
\____/ \___/|_.__/  \_|   |_|_| |_|\__,_|\___|_|

Made By: Hackware Bro    
    """)
    data = take_user_data() 
    #Create request packet 
    html = get_webpage('https://www.timesjobs.com/candidate/job-search.html',data)
    complete_data = extract_data(html)
    job_links = []
    
    with open('job_listing.txt','w') as f:
        for ind , entry in enumerate(complete_data):
            entry_txt = f"""
{ind + 1}.
Job Name : {Fore.BLACK}{Back.WHITE} {entry['job']}{Fore.RESET}{Back.RESET}
Company name : {entry['company']}
Key-Skills Required : {Back.MAGENTA} {entry['skills']}{Fore.RESET}{Back.RESET}
Location : {entry['location']}
Visit the website for more info : {entry['link']}
            """
            f.write(entry_txt) #Write into file 
            print(entry_txt)   #shows the output at the same time
            job_links.append(entry['link']) 
    print(f'{Fore.YELLOW}{Back.RED}Your current job listing has been written on the file as well!{Fore.RESET}{Back.RESET}')
    while True:
        try:
            link_no = int(input('\nType job no to get more info about it (Only press enter to close): '))
            if not link_no in range(1,len(job_links)+1):    #if integer is not in the range to close the program
                break
            webbrowser.open(job_links[link_no-1])
        except Exception:   #when gives other than integer to quit program
            print(f'Thanks for using this!\nFollow {Fore.MAGENTA}{Back.WHITE}HackwareBro{Fore.RESET}{Back.RESET} for more informative material')
            break