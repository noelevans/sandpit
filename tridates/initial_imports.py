from django.contrib.auth.models import User
#from descriptions.models        import Description
from disciplines.models         import Discipline
from events.models              import Event
from regions.models             import Region

l1 = Region.objects.create(name='London')
Region.objects.create(name='Midlands')
Region.objects.create(name='North East')
Region.objects.create(name='North West')
Region.objects.create(name='Scotland')
Region.objects.create(name='South West')
Region.objects.create(name='South East')
Region.objects.create(name='Wales')

e1 = Event(name="Mazda Triathlon")
e1.start_date = "2011-08-08"
e1.duration = 2
e1.region = Region.objects.all()[0]
e1.date_added = "2010-10-10"
e1.added_by = User.objects.all()[0]
e1.confirmed_by = User.objects.all()[0]
e1.date_confirmed = "2010-10-10"
e1.locked = False
e1.status = "Individual entrant & charity positions"
e1.save()

Discipline.objects.create(name="Super sprint", description="0.4 x 10 x 2.5 km")
d2 = Discipline.objects.create(name="Sprint", description="0.75 x 20 x 5 km")
d1 = Discipline.objects.create(name="Olympic", description="1.5 x 40 x 10 km")
Discipline.objects.create(name="Olympic plus", description="1.5 x 80 x 10 km")
Discipline.objects.create(name="Half-Ironman", description="1.93 x 90 x 21.09 km")
Discipline.objects.create(name="Full-Ironman", description="3.86 x 180 x 42.2 km")

e1.disciplines.add(d1)
e1.disciplines.add(d2)

e2 = Event(name="Dextro Energy Triathlon London")
e2.start_date = "2011-08-06"
e2.duration = 2
e2.region = Region.objects.all()[0]
e2.date_added = "2010-11-06"
e2.added_by = User.objects.all()[0]
#e2.confirmed_by = User.objects.all()[0]
#e2.date_confirmed = "2010-10-10"
e2.locked = False
e2.status = "Individual entrant & charity positions"
e2.save()

User.objects.create_user(username='lalayn', email='lalaynbaluch@hotmail.co.uk', password='e1pk')

