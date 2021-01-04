drop database food_rescuer;
create database food_rescuer;

use food_rescuer;

create table Location(
    id int auto_increment primary key,
    longitude float,
    latitude float
);

create table Donator(
    id int not null primary key,
    user_name varchar(50),
    location_id int,
    donation_count int,
    donation_level float,

    foreign key(location_id) references Location(id)
);

create table Receiver(
    id int not null primary key,
    location_id int,

    foreign key(location_id) references Location(id)
);

create table Food(
    id int auto_increment primary key,
    donator_id int,
    location_id int,
    available boolean,
    number_of_servings int,
    expiration_date float,
    description varchar(200),

    foreign key(donator_id) references Donator(id),
    foreign key(location_id) references Location(id)
);

create table Type(
    id int auto_increment primary key,
    name varchar(20)
);

create table Food_types(
    id int auto_increment primary key,
    type_id int,
    food_id int,

    foreign key(type_id) references Type(id),
    foreign key(food_id) references Food(id)
);

create table Receiver_types(
    id int auto_increment primary key,
    type_id int,
    receiver_id int,

    foreign key(type_id) references Type(id),
    foreign key(receiver_id) references Receiver(id)
);

create table photo(
    id int auto_increment primary key,
    path varchar(150)
);

create table food_photos(
    id int auto_increment primary key,
    food_id int,
    photo_id int,

    foreign key(food_id) references food(id),
    foreign key(photo_id) references photo(id)
);


INSERT INTO Type VALUES(null, 'Halal');
INSERT INTO Type VALUES(null, 'Kosher');
INSERT INTO Type VALUES(null, 'Vegetarian');
INSERT INTO Type VALUES(null, 'Vegan');
INSERT INTO Type VALUES(null, 'Animals');
INSERT INTO Type VALUES(null, 'Other');