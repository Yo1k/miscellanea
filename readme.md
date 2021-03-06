# Miscellanea

<p align="right">
  <a href="https://docs.python.org/3.9/">
    <img src="https://img.shields.io/badge/Python-3.9-FFE873.svg?labelColor=4B8BBE"
        alt="Python requirement">
  </a>
</p>

## About

The module with done tasks is located in `./yo1k/misc/` and has a name `miscellanea.py`.
There is a module with tests in that directory too: `test_misc.py`.
To run `test_misc.py` be sure that you have installed `pytest` module and name package `yo1k` is 
added to the python path. File `requirements.txt` contains used python dependencies in the project.

Running `miscellanea.py` as main will execute examples described in test tasks.

### Task_1
**part_1** Use function `get_idx_frst_zero(array)` to find index of the first zero in a string 
sequence (array) of some ones and zeros.
Example: `get_idx_frst_zero("111111111110000000000000000")` return `11`.

**part_2** Use function `is_rect_intersecting(x1,y1,x2,y2,x3,y3,x4,y4)` to check if two 
rectangles intersect and function `intersection_area(x1,y1,x2,y2,x3,y3,x4,y4)` to find 
intersection area of two rectangles.

### Task_2
Use function `gather_animal_name_stats()` to gather a number of animals per letter of the RU 
alphabet in wikipedia and return it as a dictionary object. It can take up to 1 min to gather 
the needed information.
Use `gather_animal_name_stats(print_as_you_go=True)` to print gathered stats (letter of the 
alphabet and the total number of animal names beginning with that letter) in process.

### Task_3
Use function `appearance(intervals)` to find total intersection time of three lists of 
intervals: 'lesson', 'tutor', 'pupil'.

