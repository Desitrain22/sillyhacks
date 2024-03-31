from .models import Location
import pandas as pd

def load_locations():
    df = pd.read_csv("dasite/taco_bell_coords.csv")
    for index, row in df.iterrows():
        location = Location(
            id=index,
            address=row["address"],
            longitude=row["long"],
            latitude=row["lat"],
        )
        location.save()
    
    print(Location.objects.all())

load_locations()