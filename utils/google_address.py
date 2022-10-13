
from addresses.models import Address


API_KEY = 'AIzaSyA9Jnj8xt9IH_B_Jvken_vmpAb_dc_tuwo'

def get_google_address(data):

    street = data["street"].replace(" ", "+")
    city = data["city"].replace(" ", "+")

    ADDRESS= f'{data["number"]}+{street},{city},{data["state"]}'
  
    return f'https://maps.googleapis.com/maps/api/staticmap?center={ADDRESS}&zoom=15&size=300x200&markers=color:red%7C{ADDRESS}&key={API_KEY}'

