import pymysql
from config import DB_PASSWORD
from FoodTypes import *
from location import Location

connection = pymysql.connect(
    host='localhost',
    user='root',
    password=DB_PASSWORD,
    db='food_rescuer',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def add_donator(cursor, args, table_name):
    donator = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in donator.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in donator.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new donator", e)


def add_receiver(cursor, args, table_name):
    receiver = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in receiver.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in receiver.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new receiver", e)


def add_location(cursor, args, table_name):
    location = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in location.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in location.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new location", e)


def add_photo(cursor, args, table_name):
    photo = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in photo.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in photo.values())
        print(columns, values, "PHOTO")
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new photo", e)


def add_food_photos(cursor, args, table_name):
    photo = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in photo.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in photo.values())
        print(columns, values, "food photos")
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new photo", e)


def add_food(cursor, args, table_name):
    food = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in food.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in food.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new food", e)


def get_max_id(table_name):
    try:
        with connection.cursor() as cursor:
            query = f'select max(id) as id from {table_name} '
            cursor.execute(query)
            res = cursor.fetchall()
            return res[0]['id']
    except Exception as err:
        print("500 - Internal error", err)


def add_food_type(cursor, args, table_name):
    food_id = args[0]
    type = args[1]
    type_id = food_type.index(type) + 1
    obj = {'id': '0', 'type_id': type_id, 'food_id': food_id}
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in obj.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in obj.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new food type", e)


def add_receiver_food_type(cursor, args, table_name):
    receiver_id = args[0]
    type = args[1]
    type_id = food_type.index(type) + 1
    obj = {'id': '0', 'type_id': type_id, 'receiver_id': receiver_id}
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in obj.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in obj.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new receiver food type", e)


def get_location_by_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""
    query = "select * from location as l where l.id = " + str(id)
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res[0]


def get_receiver_by_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""
    query = "select * from receiver as r where r.id = " + str(id)
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res[0]


def get_photos_by_food_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""

    query = 'select * from photo as p join food_photos as pt ' \
            'on p.id = pt.photo_id ' \
            'where pt.food_id = ' + id
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return res

    return [val['path'] for val in res]


def get_donator_by_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""
    query = "select * from donator as d where d.id = " + str(id)
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res[0]


def process_foods_types(cursor, res):
    processed_res = {}
    for food in res:
        if food['id'] not in processed_res:
            food['food_types'] = [food['name']]
            del food['name']
            print(food['location_id'])
            location = get_location_by_id(cursor, (food['location_id'],))
            print("LOCATION", location)
            if location:
                location_obj = Location()
                location_obj.set_address(location['longitude'], location['latitude'])
                food['location'] = location_obj
            processed_res[food['id']] = food
        else:
            processed_res[food['id']]['food_types'].append(food['name'])

    return list(processed_res.values())


def get_foods_by_types(cursor, args):
    types = args[0]
    if len(types) == 0:
        query = 'select * from food as f join food_types as ft join type as t ' \
                'on f.id = ft.food_id and t.id = ft.type_id '
        cursor.execute(query)
        res = cursor.fetchall()
    else:
        types = ', '.join("'" + str(x).replace('/', '_') + "'" for x in tuple(types))
        query = 'select * from food as f join food_types as ft join type as t ' \
                'on f.id = ft.food_id and t.id = ft.type_id ' \
                'where t.name in (' + types + ') '
        cursor.execute(query)
        res = cursor.fetchall()

    return process_foods_types(cursor, res)


def get_receiver_food_types_by_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""
    query = "select * from receiver_types as rt join type as t on rt.type_id = t.id where rt.receiver_id = " + str(id)
    cursor.execute(query)
    res = cursor.fetchall()
    res = [val['name'] for val in res]

    return res


def delete_receiver_by_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""
    query = "delete from receiver as r where r.id = " + str(id)
    cursor.execute(query)
    connection.commit()


