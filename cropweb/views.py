from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd
# Create your views here.
from django.contrib.auth import logout

from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout
    return redirect('home')
class UserRegisterView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is authenticated, log them in.
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')  # Redirect to the home page or any desired URL after login
        else:
            messages.error(request, 'Login failed. Please check your credentials.')
    
    return redirect('home')  # Redirect to the home page or any desired URL after login
def home(request):
    signupform=SignUpForm
    
    return render(request,'home.html',{'signupform':signupform})


def predictcrop(request):
    crop_type=    {0: 'monsoon ', 1: 'winter ', 2: 'summer', 3: 'whole year'}

    crop_data={0: 'apple',
    1: 'arecanut',
    2: 'ashgourd',
    3: 'banana',
    4: 'barley',
    5: 'beetroot',
    6: 'bittergourd',
    7: 'blackgram',
    8: 'blackpepper',
    9: 'bottlegourd',
    10: 'brinjal',
    11: 'cabbage',
    12: 'cardamom',
    13: 'carrot',
    14: 'cashewnuts',
    15: 'cauliflower',
    16: 'coffee',
    17: 'coriander',
    18: 'cotton',
    19: 'cucumber',
    20: 'drumstick',
    21: 'garlic',
    22: 'ginger',
    23: 'grapes',
    24: 'horsegram',
    25: 'jackfruit',
    26: 'jowar',
    27: 'jute',
    28: 'ladyfinger',
    29: 'maize',
    30: 'mango',
    31: 'moong',
    32: 'onion',
    33: 'orange',
    34: 'papaya',
    35: 'pineapple',
    36: 'pomegranate',
    37: 'potato',
    38: 'pumpkin',
    39: 'radish',
    40: 'ragi',
    41: 'rapeseed',
    42: 'rice',
    43: 'ridgegourd',
    44: 'sesamum',
    45: 'soyabean',
    46: 'sunflower',
    47: 'sweetpotato',
    48: 'tapioca',
    49: 'tomato',
    50: 'turmeric',
    51: 'watermelon',
    52: 'wheat'}


    state = {
        0: 'Andaman and Nicobar',
        1: 'Andhra Pradesh',
        2: 'Arunachal Pradesh',
        3: 'Assam',
        4: 'Bihar',
        5: 'Chandigarh',
        6: 'Chhattisgarh',
        7: 'Dadra and Nagar Haveli',
        8: 'Goa',
        9: 'Gujarat',
        10: 'Haryana',
        11: 'Himachal Pradesh',
        12: 'Jammu and Kashmir',
        13: 'Jharkhand',
        14: 'Karnataka',
        15: 'Kerala',
        16: 'Madhya Pradesh',
        17: 'Maharashtra',
        18: 'Manipur',
        19: 'Meghalaya',
        20: 'Mizoram',
        21: 'Nagaland',
        22: 'Odisha',
        23: 'Puducherry',
        24: 'Punjab',
        25: 'Rajasthan',
        26: 'Sikkim',
        27: 'Tamil Nadu',
        28: 'Telangana',
        29: 'Tripura',
        30: 'Uttar Pradesh',
        31: 'Uttarakhand',
        32: 'West Bengal'
    }
    if request.method == 'POST':
        # Retrieve form data from the POST request
        temperature = request.POST.get('temperature')
        nitrogen_ratio = request.POST.get('nitrogen_ratio')
        phosphorous_ratio = request.POST.get('phosphorous_ratio')
        potassium_ratio = request.POST.get('potassium_ratio')
        ph_value = request.POST.get('ph_value')
        rainfall = request.POST.get('rainfall')
        crop_type1 = request.POST.get('crop_type')
        state1 = request.POST.get('state')
        df=pd.read_csv('cropvalue.csv')
        stateee=state.get(int(state1))
        print("heyyyyyyyyyyyyivgdgqwdgvwqjhqwjdbjqwgu",stateee)
        state_row = df[df['state'] == stateee]
        print(state_row)
        print("Hey")
        if not state_row.empty:
            print("i am in")
            tmin, tmax = state_row['tmin'].values[0], state_row['tmax'].values[0]
            nmin, nmax = state_row['nmin'].values[0], state_row['nmax'].values[0]
            pomin, pomax = state_row['pomin'].values[0], state_row['pomax'].values[0]
            phmin, phmax = state_row['phmin'].values[0], state_row['phmax'].values[0]
            phomin, phomax = state_row['phomin'].values[0], state_row['phomax'].values[0]
            print(potassium_ratio)
            print(tmax)
            if(float(tmin) >=float(temperature) or float(temperature) >= float(tmax)):
                mess="Temperature value is not in range"
                mess_bool=True
                return render(request,'croppredict.html',{'state':state,'crop_type':crop_type,'mess':mess,'mess_bool':mess_bool})
            
            if(float(nmin) >= float(nitrogen_ratio) or float(nitrogen_ratio)   >= float(nmax)):
                mess="Nitrogen value is not in range"
                mess_bool=True
                return render(request,'croppredict.html',{'state':state,'crop_type':crop_type,'mess':mess,'mess_bool':mess_bool})
            if( int(potassium_ratio) >= int(pomax) or int(pomin) >= int(potassium_ratio)):
                mess="Potassium value is not in range"
                mess_bool=True
                print("heyyyyyyyyyy",crop_type)
                return render(request,'croppredict.html',{'state':state,'crop_type':crop_type,'mess':mess,'mess_bool':mess_bool})
            if(float(phmin) >= float(ph_value) or float(ph_value) >= float(phmax)):
                mess="Ph-value is not in range"
                mess_bool=True
                return render(request,'croppredict.html',{'state':state,'crop_type':crop_type,'mess':mess,'mess_bool':mess_bool})
            if(float(phomin) >= float(phosphorous_ratio) or float(phosphorous_ratio) >= float(phomax)):
                mess="Phosphorous ratio is not in range"
                mess_bool=True
                return render(request,'croppredict.html',{'state':state,'crop_type':crop_type,'mess':mess,'mess_bool':mess_bool})
        print(state)
        print(crop_type)
        data=[]
        data.append(int(nitrogen_ratio))
        data.append(int(phosphorous_ratio))
        data.append(int(potassium_ratio))
        data.append(float(ph_value))
        data.append(float(rainfall))
        data.append(float(temperature))
        data.append(int(state1))
        data.append(int(crop_type1))
        print(data)

        loaded_model = pickle.load(open("crop_classifier_model.pkl", 'rb'))
        data1=np.array(data)
        data = data1.reshape(1,-1)
    
        predictions = loaded_model.predict( data)
        print(predictions)
        print(crop_data[predictions[0]])
        return render(request,'predicted_crop.html',{'predict_crop':crop_data[predictions[0]]})
    mess_bool=False
    return render(request,'croppredict.html',{'state':state,'crop_type':crop_type,'mess_bool':mess_bool})