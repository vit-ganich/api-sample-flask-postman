from datetime import datetime
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Data to serve with our API
BATTLESHIPS = {
    "Mikasa": {
        "name": "Mikasa",
        "country": "Japan",
        "caliber": 12,
        "guns": 4,
        "timestamp": get_timestamp()
    },
    "Borodino": {
        "name": "Borodino",
        "country": "Russian Empire",
        "caliber": 12,
        "guns": 4,
        "timestamp": get_timestamp()
    },
    "Warspite": {
        "name": "Warspite",
        "country": "British Empire",
        "caliber": 13.8,
        "guns": 8,
        "timestamp": get_timestamp()
    }
}


def read_all():
    """
    This function responds to a request for /api/battleships
    with the complete lists of ships

    :return:       json string of battleships
    """
    return [BATTLESHIPS[key] for key in sorted(BATTLESHIPS.keys())]


def read_one(name):
    """
    This function responds to a request for /api/battleships/{name}
    with one matching ship from battleships

    :param name:   name of ship to find
    :return:       ship matching name
    """
    if name in BATTLESHIPS:
        ship = BATTLESHIPS.get(name)
    else:
        abort(
            404,
            "Battleship with name {name} not found".format(name=name)
        )

    return ship


def create(ship):
    """
    Creates a new ship in the battleships structure
    based on the passed in ship data
    :param ship:  ship to create
    :return:        201 on success, 406 on ship exists
    """

    name = ship.get("name", None)
    country = ship.get("country", None)
    caliber = ship.get("caliber", None)
    guns = ship.get("guns", None)

    if name not in BATTLESHIPS and name is not None:
        BATTLESHIPS[name] = {
            "name": name,
            "country": country,
            "caliber": caliber,
            "guns": guns,
            "timestamp": get_timestamp(),
        }

        return make_response(
            "Battleship with name '{name}' successfully created".format(name=name), 201
        )

    else:
        abort(
            406,
            "Battleship with name '{name}' already exists".format(name=name)
        )


def update(name, battleship):
    """
    Updates an existing ship in the battleships structure
    :param name:   name of ship to update in the battleships structure
    :param battleship:  battleship to update
    :return:        updated battleship structure
    """
    if name not in BATTLESHIPS:
        abort(
            404,
            "Battleship with name '{name}' not found".format(name=name)
        )
    else:
        update_ship_keys(name, battleship)
        BATTLESHIPS[name]["timestamp"] = get_timestamp()

        return make_response(
            "Battleship with name '{name}' successfully updated".format(name=name), 200
        )


def update_ship_keys(name, battleship):
    for key in ("name", "country", "caliber", "guns"):
        value = battleship.get(key, None)
        if value:
            BATTLESHIPS[name][key] = value


def delete(name):
    """
    Deletes a ship from the battleships structure
    :param name:   name of ship to delete
    :return:        200 on successful delete, 404 if not found
    """

    if name in BATTLESHIPS:
        del BATTLESHIPS[name]
        return make_response(
            "{name} successfully deleted".format(name=name), 200
        )

    else:
        abort(
            404,
            "Battleship with name {name} not found".format(name=name)
        )
