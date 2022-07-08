import urllib.request
import urllib.error
from collections import defaultdict
from collections.abc import Sequence
from html.parser import HTMLParser
from time import sleep
from typing import Optional


def get_idx_frst_zero(array: str) -> Optional[int]:
    """Finds index of the first zero in a string sequence of some ones and zeros.

    A string sequence has strict structure: firstly there can be only ones in the sequence
    and then only zeros in the sequence can follow. Sequence has elements.
    Border conditions:
    if a sequence does not contain zeros, then return value is None;
    if a sequence contains only zeros, then return value is 0.
    """
    size: int = len(array)
    assert size != 0, f"`array` is empty: {array}"

    def _get_null_idx(_array: str, begin: int, end: int) -> Optional[int]:
        if end - begin == 0:
            if _array[begin] == "0":
                return 0
            else:
                return None

        median_idx: int = begin + (end - begin) // 2
        if _array[median_idx] == "1" and _array[median_idx + 1] == "0":
            return median_idx + 1
        elif _array[median_idx] == "1" and _array[median_idx + 1] == "1":
            return _get_null_idx(_array, median_idx + 1, end)
        elif _array[median_idx] == "0":
            return _get_null_idx(_array, begin, median_idx)
        else:
            assert False

    return _get_null_idx(array, 0, size - 1)


def is_rect_intersecting(
        x1: float, y1: float,
        x2: float, y2: float,
        x3: float, y3: float,
        x4: float, y4: float
) -> bool:
    """Checks if two rectangles intersect.

    x1, y1, x2, y2 correspond to opposite coordinates of vertices of the first rectangle
    and x3, y3, x4, y4 correspond to the second one.
    Sides of rectangles are parallel to the coordinate axes
    and rectangles are not degenerate (side length is not zero).
    Opposite coordinates of vertices are not ordered: xi, yi vertex (i is index) can be
    left or right (top or bottom) vertex in a particular rectangle.
    The condition when the rectangles have common borders is not considered as an intersection.
    """
    assert x1 != x2 and y1 != y2, f"Rectangle is degenerate: x1={x1}, x2={x2}, y1={y1}, y2={y2}"
    assert x3 != x4 and y3 != y4, f"Rectangle is degenerate: x3={x3}, x4={x4}, y3={y3}, y4={y4}"
    if max(x1, x2) < min(x3, x4) or min(x1, x2) > max(x3, x4):
        return False
    elif max(y1, y2) < min(y3, y4) or min(y1, y2) > max(y3, y4):
        return False
    else:
        return True


def intersection_area(
        x1: float, y1: float,
        x2: float, y2: float,
        x3: float, y3: float,
        x4: float, y4: float
) -> float:
    """Finds intersection area of two rectangles.

    The intersection area of two non-intersecting rectangles is 0. For a detailed description,
    see `is_rect_intersecting()`.
    """
    if not is_rect_intersecting(x1, y1, x2, y2, x3, y3, x4, y4):
        return 0
    else:
        x_sorted: list[float] = [x1, x2, x3, x4]
        x_sorted.sort()
        y_sorted: list[float] = [y1, y2, y3, y4]
        y_sorted.sort()
        x_intersection = x_sorted[2] - x_sorted[1]
        y_intersection = y_sorted[2] - y_sorted[1]
        return x_intersection * y_intersection


class AnimalsHTMLParser(HTMLParser):
    """Gathers stats from RU wikipedia page about animals.

    Counts number of animals per letter of the alphabet for the specific wiki page and saves this
    information in `stats` attribute.
    Finds url to the next wiki page and saves it in `next_page_url_part`.
    Parser gathers information until the end of a wiki page
    or until it encounters the specific letter (the latin letter 'A' in the case to gather stats for
    the whole RU alphabet).

    Class constructor takes parameter `print_as_you_go` which is `False` by default.
    If set value `True` for this parameter, then `AnimalsHTMLParser` instance will print
    gathered stats (letter of the alphabet and the total number of animal names beginning with
    that letter) while running.
    """

    def __init__(self, print_as_you_go: bool = False):
        super().__init__()
        self.print_as_you_go: bool = print_as_you_go
        self.tag_stack: list[str] = []
        self.name_letter: str = "uninitialised"
        self.stats: dict[str, int] = defaultdict(int)
        self.attrs_stack: list[list[tuple[str, Optional[str]]]] = []
        self.page_end = False
        self.next_page_url_part: str = "uninitialised"
        self.run: bool = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag == "div" and ("class", "mw-category mw-category-columns") in attrs:
            assert len(self.tag_stack) == 0, f"tag_stack={self.tag_stack}"
            self.tag_stack.append("div1")

        elif (
                tag == "div"
                and ("class", "mw-category-group") in attrs
                and self.tag_stack
                and self.tag_stack[-1] == "div1"
        ):
            self.tag_stack.append("div2")

        elif (
                tag == "h3"
                and self.run
                and self.tag_stack
                and self.tag_stack[-1] == "div2"
        ):
            self.tag_stack.append("h3")

        elif (
                tag == "li"
                and self.tag_stack
                and self.tag_stack[-1] == "div2"
        ):
            if self.name_letter != "uninitialised":
                self.stats[self.name_letter] += 1

        elif tag == "a" and self.page_end:
            self.tag_stack.append("a")
            self.attrs_stack.append(attrs)

    def handle_endtag(self, tag: str) -> None:
        if (
                tag == "h3"
                and self.tag_stack
                and self.tag_stack[-1] == "h3"
        ):
            self.tag_stack.pop()

        elif (
                tag == "div"
                and self.tag_stack
                and self.tag_stack[-1] == "div2"):
            self.tag_stack.pop()

        elif (
                tag == "div"
                and self.tag_stack
                and self.tag_stack[-1] == "div1"):
            self.tag_stack.pop()
            self.page_end = True

        elif (
                tag == "a"
                and self.tag_stack
                and self.tag_stack[-1] == "a"):
            self.tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if self.tag_stack and self.tag_stack[-1] == "h3":
            if data == "A":
                self.run = False
                if self.print_as_you_go:
                    self.print_stats()
            else:
                if self.print_as_you_go:
                    if self.name_letter != "uninitialised" and data != self.name_letter:
                        self.print_stats()
                self.name_letter = data

        elif self.tag_stack and self.tag_stack[-1] == "a":
            if data == "Следующая страница":
                self.next_page_url_part = self.attrs_stack.pop()[0][1]
                self.page_end = False
            else:
                self.attrs_stack.pop()

    def print_stats(self) -> None:
        print(f"{self.name_letter}: {self.stats[self.name_letter]}")


