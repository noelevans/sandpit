from django.db import models

help_text="Please use the following format: <em>YYYY-MM-DD</em>"

class Address(models.Model):
	first_line = models.CharField(max_length=64)
	second_line = models.CharField(max_length=64, blank=True)
	city = models.CharField(max_length=32, blank=True)
	postcode = models.CharField(max_length=8, blank=True)

	def __unicode__(self):
		return self.first_line + ' ' + self.second_line + ' (' + self.postcode + ')'


class Car(models.Model):
	registration_plate = models.CharField(max_length=32, blank=True)
	make = models.CharField(max_length=32)
	model = models.CharField(max_length=32)
	colour = models.CharField(max_length=32)
	desc = models.CharField(max_length=512, blank=True)

	def __unicode__(self):
		return self.make + ', ' + self.model + ' (' + self.registration_plate + ')'


class Driver(models.Model):
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	phone_number = models.IntegerField()
	car = models.ForeignKey(Car)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name


class Customer(models.Model):
	first_name = models.CharField(max_length=32, blank=True)
	last_name = models.CharField(max_length=32, blank=True)
	phone_number = models.IntegerField()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name


class Booking(models.Model):
	pickup_address = models.ForeignKey(Address, related_name='booking_pickup')
	drop_off_address = models.ForeignKey(Address, related_name='booking_drop_off')
	customer = models.ForeignKey(Customer)
	order_received = models.DateTimeField(editable=False, auto_now=True)
	collection_time = models.DateTimeField(blank=True, help_text=help_text)
	no_passengers = models.IntegerField(blank=True)
	baggage_or_instructions = models.CharField(max_length=512, blank=True)
	driver = models.ForeignKey(Driver)
	confirmationSent = models.BooleanField(editable=False)
	price = models.DecimalField(blank=True, decimal_places=2, max_digits=8)

	def __unicode__(self):
		return self.pickup_address.first_line + ' to ' + self.drop_off_address.first_line
