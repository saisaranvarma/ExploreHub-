from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from .models import *
from rest_framework import generics
from .serializers import *
from .forms import ExploreForm
from django.contrib import messages
import requests


class DestinationsCreateView(generics.ListCreateAPIView):
    queryset = Destinations.objects.all()
    serializer_class = exploreSerializers
    permission_classes = [AllowAny]


class DestinationsDetail(generics.RetrieveAPIView):
    queryset = Destinations.objects.all()
    serializer_class = exploreSerializers

class DestinationsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Destinations.objects.all()
    serializer_class = exploreSerializers

class DestinationsDelete(generics.DestroyAPIView):
    queryset = Destinations.objects.all()
    serializer_class = exploreSerializers

class DestinationsSearchView(generics.ListAPIView):
    queryset = Destinations.objects.all()
    serializer_class = exploreSerializers

    def get_queryset(self):
        name = self.kwargs.get('Name')
        return Destinations.objects.filter(Name__icontains=name)


def create_destination(request):
    if request.method == 'POST':
        form = ExploreForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/create/'

                # Prepare data and file for POST request
                data = {
                    "Name": request.POST['Name'],
                    "Weather": request.POST['Weather'],
                    "State": request.POST['State'],
                    "District": request.POST['District'],
                    "Google_Maps_Link": request.POST['Google_Maps_Link'],
                    "Description": request.POST['Description'],
                }

                # Ensure the 'explore_img' key exists in request.FILES
                if 'explore_img' in request.FILES:
                    response = requests.post(api_url, data=data, files={'explore_img': request.FILES['explore_img']})

                    if response.status_code in [200, 201]:
                        messages.success(request, 'Destination inserted successfully')
                    else:
                        messages.error(request, f'Error {response.status_code}: {response.text}')
                else:
                    messages.error(request, 'Image file is missing.')

            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')

            finally:
                # Redirect to home page regardless of the outcome
                return redirect('/')

        else:
            messages.error(request, 'Form is invalid')

    else:
        form = ExploreForm()

    return render(request, 'create-destination.html', {'form': form})

def update_destination(request, id):
    # Fetch existing data when it's a GET request
    if request.method == 'GET':
        api_url = f'http://127.0.0.1:8000/detail/{id}/'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()  # Fetch existing data
            description = data['Description'].split('.')  # Split the description if needed
            weather_choices = Destinations.CHOICES
            return render(request, 'destination_update.html', {'Destination': data, 'Description': description,'weather_choices': weather_choices})
        else:
            messages.error(request, f'Error fetching details: {response.status_code}')
            return redirect('/')

    # Handle form submission when it's a POST request
    elif request.method == 'POST':
        name = request.POST['Name']
        weather = request.POST['Weather']
        state = request.POST['State']
        district = request.POST['District']
        links = request.POST['Google_Maps_Link']
        description = request.POST['Description']

        print('Image Url:', request.FILES.get('explore_img'))

        api_url = f'http://127.0.0.1:8000/update/{id}/'

        data = {
            "Name": name,
            "Weather": weather,
            "State": state,
            "District": district,
            "Google_Maps_Link": links,
            "Description": description,
        }

        files = {'explore_img': request.FILES.get('explore_img')} if request.FILES.get('explore_img') else None

        try:
            response = requests.put(api_url, data=data, files=files)
            if response.status_code == 200:
                messages.success(request, 'Destination updated successfully')
                return redirect('/')
            else:
                messages.error(request, f'Error updating data: {response.status_code}')
        except requests.RequestException as e:
            messages.error(request, f'Error during API request: {str(e)}')

    return render(request, 'destination_update.html')



def index(request):
    if request.method == 'POST':
        search = request.POST['search']
        api_url = f'http://127.0.0.1:8000/search/{search}/'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
            else:
                data = None
        except requests.exceptions.RequestException as e:
            data = None
            print(f"Error during API request: {str(e)}")

        return render(request, 'index.html', {'data': data})

    else:
        api_url = 'http://127.0.0.1:8000/create/'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                paginator = Paginator(data, 4)

                try:
                    page = int(request.GET.get('page', 1))
                except:
                    page = 1

                try:
                    recipes = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    recipes = paginator.page(paginator.num_pages)

                context = {
                    'recipes': recipes
                }

                return render(request, 'index.html', context)

            else:
                return render(request, 'index.html', {'error_message': f'Error:{response.status_code}'})

        except requests.exceptions.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error:{str(e)}'})


def destination_fetch(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        description_parts = data['Description'].split('.')  # Split the description into parts
        return render(request, "destination-fetch.html", {'destination': data, "description_parts": description_parts})

    # Return empty or error page if not found or error in API call
    return render(request, 'destination-fetch.html', {'error_message': 'Destination not found'})


def destination_delete(request, id):
    api_url = f'http://127.0.0.1:8000/delete/{id}'

    response = requests.delete(api_url)

    if response.status_code == 200:
        print(f'Destination with id {id} has been deleted')
    else:
        print(f'Failed to delete the destination. Status code: {response.status_code}')

    return redirect('/')  # Redirect to the homepage or list of destinations








