import math
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from tools.geometric_tools import get_alpha_for_distance_on_circle, get_vector_angle, get_2d_vector_from_polar, \
    get_2d_distance


def get_position_on_circle_base_on_travel_time(self, d_ta_arrive, new_position, settings):
    distance = settings["v_of_uav"] * d_ta_arrive
    alpha = get_alpha_for_distance_on_circle(settings["tier1_distance_from_intruder"], distance)
    uav_current_alpha = get_vector_angle(self.position)
    new_alpha = alpha + uav_current_alpha
    new_position = get_2d_vector_from_polar(new_alpha, settings["tier1_distance_from_intruder"])
    return new_position

def get_time_to_reach_point_in_streinght_line(position, target,settings):
    distance=float(get_2d_distance(position,target))
    time=distance/settings["v_of_uav"]
    return time





def get_d_t_arrive_poison(settings):
    d_ta_arrive=0
    if (settings.arrive_deterministic):
        d_ta_arrive = 1.0 / settings.lambda1
    else:
        d_ta_arrive = 1.0 / settings.lambda1* math.log(2, math.e)
    return d_ta_arrive
