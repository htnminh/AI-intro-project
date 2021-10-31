# TODO: Test Coordinate and new methods
# -----------------------------------------------------------------------------

from AI_intro_project.Game import Road, Coordinate

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
