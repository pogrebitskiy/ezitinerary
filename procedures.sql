-- Creates a travel group
drop procedure if exists create_group;

delimiter //
CREATE PROCEDURE create_group
(
	IN group_name_param VARCHAR(255)
)

BEGIN 
	INSERT IGNORE INTO travel_group (group_name)VALUES
    (group_name_param);
END //

delimiter ;


-- Adds a member to the member table
drop procedure if exists add_member;

delimiter //
create procedure add_member
(
	in member_name_param varchar(255),
    in dob_param DATE,
    in email_param varchar(255)
)
BEGIN 
	INSERT IGNORE INTO `member`(name, birthdate, email) VALUES
    (member_name_param, dob_param, emaiL_param);
    
END //

delimiter ;

-- Ads a member to a group and the member table if not already exists
drop procedure if exists add_member_to_group;

delimiter //
create procedure add_member_to_group
(
	IN member_name_param VARCHAR(255),
    IN dob_param DATE,
    IN group_name_param VARCHAR(255)
)
BEGIN
	INSERT IGNORE INTO member_in_group (travel_group_id, member_id) VALUES
    ((SELECT travel_group_id FROM travel_group WHERE group_name_param = group_name),
    (SELECT member_id FROM member WHERE name = member_name_param AND birthdate = dob_param));
END //

delimiter ;

-- Removes a member from the member table
drop procedure if exists remove_member;

delimiter //
CREATE PROCEDURE remove_member
(
	in member_name_param VARCHAR(255),
    in dob_param DATE
)
BEGIN 
	DELETE FROM `member` WHERE member_name_param = name AND dob_param = birthdate;
END //

delimiter ;

-- Removes a member from a group
drop procedure if exists remove_member_from_group;

delimiter //
CREATE PROCEDURE remove_member_from_group
(
	IN member_name_param VARCHAR(255),
    IN dob_param DATE,
    IN group_name_param VARCHAR(255)
)
BEGIN 
	DELETE IGNORE FROM member_in_group WHERE member_id = (SELECT member_id FROM `member` WHERE name = member_name_param AND birthdate = dob_param)
		AND travel_group_id = (SELECT travel_group_id FROM travel_group WHERE group_name = group_name_param);
END //

delimiter ;


-- Deletes a group from the travel_group table and and removes all associated members
drop procedure if exists delete_group;

delimiter //
CREATE PROCEDURE delete_group
(
	IN travel_group_name_param VARCHAR(255)
)
BEGIN
	DELETE IGNORE FROM travel_group WHERE travel_group_name_param = group_name;
END //

delimiter ;


-- shows all the members in groups and their associated groups
drop procedure if exists view_groups;

delimiter //
CREATE PROCEDURE view_groups()

BEGIN
	SELECT travel_group_id, group_name, m.member_id, m.name, m.birthdate, m.email  FROM travel_group t JOIN member_in_group mg USING (travel_group_id)
								JOIN `member` m USING (member_id)
	ORDER BY travel_group_id;
END //

delimiter ;


-- Shows all the members of the selected group name
drop procedure if exists view_group_members;

delimiter //
CREATE PROCEDURE view_group_members
(
	IN group_name_param VARCHAR(255)
)
BEGIN
	SELECT * FROM `member` WHERE member_id IN
		(SELECT member_id FROM member_in_group
        WHERE travel_group_id =
			(SELECT travel_group_id FROM travel_group
            WHERE group_name = group_name_param));
END //

delimiter ;

-- Creates a trip in the trip table
drop procedure if exists create_trip;

delimiter //
CREATE PROCEDURE create_trip
(
	IN group_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255),
    IN start_date_param DATE,
    IN end_date_param DATE
)
BEGIN 
	INSERT INTO trip (name) VALUES
    (trip_name_param);
    INSERT INTO taking(trip_id, travel_group_id, start_date, end_date) VALUES
	(	(SELECT trip_id FROM trip WHERE name = trip_name_param),
		(SELECT travel_group_id FROM travel_group
        WHERE group_name = group_name_param),
        start_date_param, end_date_param
	);
END //

delimiter ;

-- Deletes a trip from the trip table
DROP PROCEDURE IF EXISTS delete_trip;

delimiter //
CREATE PROCEDURE delete_trip
(
	IN trip_name_param VARCHAR(255)
)
BEGIN
	DELETE IGNORE FROM trip WHERE trip_name_param = trip.name;
END //

delimiter ;

-- Adds a restaurant to a given trip
drop procedure if exists add_restaurant;

delimiter //
CREATE PROCEDURE add_restaurant
(
	IN restaurant_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255)
)
BEGIN 
	INSERT INTO trip_has_restaurant (trip_id, restaurant_id) VALUES
    ((SELECT trip_id FROM trip WHERE trip.name = trip_name_param), (SELECT restaurant_id FROM restaurant WHERE restaurant.name = restaurant_name_param));
END //

delimiter ;

