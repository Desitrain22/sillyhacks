from django.core.management.base import BaseCommand, CommandError
from dasite.models import Location
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv("dasite/taco_bell_coords.csv")
        print(df)
        for index, row in df.iterrows():
            location = Location(
                id=index,
                address=row["address"],
                longitude=row["long"],
                latitude=row["lat"],
            )
            location.save()