def get_html(url: str) -> str:
    attempt: int = 2
    while attempt > 0:
        try:
            with urllib.request.urlopen(url=url) as response:
                html: str = response.read().decode("utf-8")
            return html
        except urllib.error.URLError as e:
            attempt -= 1
            if attempt == 0:
                raise e
            sleep(1)


def gather_animal_name_stats(print_as_you_go: bool = False) -> dict[str, int]:
    """Gathers a number of animals per letter of the RU alphabet and return it as a dictionary.

    To gather information it uses RU wiki pages. It creates object of `AnimalsHTMLParser` class
    which do the main job (in more details see `AnimalsHTMLParser` docs).

    The function takes parameter `print_as_you_go` which is `False` by default.
    If set value `True` for this parameter, then gathered stats will be printed while
    function execution.
    """
    start_url: str = (
            "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F%3A%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90"
    )
    url_prefix: str = "https://ru.wikipedia.org"
    parser = AnimalsHTMLParser(print_as_you_go)

    url: str = start_url
    while parser.run:
        parser.feed(data=get_html(url))
        assert len(parser.tag_stack) == 0, f"parser.tag_stack={parser.tag_stack}"
        url = url_prefix + parser.next_page_url_part
    return parser.stats


def appearance(intervals: dict[str, list[int]]) -> int:
    """Finds total intersection time of three lists of intervals: 'lesson', 'tutor', 'pupil'.

    Takes as a parameter dictionary of three intervals lists for corresponding keys 'lesson',
    'tutor', 'pupil'. Each list consists of even number of timestamps elements in seconds:
    for 'lesson' they are start and end of the lesson;
    for 'tutor', 'pupil' they are timestamps of entrance and exit to the lesson. That is all
    lists are ordered by ascending.
    """
    lesson: list[int] = intervals["lesson"]
    tutor: list[int] = intervals["tutor"]
    pupil: list[int] = intervals["pupil"]

    assert len(lesson) % 2 == 0, f"`lesson` has odd number of elements: {len(lesson)}"
    assert len(tutor) % 2 == 0, f"`tutor` has odd number of elements: {len(tutor)}"
    assert len(pupil) % 2 == 0, f"`pupil` has odd number of elements: {len(pupil)}"
    assert lesson == sorted(lesson), f"`lesson` is unsorted: {lesson}"
    assert tutor == sorted(tutor), f"`tutor` is unsorted: {tutor}"
    assert pupil == sorted(pupil), f"`pupil` is unsorted: {pupil}"

    total_intersection: list[int] = (
            intersected_intervals(intersected_intervals(lesson, tutor), pupil)
    )
    return sum_intervals(total_intersection)


def sum_intervals(seq: Sequence[int]) -> int:
    """Return total sum of intervals from a timestamps list."""
    total: int = 0
    for i in range(len(seq) // 2):
        total += (seq[2 * i + 1] - seq[2 * i])
    return total


def intersected_intervals(lst1: list[int], lst2: list[int]) -> list[int]:
    """Returns a list of timestamps of intervals intersection from two lists of intervals.

    Accepted lists have to be ordered by ascending of timestamps of intervals and have an even
    number of elements.

    """
    result: list[int] = []
    i = j = 0
    len1 = len(lst1) // 2
    len2 = len(lst2) // 2
    while i < len1 and j < len2:
        left = max(lst1[2 * i], lst2[2 * j])
        right = min(lst1[2 * i + 1], lst2[2 * j + 1])
        if left <= right:
            result.extend([left, right])
        if lst1[2 * i + 1] < lst2[2 * j + 1]:
            i += 1
        else:
            j += 1
    return result


if __name__ == "__main__":
    # Task_1
    # 1st task part
    idx_frst_zero = get_idx_frst_zero("111111111110000000000000000")
    print(f"get_idx_frst_zero('111111111110000000000000000') = {idx_frst_zero} \n")

    # 2nd task part
    two_rectangle_vert = [1, 1, 2, 2, 3, 3, 4, 4]
    intersect = is_rect_intersecting(*two_rectangle_vert)
    area = intersection_area(*two_rectangle_vert)
    print(f"Rectangles {two_rectangle_vert} are intersecting: {intersect}, "
          f"intersection area = {area} \n")

    # Task_2
    print("Number of animals per letter of the RU alphabet:")
    gather_animal_name_stats(print_as_you_go=True)
    # [print(f"{k}: {v}") for k, v in gather_animal_name_stats().items()]

    # Task_3
    tests = [
            {'data': {'lesson': [1594663200, 1594666800],
                      'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396,
                                1594666472],
                      'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
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
            #                     1594706524, 1594706579, 1594706641],
            #           'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149,
            #                     1594706463]},
            #  'answer': 3577
            #  },
            {'data': {'lesson': [1594692000, 1594695600],
                      'pupil': [1594692033, 1594696347],
                      'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
             'answer': 3565
             },
    ]

    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test[
            'answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
