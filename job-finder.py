import requests,os

#Global vars

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

if __name__=='__main__':
    data = take_user_data()
    #Create request packet 
    input_values = {
        'searchType':'personalizedSearch',
        'from':'submit',
        'txtKeywords': data['jobs'],
        'txtLocation': data['location'],
        "cboWorkExp1": data['exp']
    }
    response = requests.get('https://www.timesjobs.com/candidate/job-search.html',params=input_values)