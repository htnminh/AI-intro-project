from AI_intro_project.Game import Road, Coordinate, State

# Initial variable used for testing
# Currently assuming board_size is (4, 4)
coord_rd = (2, 3)  # a totally-not-random coord
coord_ul = (1, 1)  # Up-Left aka. North-West
coord_dr = (3, 3)  # Down-Right aka. South-East
coord_ul_invalid = (-1, -1)
coord_dr_invalid = (5, 5)
board_size = (4, 4)


#
# TEST FOR CLASS: AI_intro_project.Game.Coordinate()
#
def test_coord_check_inside():
    # Check coords: 2x invalid & 1 valid
    assert not Coordinate(*coord_ul_invalid).check_inside(*board_size), \
        'test Coordinate(-1, -1).check_inside(4, 4) failed'

    assert not Coordinate(*coord_dr_invalid).check_inside(*board_size), \
        'test Coordinate(5, 5).check_inside(4, 4) failed'

    assert Coordinate(*coord_ul).check_inside(*board_size), \
        'test Coordinate(1, 1).check_inside(4, 4) failed'


def test_coord_eq():
    assert Coordinate(1, 1) == Coordinate(*coord_ul), \
        'test Coordinate.__eq__ for == failed'

    assert Coordinate(1, 1) != Coordinate(2, 1), \
        'test Coordinate.__eq__ for != failed'


#
# TEST FOR CLASS: AI_intro_project.Game.Road()
#
def test_road_coordinate_end_calc():
    # test for near-edge coords
    assert Road(*coord_ul, 'U').coordinate_end == Coordinate(0, 1), \
        'Test Road.coordinate_end_calc for (1, 1, U) did not return (0, 1)'

    assert Road(*coord_ul, 'L').coordinate_end == Coordinate(1, 0), \
        'Test Road.coordinate_end_calc for (1, 1, L) did not return (0, 1)'

    assert Road(*coord_dr, 'D').coordinate_end == Coordinate(4, 3), \
        'Test Road.coordinate_end_calc for (3, 3, D) did not return (4, 3)'

    assert Road(*coord_dr, 'R').coordinate_end == Coordinate(3, 4), \
        'Test Road.coordinate_end_calc for (3, 3, R) did not return (3, 4)'


def test_road_eq():
    # told you that _rd is not random
    assert Road(*coord_dr, 'U') == Road(*(coord_rd + tuple('D'))), \
        'Test Road(2, 3, D) == Road(3, 3, U) did not return True'

    assert Road(*coord_ul, 'D') != Road(2, 2, 'L'), \
        'Test Road(1, 1, D) == Road(2, 2, L) did not return False'


#
# TEST FOR CLASS: AI_intro_project.Game.State()
#
# TODO: full impl
def test_state_random_initialize():
    assert 1 == 1


# create fixed for-test variables for 4x4 board
var_test_state = State()
var_test_state.board_size = board_size
var_test_state.walked_roads = [
    Road(0, 0, 'R'),
    Road(0, 1, 'R')
]
var_test_state.current_pos = Coordinate(0, 2)
var_test_state.current_tax = 4


def test_state_check_not_duplicate_road():
    assert not var_test_state\
        .check_not_duplicate_road(Road(0, 2, 'L')), \
        'Test State.check_not_duplicate_road failed for duped path'

    assert var_test_state\
        .check_not_duplicate_road(Road(0, 2, 'R')), \
        'Test State.check_not_duplicate_road failed for free path'


def test_state_available_roads_calc():
    # order of check is R->, L<-, U^, Dv
    assert var_test_state.available_roads_calc() \
        == [Road(0, 2, 'R'), Road(0, 2, 'D')], \
        'Test State.available_roads_calc failed at pos = (0, 2)'

    # take Road(0, 2, D)
    var_test_state.walked_roads.append(Road(0, 2, 'D'))

    # TODO: convert normal tuple to Coordinate in Game.State.current_pos
    # var_test_state.current_pos = Road(0, 2, 'D').coordinate_end
    var_test_state.current_pos = Coordinate(1, 2)
    var_test_state.current_tax *= 2

    assert var_test_state.available_roads_calc() \
        == [Road(1, 2, 'R'), Road(1, 2, 'L'), Road(1, 2, 'D')], \
        'Test State.available_roads_calc failed at pos = (1, 2)'
