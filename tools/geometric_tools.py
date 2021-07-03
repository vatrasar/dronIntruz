import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import math
from random import Random


import numpy as np

from GameObjects.Point import Point


def get_2d_vector_from_polar(angle,distance):
	x=distance*np.cos(angle)
	y=distance*np.sin(angle)

	return [x,y]

def get_alpha_for_distance_on_circle(r,distance):
	alpha=2*3.14*distance/(2*3.14*r)
	return alpha

def convert_to_360(angle):
	if(angle<0):
		angle=2*3.14+angle
	return angle

def get_postion_when_origin_is_central_point(orginal_position:Point,new_central:Point):
	new_point=Point(orginal_position.x-new_central.x,orginal_position.y-new_central.y)
	return new_point



def get_2d_distance(source, position):
	x_target=position.x
	y_target=position.y
	x_source=source.x
	y_source=source.y


	p1 = np.array([x_target, y_target])
	p2 = np.array([x_source, y_source])

	squared_dist = np.sum((p1 - p2) ** 2, axis=0)
	dist = np.sqrt(squared_dist)

	return dist


def rotate_vector(vector,angle):
	new_x=math.cos(angle)*vector[0]-math.sin(angle)*vector[1]
	new_y=math.sin(angle)*vector[0]+math.cos(angle)*vector[1]
	return (new_x,new_y)

def get_vector_angle(vector):
	vector_2=[vector.x,vector.y]
	vector_1=[1,0]
	unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
	unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
	dot_product = np.dot(unit_vector_1, unit_vector_2)
	det_produtcst=np.cross(unit_vector_1,unit_vector_2)
	angle = np.arctan2(det_produtcst,dot_product)
	return angle

def dec_to_rad(angle):
	return (3.14/180)*angle

def get_random_position(rand:Random, gameState,settings):
	intruder_position=gameState.intruder.position
	polar_angle=rand.random()*360
	polar_angle=dec_to_rad(polar_angle)
	x,y=get_2d_vector_from_polar(polar_angle,settings.tier1_distance_from_intruder)
	new_position=Point(x,y)
	return new_position


def get_transform_between_points(source, target):
	transform = (target.x - source.x, target.y - source.y)

	return transform


def get_vector_with_length_and_direction(drone_move_max_speed,direction_vector):
	sum_of_squares=direction_vector[0]**2+direction_vector[1]**2
	scale_factor=drone_move_max_speed/math.sqrt(sum_of_squares)
	result_vector=[direction_vector[0],direction_vector[1]]
	result_vector[0]=result_vector[0]*scale_factor
	result_vector[1]=result_vector[1]*scale_factor

	return result_vector