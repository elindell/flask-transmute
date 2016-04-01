import flask_transmute
from decimal import Decimal
from flask import Flask
from flask_transmute.flask import FlaskRouteSet
from flask_transmute.swagger import Swagger
from flask_transmute.exceptions import NotFoundException, ApiException


# having an exception that is raised in
# a situation like this is valuable. this can help
# indicate to Transmute what is an expected exception
# based off of incorrect input, or a real error.
# former should raise this.
class DeckException(Exception):
    pass


class Card(object):

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    # transmute_schema is an attribute that helps flask_transmute
    # serialize and deserialize your object.
    #
    # transmute_schema is a modified json-schema: http://json-schema.org/
    # in contrast to using primitive types, you pass in classes for the
    # type definitions.
    transmute_schema = {
        "properties": {
            "name": {"type": str},
            "description": {"type": str},
            "price": {"type": Decimal}
        },
        "required": ["name", "description", "price"]
    }

    # if you want to be able to automatically populate fields
    # with the desired types, you must specify a from_dict method.
    # this is how flask-transmute will be able to convert a data
    # object to a class instance.
    @staticmethod
    def from_transmute_dict(model):
        return Card(**model)


class Deck(object):

    def __init__(self):
        self._cards = []

    # the update decorator tells
    # flask-transmute that this method will
    # modify data. adding updtate ensures
    # the request will be a POST
    @flask_transmute.updates
    @flask_transmute.annotate({"card": Card, "return": Card})
    def add_card(self, card):
        """ add a card to the deck """
        if len(card.name) > 100:
            raise DeckException(
                "the name is too long! must be under 100 characters."
            )
        self._cards += [card]
        return card

    @flask_transmute.annotate({"return": [Card]})
    def cards(self):
        """ retrieve all cards from the deck """
        return self._cards

    def reset(self):
        self._cards = []

app = Flask(__name__)
deck = Deck()

route_set = FlaskRouteSet()
route_set.route_object('/deck', deck,
                       # if exceptions are added to error_exceptions,
                       # they will be caught and raise a success: false
                       # response, with the error message being the message
                       # of the exception
                       error_exceptions=[DeckException])


def raise_401():
    raise ApiException("", status_code=401)

route_set.route_function("/raise_401", raise_401)


def raise_404():
    raise NotFoundException()

route_set.route_function("/raise_404", raise_404)

swagger = Swagger("myApi", "1.0")
# route_set.add_extension(swagger)

route_set.init_app(app)
swagger.init_app(app)

app.debug = True