-- Adds an excursion to a given trip
DROP PROCEDURE IF EXISTS add_excursion;

delimiter //
CREATE PROCEDURE add_excursion
(
	IN excursion_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255)
)
BEGIN 
	INSERT INTO trip_has_excursion (trip_id, excursion_id) VALUES
    ((SELECT trip_id FROM trip WHERE trip.name = trip_name_param), (SELECT excursion_id FROM excursion WHERE excursion.name = excursion_name_param));
END //

delimiter ;

-- Adds a hotel to a given trip
DROP PROCEDURE IF EXISTS add_hotel;

delimiter //
CREATE PROCEDURE add_hotel
(
	IN hotel_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255)
)
BEGIN 
	INSERT INTO trip_has_hotel (trip_id, hotel_id) VALUES
    ((SELECT trip_id FROM trip WHERE trip.name = trip_name_param), (SELECT hotel_id FROM hotel WHERE hotel.name = hotel_name_param));
END //

delimiter ;

-- Removes a restaurant from a trip
DROP PROCEDURE IF EXISTS remove_restaurant;

delimiter //
CREATE PROCEDURE remove_restaurant
(
	IN restaurant_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255)
)
BEGIN
	DELETE FROM trip_has_restaurant
		WHERE trip_id = (SELECT trip_id FROM trip WHERE trip.name = trip_name_param)
			AND restaurant_id = (SELECT restaurant_id FROM restaurant WHERE restaurant.name = restaurant_name_param);
END //

delimiter ;

-- Removes an excursion from a trip
DROP PROCEDURE IF EXISTS remove_excursion;

delimiter //
CREATE PROCEDURE remove_excursion
(
	IN excursion_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255)
)
BEGIN
	DELETE FROM trip_has_excursion
		WHERE trip_id = (SELECT trip_id FROM trip WHERE trip.name = trip_name_param)
			AND excursion_id = (SELECT excursion_id FROM excursion WHERE excursion.name = excursion_name_param);
END //

delimiter ;

-- Removes a hotel from a trip
DROP PROCEDURE IF EXISTS remove_hotel;

delimiter //
CREATE PROCEDURE remove_hotel
(
	IN hotel_name_param VARCHAR(255),
    IN trip_name_param VARCHAR(255)
)
BEGIN
	DELETE FROM trip_has_hotel
		WHERE trip_id = (SELECT trip_id FROM trip WHERE trip.name = trip_name_param)
			AND hotel_id = (SELECT hotel_id FROM hotel WHERE hotel.name = hotel_name_param);
END //

delimiter ;


-- Shows restaurants in an inputted neighborhood
DROP PROCEDURE IF EXISTS search_restaurants;

delimiter //
CREATE PROCEDURE search_restaurants
(
	IN city_param VARCHAR(45)
)
BEGIN
	SELECT * FROM restaurant WHERE city LIKE city_param;
END //

delimiter ;

-- Shows excursions in an inputted neighborhood
DROP PROCEDURE IF EXISTS search_excursions;

delimiter //
CREATE PROCEDURE search_excursions
(
	IN neighborhood_param VARCHAR(45)
)
BEGIN
	SELECT * FROM excursion WHERE neighborhood LIKE neighborhood_param;
END //

delimiter ;

-- Shows hotels in an inputed neighborhood
DROP PROCEDURE IF EXISTS search_hotels;

delimiter //
CREATE PROCEDURE search_hotels
(
	IN city_param VARCHAR(45)
)
BEGIN
	SELECT * FROM hotel WHERE city LIKE city_param;
END //

delimiter ;

-- shows all the excursions in a given trip
DROP PROCEDURE IF EXISTS view_trip_excursions;

delimiter //
CREATE PROCEDURE view_trip_excursions
(
	IN trip_name_param VARCHAR(255)
)
BEGIN
	SELECT e.* 
    FROM excursion e JOIN trip_has_excursion USING (excursion_id)
					JOIN trip t USING (trip_id)
                    WHERE t.name LIKE trip_name_param;
                    
END //

delimiter ;

-- shows all the hotels added to a trip
DROP PROCEDURE IF EXISTS view_trip_hotels;

delimiter //
CREATE PROCEDURE view_trip_hotels
(
	IN trip_name_param VARCHAR(255)
)
BEGIN
	SELECT h.* 
    FROM hotel h JOIN trip_has_hotel USING (hotel_id)
					JOIN trip t USING (trip_id)
                    WHERE t.name LIKE trip_name_param;
                    
END //

delimiter ;

-- shows all the restaurants added to a trip
DROP PROCEDURE IF EXISTS view_trip_restaurants;

delimiter //
CREATE PROCEDURE view_trip_restaurants
(
	IN trip_name_param VARCHAR(255)
)
BEGIN
	SELECT r.* 
    FROM restaurant r JOIN trip_has_restaurant USING (restaurant_id)
					JOIN trip t USING (trip_id)
                    WHERE t.name LIKE trip_name_param;
                    
END //

delimiter ;
