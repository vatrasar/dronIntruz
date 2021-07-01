import math
import sys, os, inspect



currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from GameObjects.Point import Point
from tools.geometric_tools import get_alpha_for_distance_on_circle, get_vector_angle, get_2d_vector_from_polar, \
    get_2d_distance, get_transform_between_points


def get_position_on_circle_base_on_travel_time(uav, delta_time, settings):
    distance = settings.v_of_uav * delta_time
    alpha = get_alpha_for_distance_on_circle(settings.tier1_distance_from_intruder, distance)
    uav_current_alpha = get_vector_angle(uav.position)
    new_alpha = alpha + uav_current_alpha
    new_position = get_2d_vector_from_polar(new_alpha, settings.tier1_distance_from_intruder)
    new_position=Point(new_position[0],new_position[1])
    return new_position

def get_time_to_reach_point_in_streinght_line(position, target,velocity):
    distance=float(get_2d_distance(position,target))
    time=distance/velocity
    return time

# def get_get_position_base_on_travel_time(uav_position,target_position, delta_time, settings):
#     distance = settings["v_of_uav"] * delta_time
#     vector=get_transform_between_points(uav_position, target_position)
#
#     uav_current_alpha = get_vector_angle(uav.position)
#     new_alpha = alpha + uav_current_alpha
#     new_position = get_2d_vector_from_polar(new_alpha, settings["tier1_distance_from_intruder"])
#     return new_position



def get_d_t_arrive_poison(settings):
    d_ta_arrive=0
    if (settings.arrive_deterministic):
        d_ta_arrive = 1.0 / settings.lambda1
    else:
        d_ta_arrive = 1.0 / settings.lambda1* math.log(2, math.e)
    return d_ta_arrive


def get_move_point(velocity_vector, delta_time):
    result_pozition=Point(1,1)
    result_pozition.x=velocity_vector[0]*delta_time
    result_pozition.y=velocity_vector[1]*delta_time
    return result_pozition