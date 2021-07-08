import typing

from Enums import UavStatus
from GameObjects import Uav
from GameState import GameState
from Map.FluidCel import FluidCell
from events import Event_list, Move_along
from tools.geometric_tools import get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line


def plan_move_attakc(game_state:GameState,settings,event_list:Event_list,uav:Uav,path:typing.List[FluidCell]):
    target_position=path[1].position
    dt_arrive=get_time_to_reach_point_in_streinght_line(target_position,uav.position,settings.v_of_uav)
    event_time=dt_arrive+game_state.t_curr
    new_event=Move_along(event_time,target_position,uav,UavStatus.ON_ATTACK,game_state.t_curr)
    event_list.append_event(new_event,uav,UavStatus.ON_ATTACK)
