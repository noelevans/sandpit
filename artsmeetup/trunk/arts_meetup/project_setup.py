import re
from datetime                   import datetime
from datetime                   import date
from django.contrib.auth.models import User
from users.models               import *
from tags.models                import *
from booking.models             import *
from messaging.models           import *
from blog.models                import *
from django.db.models           import Q
from links.models               import *

u0 = User.objects.create_user("noel", "noelevans@gmail.com", "[e1pk]")
u1 = User.objects.create_user("lalayn", "lalayn@thestage.co.uk", "east")
u2 = User.objects.create_user("brian", "brian@thestage.co.uk", "east")
u3 = User.objects.create_user("waja", "waja@empire.com", "east")

u0.is_staff=True
u0.is_superuser=True

u0.save()
u1.save()
u2.save()
u3.save()

p0              = Profile()
p0.user         = User.objects.get(username='noel')
p0.first_name   = 'Noel'
p0.last_name    = 'Evans'
p0.city         = 'London'
p0.sex          = 'M'


p1              = Profile()
p1.user         = u1
p1.first_name   = "Lalayn"
p1.last_name    = "Baluch"
p1.city         = 'London'
p1.sex          = 'F'

p2              = Profile()
p2.user         = u2
p2.first_name   = "Brian"
p2.last_name    = "McCheese"
p2.city         = 'London'
p2.sex          = 'M'

p3              = Profile()
p3.user         = u3
p3.first_name   = "Waja"
p3.last_name    = "Baluch"
p3.city         = 'London'
p3.sex          = 'M'

p0.save()
p1.save()
p2.save()
p3.save()

v1                 = Profile()
v1.type            = Profile.VENUE
v1.name            = "tricycle"
v1.org_name        = "Tricycle"
v1.address_line_1  = "276 Kilburn High Road"
v1.city            = "London"
v1.producing       = False
v1.recieving       = True
v1.save()
v1.contact.add(u1.get_profile())

v2                 = Profile()
v2.type            = Profile.VENUE
v2.name            = "bearandstaff"
v2.org_name        = "Bear and Staff"
v2.address_line_1  = "13 Oval Road"
v2.city            = "London"
v2.producing       = True
v2.recieving       = True
v2.save()
v2.contact.add(u3.get_profile())

r1 = RoleTag(name='ballerina')
r2 = RoleTag(name='actor', description='Sexually ambiguous')
r3 = RoleTag(name='trombonist', description='Long arm collective')
r4 = RoleTag(name='castingdirector')
r5 = RoleTag(name='actress', description='Definitely a lady')
r6 = RoleTag(name='director')
r7 = RoleTag(name='producer')

r1.save()
r2.save()
r3.save()
r4.save()
r5.save()
r6.save()
r7.save()

vt1 = VenueTag(name='receiving_works')
vt2 = VenueTag(name='producing_works')
vt3 = VenueTag(name='want_new_directions')

vt1.save()
vt2.save()
vt3.save()

gt1 = GroupTag(name='need_more_ppl')
gt2 = GroupTag(name='search_for_venue')

gt1.save()
gt2.save()

b0 = Booking(start=date(2009, 1, 01), end=date(2009, 3, 1), name='Fishing', location = "Nice peaceful lake somewhere")
b0.more = "Down through the dark waters he catches the Whale"
b0.profile = p0
b0.save()

b1 = Booking(start=date(2007, 1, 1), end=date(2007, 9, 1), name='Trout tickling')
b1.profile = p0
b1.save()

b2 = Booking(start=date(2011, 1, 1), end=date(2011, 9, 1), name='Hallibut heckling')
b2.profile = p0
b2.save()

b20 = Booking(start=date(2006, 1, 5), end=date(2009, 3, 5), name='Appointment')
b20.profile = p1
b20.save()

interests1 = OtherTag(name="shakespeare")
interests1.save()

interests2 = OtherTag(name="comedyplays")
interests2.save()

interests3 = OtherTag(name="physicaltheatre")
interests3.save()

mess1 = Message()
mess1.sender = u0.get_profile()
mess1.body = "Hello My Love, how are you this bird-chirpingly lovely morning?"
mess1.save()
mess1.recipient.add(u1.get_profile())
mess1.make_copies()

mess2 = Message()
mess2.sender = u0.get_profile()
mess2.body = "Ello my chinas. Any Captain Kirk doing?"
mess2.save()
mess2.recipient.add(u1.get_profile())
mess2.recipient.add(u2.get_profile())
mess2.recipient.add(u3.get_profile())
mess2.make_copies()

post1 = Post(author=u0.get_profile())
post1.body="I hope terpsicle will one day be as big as the shaquille o'neal"
post1.save()

