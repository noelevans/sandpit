from bookings.models import Booking, Address, Car, Driver, Customer
from django.http  import HttpResponse

def index(request):
    return HttpResponse("Hello, world. Digital Bookings homepage. Now go to: <a>http://noelevans.webfactional.com/admin</a>")

