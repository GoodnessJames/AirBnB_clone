#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent the Amenity class.

    Attribute:
        name (str): The name of the amenity.
    """
    name = ""
