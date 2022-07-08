from collections.abc import Sequence
from typing import Any

import pytest
import yo1k.misc.miscellanea as misc


def test_idx_before_frst_zero() -> None:
    assert misc.get_idx_frst_zero("1") is None
    assert misc.get_idx_frst_zero("0") == 0
    assert misc.get_idx_frst_zero("00") == 0
    assert misc.get_idx_frst_zero("10") == 1
    assert misc.get_idx_frst_zero("11") is None
    assert misc.get_idx_frst_zero("11000") == 2
    # case from the task
    assert misc.get_idx_frst_zero("111111111110000000000000000") == 11


def test_is_rect_intersecting() -> None:
    # case from the task
    assert misc.is_rect_intersecting(1, 1, 2, 2, 3, 3, 4, 4) is False
    assert misc.is_rect_intersecting(1, 1, 4, 4, 2, 2, 3, 3) is True
    assert misc.is_rect_intersecting(2, 2, 3, 3, 1, 1, 4, 4) is True
    assert misc.is_rect_intersecting(1, 1, 2, 2, 3, 3, 1, 4) is False
    assert misc.is_rect_intersecting(1, 1, 2, 2, 3, 1, 1, 4) is True


def test_intersection_area() -> None:
    # case from the task
    assert misc.intersection_area(1, 1, 2, 2, 3, 3, 4, 4) == 0
    assert misc.intersection_area(1, 1, 4, 4, 2, 2, 3, 3) == 1
    assert misc.intersection_area(4, 4, 1, 1, 2, 2, 3, 3) == 1
    assert misc.intersection_area(1, 1, 4, 4, 3, 3, 5, 5) == 1


def test_sum_intervals() -> None:
    assert misc.sum_intervals([1, 2]) == 1
    assert misc.sum_intervals([1, 2, 5, 6]) == 2


@pytest.fixture(name="intervals")
def fixtures_intervals() -> Sequence[dict[str, Any]]:
    return [
            {"input_data": ([1, 25], [2, 4, 8, 24]), "expected": [2, 4, 8, 24]},
            {"input_data": ([1, 25], [0, 5, 7, 28]), "expected": [1, 5, 7, 25]},
            {"input_data": ([1, 25], [1, 5, 7, 25]), "expected": [1, 5, 7, 25]},
            {"input_data": ([1, 25], [0, 5, 7, 24]), "expected": [1, 5, 7, 24]},
            {"input_data": ([1, 25], [2, 5, 7, 28]), "expected": [2, 5, 7, 25]},
            {"input_data": ([0, 5, 7, 24], [2, 4, 8, 24]), "expected": [2, 4, 8, 24]}
    ]


def test_intersected_intervals(
        intervals: Sequence[dict[str, Any]]) -> None:
    for case in intervals:
        lst1, lst2 = case["input_data"]
        assert misc.intersected_intervals(lst1, lst2) == case["expected"]


# cases from the task
@pytest.fixture(name="tests")
def fixtures_tests() -> Sequence[dict[str, Any]]:
    return [
            {'data': {'lesson': [1_594_663_200, 1_594_666_800],
                      'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396,
                                1594666472],
                      'tutor': [1_594_663_290, 1_594_663_430, 1_594_663_443, 1_594_666_473]},
             'answer': 3117
             },

            # This test case is wrong. 'pupil' list is not ordered:
            # element 1_594_704_500 goes before 1_594_702_807.
            # However, even after 'pupil' list sorting 'answer' is wrong in the test case.

            # {'data': {'lesson': [1594702800, 1594706400],
            #           'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512,
            #                     1594704513, 1594704564, 1594705150, 1594704581, 1594704582,
            #                     1594704734, 1594705009, 1594705095, 1594705096, 1594705106,
            #                     1594706480, 1594705158, 1594705773, 1594705849, 1594706480,
            #                     1594706500, 1594706875, 1594706502, 1594706503, 1594706524,
            #                     1_594_706_524, 1_594_706_579, 1_594_706_641],
            #           'tutor': [1594700035, 1594700364, 1594702749, 1594705148,
            #                     1594705149,
            #                     1594706463]},
            #  'answer': 3577
            #  },
            {'data': {'lesson': [1594692000, 1594695600],
                      'pupil': [1594692033, 1594696347],
                      'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
             'answer': 3565
             },
    ]


# cases from the task
def test_appearance(tests: Sequence[dict[str, Any]]) -> None:
    for test in tests:
        assert misc.appearance(test["data"]) == test["answer"]


if __name__ == "__main__":
    pytest.main()
