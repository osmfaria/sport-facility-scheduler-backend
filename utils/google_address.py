import os


def get_google_address(data):
    KEY = os.environ.get("API_KEY")

    street = data["address1"].replace(" ", "+")
    city = data["city"].replace(" ", "+")

    ADDRESS= f'{street},{city},{data["state"]}'

    return f'https://maps.googleapis.com/maps/api/staticmap?center={ADDRESS}&zoom=15&size=300x200&markers=color:red%7C{ADDRESS}&key={KEY}'

