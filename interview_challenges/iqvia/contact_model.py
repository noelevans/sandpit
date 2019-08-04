import os
import sys
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 

Base = declarative_base()

 
class Contact(Base):

    __tablename__ = 'contact'
    username = Column(String(128), primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    emails = relationship(
        'Email', 
        back_populates='contact',
        cascade='all, delete, delete-orphan')

    def to_dict(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'emails': [e.address for e in self.emails]
        }

 
class Email(Base):
    
    __tablename__ = 'email'
    address = Column(String(256), primary_key=True)
    contact_username = Column(String, ForeignKey('contact.username'))
    contact = relationship('Contact', back_populates='emails')

    def to_dict(self):
        return {
            'address': self.address,
            'contact': self.contact.username}

