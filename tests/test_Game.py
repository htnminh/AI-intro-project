from AI_intro_project.Game import Road

# Initial variable used for testing
# Assuming board_size is (4, 4)
coord_rd = (2, 3)  # a totally-not-random coord
coord_ul = (1, 1)  # Up-Left aka. North-West
coord_dr = (3, 3)  # Down-Right aka. South-East
coord_ul_invalid = (0, 0)
coord_dr_invalid = (4, 4)


#
# TEST FOR CLASS: AI_intro_project.Game.Road()
#
def test_coordinate_end_calc():
    # test for near-edge coords
    assert Road(*(coord_ul + tuple('U'))).coordinate_end == (0, 1), \
        'Test coordinate_end_calc for (1, 1, U) did not return (0, 1)'

    assert Road(*(coord_ul + tuple('L'))).coordinate_end == (1, 0), \
        'Test coordinate_end_calc for (1, 1, L) did not return (0, 1)'

    assert Road(*(coord_dr + tuple('D'))).coordinate_end == (4, 3), \
        'Test coordinate_end_calc for (3, 3, D) did not return (4, 3)'

    assert Road(*(coord_dr + tuple('R'))).coordinate_end == (3, 4), \
        'Test coordinate_end_calc for (3, 3, R) did not return (3, 4)'

    # test for corner coords, these should return 'invalid'
    # TODO: impl invalid moves first in main game logic.
    assert 1 == 1


def test_eq():
    # told you that _rd is not random
    assert Road(*(coord_dr + tuple('U'))) == Road(*(coord_rd + tuple('D'))), \
        'Test Road(2, 3, D) == Road(3, 3, U) did not return True'

    assert Road(*(coord_ul + tuple('D'))) != Road(*((2, 2) + tuple('L'))), \
        'Test Road(1, 1, D) == Road(2, 2, L) did not return False'
