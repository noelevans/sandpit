from bookings.models import Booking, Address, Car, Driver, Customer
from django.contrib  import admin

class BookingAdmin( admin.ModelAdmin ):
    def queryset(self, request):
        qs = super(BookingAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

admin.site.register( Booking )
admin.site.register( Address )
admin.site.register( Car )
admin.site.register( Driver )
admin.site.register( Customer )
