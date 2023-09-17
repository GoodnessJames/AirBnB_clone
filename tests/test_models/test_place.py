#!/usr/bin/python3
"""Defines unittests for place_objace.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place_obj))
        self.assertNotIn("city_id", place_obj.__dict__)

    def test_user_id_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place_obj))
        self.assertNotIn("user_id", place_obj.__dict__)

    def test_name_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place_obj))
        self.assertNotIn("name", place_obj.__dict__)

    def test_description_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place_obj))
        self.assertNotIn("desctiption", place_obj.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place_obj))
        self.assertNotIn("number_rooms", place_obj.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place_obj))
        self.assertNotIn("number_bathrooms", place_obj.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place_obj))
        self.assertNotIn("max_guest", place_obj.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place_obj))
        self.assertNotIn("price_by_night", place_obj.__dict__)

    def test_latitude_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place_obj))
        self.assertNotIn("latitude", place_obj.__dict__)

    def test_longitude_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place_obj))
        self.assertNotIn("longitude", place_obj.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        place_obj = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place_obj))
        self.assertNotIn("amenity_ids", place_obj.__dict__)

    def test_two_places_unique_ids(self):
        place_obj1 = Place()
        place_obj2 = Place()
        self.assertNotEqual(place_obj1.id, place_obj2.id)

    def test_two_places_different_created_at(self):
        place_obj1 = Place()
        sleep(0.05)
        place_obj2 = Place()
        self.assertLess(place_obj1.created_at, place_obj2.created_at)

    def test_two_places_different_updated_at(self):
        place_obj1 = Place()
        sleep(0.05)
        place_obj2 = Place()
        self.assertLess(place_obj1.updated_at, place_obj2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place_obj = Place()
        place_obj.id = "123456"
        place_obj.created_at = place_obj.updated_at = dt
        place_objstr = place_obj.__str__()
        self.assertIn("[Place] (123456)", place_objstr)
        self.assertIn("'id': '123456'", place_objstr)
        self.assertIn("'created_at': " + dt_repr, place_objstr)
        self.assertIn("'updated_at': " + dt_repr, place_objstr)

    def test_args_unused(self):
        place_obj = Place(None)
        self.assertNotIn(None, place_obj.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place_obj = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place_obj.id, "345")
        self.assertEqual(place_obj.created_at, dt)
        self.assertEqual(place_obj.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        place_obj = Place()
        sleep(0.05)
        first_updated_at = place_obj.updated_at
        place_obj.save()
        self.assertLess(first_updated_at, place_obj.updated_at)

    def test_two_saves(self):
        place_obj = Place()
        sleep(0.05)
        first_updated_at = place_obj.updated_at
        place_obj.save()
        second_updated_at = place_obj.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place_obj.save()
        self.assertLess(second_updated_at, place_obj.updated_at)

    def test_save_with_arg(self):
        place_obj = Place()
        with self.assertRaises(TypeError):
            place_obj.save(None)

    def test_save_updates_file(self):
        place_obj = Place()
        place_obj.save()
        place_objid = "Place." + place_obj.id
        with open("file.json", "r") as f:
            self.assertIn(place_objid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        place_obj = Place()
        self.assertIn("id", place_obj.to_dict())
        self.assertIn("created_at", place_obj.to_dict())
        self.assertIn("updated_at", place_obj.to_dict())
        self.assertIn("__class__", place_obj.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place_obj = Place()
        place_obj_dict = place_obj.to_dict()
        self.assertEqual(str, type(place_obj_dict["id"]))
        self.assertEqual(str, type(place_obj_dict["created_at"]))
        self.assertEqual(str, type(place_obj_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        place_obj = Place()
        place_obj.id = "123456"
        place_obj.created_at = place_obj.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place_obj.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        place_obj = Place()
        with self.assertRaises(TypeError):
            place_obj.to_dict(None)


if __name__ == "__main__":
    unittest.main()