def delete_donator_by_id(cursor, args):
    id = "\"" + str(args[0]).replace('/', '_') + "\""
    query = "delete from donator as d where d.id = " + str(id)
    cursor.execute(query)
    connection.commit()


def main_db(action, *args):
    try:
        with connection.cursor() as cursor:
            if action == 'add_donator':
                add_donator(cursor, args, 'donator')
            elif action == 'add_receiver':
                receiver = args[0]
                food_types = receiver['food_types']
                del receiver['food_types']
                add_receiver(cursor, (receiver,), 'receiver')
                for type_ in food_types:
                    add_receiver_food_type(cursor, (receiver['id'], type_), 'receiver_types')
            elif action == 'add_location':
                add_location(cursor, args, 'location')
            elif action == 'add_food':
                food = args[0]
                food_types = food['food_types']
                del food['food_types']
                add_food(cursor, (food,), 'food')
                food_id = get_max_id('food')
                for type_ in food_types:
                    add_food_type(cursor, (food_id, type_), 'food_types')
            elif action == 'get_food_by_types':
                return get_foods_by_types(cursor, args)
            elif action == 'get_location_by_id':
                return get_location_by_id(cursor, args)
            elif action == 'get_receiver_by_id':
                return get_receiver_by_id(cursor, args)
            elif action == 'get_donator_by_id':
                return get_donator_by_id(cursor, args)
            elif action == 'get_receiver_food_types_by_id':
                return get_receiver_food_types_by_id(cursor, args)
            elif action == 'delete_receiver_by_id':
                delete_receiver_by_id(cursor, args)
            elif action == 'delete_donator_by_id':
                delete_donator_by_id(cursor, args)
            elif action == 'add_photo':
                add_photo(cursor, args, 'photo')
            elif action == 'add_food_photos':
                add_food_photos(cursor, args, 'food_photos')
            elif action == 'get_photos_by_food_id':
                return get_photos_by_food_id(cursor, args)
            else:
                print("Invalid option")
    except Exception as err:
        print("500 - Internal error", err)


if __name__ == '__main__':
    # main_db('add_location', {'id': '0', 'longitude': 34, 'latitude': 35})
    # main_db('add_location', {'id': '0', 'longitude': 35, 'latitude': 37})
    # main_db('add_location', {'id': '0', 'longitude': 36, 'latitude': 38})
    # main_db('add_location', {'id': '0', 'longitude': 37, 'latitude': 39})
    #
    # main_db('add_receiver', {'id': 1, 'location_id': 1, 'food_types': ['Halal', 'Other']})
    # main_db('add_receiver', {'id': 2, 'location_id': 3, 'food_types': ['Kosher', 'Vegan']})
    # main_db('add_receiver', {'id': 3, 'location_id': 2, 'food_types': ['Halal']})
    #
    # main_db('add_donator',
    #         {'id': 1, 'user_name': 'donator1', 'location_id': 4, 'donation_count': 1, 'donation_level': 0.5})
    #
    # main_db('add_food', {'id': '0', 'donator_id': 1, 'location_id': 1, 'available': 1,
    #                      'number_of_servings': 2, 'expiration_date': 3, 'description': 'blabla',
    #                      'food_types': ['Halal', 'Kosher', 'Other']})
    # main_db('add_food', {'id': '0', 'donator_id': 1, 'location_id': 2, 'available': 1,
    #                      'number_of_servings': 3, 'expiration_date': 2, 'description': 'blabla',
    #                      'food_types': ['Halal', 'Kosher', 'Other']})
    #
    # main_db('add_food', {'id': '0', 'donator_id': 1, 'location_id': 2, 'available': 1,
    #                      'number_of_servings': 3, 'expiration_date': 2, 'description': 'blabla',
    #                      'food_types': ['Vegan']})
    # res = main_db('get_food_by_types', ['Vegan'])
    # print(res, len(res))
    # print(main_db('get_location_by_id', 2))
    # print(main_db('get_receiver_food_types_by_id', 2))
    print(main_db('get_photos_by_food_id', 36))
