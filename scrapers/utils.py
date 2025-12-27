"""
Utility data and functions for the scrapers folder.

Constants:
    GIR_REWRITE: dict[str, str]
    TIMESLOTS: int
    DAYS: dict[str, int]
    TIMES: dict[str, int]
    EVE_TIMES: dict[str, int]
    Term: enum.EnumType

Functions:
    find_timeslot(day, slot, pm)
    zip_strict(*iterables)
    grouper(iterable, n)
    get_term_info(sem_term)
    url_name_to_term(url_name)
"""

from __future__ import annotations

import json
import os.path
from enum import Enum
from itertools import zip_longest
from typing import Any, Generator, Iterable, Literal, Tuple, TypedDict, TypeVar

GIR_REWRITE = {
    "GIR:CAL1": "Calculus I (GIR)",
    "GIR:CAL2": "Calculus II (GIR)",
    "GIR:PHY1": "Physics I (GIR)",
    "GIR:PHY2": "Physics II (GIR)",
    "GIR:CHEM": "Chemistry (GIR)",
    "GIR:BIOL": "Biology (GIR)",
}

TIMESLOTS = 34

DAYS = {
    "M": 0,
    "T": TIMESLOTS,
    "W": TIMESLOTS * 2,
    "R": TIMESLOTS * 3,
    "F": TIMESLOTS * 4,
}

TIMES = {
    "6": 0,
    "6.30": 1,
    "7": 2,
    "7.30": 3,
    "8": 4,
    "8.30": 5,
    "9": 6,
    "9.30": 7,
    "10": 8,
    "10.30": 9,
    "11": 10,
    "11.30": 11,
    "12": 12,
    "12.30": 13,
    "1": 14,
    "1.30": 15,
    "2": 16,
    "2.30": 17,
    "3": 18,
    "3.30": 19,
    "4": 20,
    "4.30": 21,
    "5": 22,
    "5.30": 23,
}

EVE_TIMES = {
    "12": 12,
    "12.30": 13,
    "1": 14,
    "1.30": 15,
    "2": 16,
    "2.30": 17,
    "3": 18,
    "3.30": 19,
    "4": 20,
    "4.30": 21,
    "5": 22,
    "5.30": 23,
    "6": 24,
    "6.30": 25,
    "7": 26,
    "7.30": 27,
    "8": 28,
    "8.30": 29,
    "9": 30,
    "9.30": 31,
    "10": 32,
    "10.30": 33,
}

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


class Term(Enum):
    """Terms for the academic year."""

    FA = "fall"
    JA = "IAP"
    SP = "spring"
    SU = "summer"


class CourseData(TypedDict):
    """Metadata about a particular class."""

    nonext: bool
    repeat: bool
    url: str
    final: bool
    half: int | bool
    limited: bool
    new: bool


class QuarterInfo(TypedDict, total=False):
    """Information about the quarter in which a course is offered."""

    start: tuple[int, int]
    end: tuple[int, int]


class Attributes(TypedDict):
    """Information about a course's primary attributes, for filtering."""

    hass: list[Literal["H", "A", "S", "E"]]
    comms: Literal["", "CI-H", "CI-HW"]
    gir: Literal[
        "", "BIOL", "CAL1", "CAL2", "CHEM", "LAB", "LAB2", "PHY1", "PHY2", "REST"
    ]


class ScheduleInfo(TypedDict, total=False):
    """Information about a course's schedule."""

    tba: bool
    sectionKinds: list[str]
    lectureRawSections: list[str]
    recitationRawSections: list[str]
    labRawSections: list[str]
    designRawSections: list[str]
    lectureSections: list[tuple[list[tuple[int, int]], str]]
    recitationSections: list[tuple[list[tuple[int, int]], str]]
    labSections: list[tuple[list[tuple[int, int]], str]]
    designSections: list[tuple[list[tuple[int, int]], str]]


class FireroadRawData(TypedDict, total=False):
    """Raw output data from Fireroad about a course."""

    subject_id: str
    title: str
    description: str
    instructors: list[str]
    virtual_status: str
    lecture_units: int
    lab_units: int
    preparation_units: int
    level: int
    is_variable_units: bool
    joint_subjects: list[str]
    meets_with_subjects: list[str]
    quarter_information: str
    hass_attribute: str
    communication_requirement: Literal["CI-H", "CI-HW"]
    gir_attribute: Literal[
        "BIOL", "CAL1", "CAL2", "CHEM", "LAB", "LAB2", "PHY1", "PHY2", "REST"
    ]
    offered_fall: bool
    offered_IAP: bool
    offered_spring: bool
    offered_summer: bool
    prerequisites: str
    schedule: str
    schedule_fall: str
    schedule_IAP: str
    schedule_spring: str
    old_id: str
    rating: float
    in_class_hours: float
    out_of_class_hours: float
    enrollment_number: int


class FireroadCourseDict(TypedDict, total=False):
    """Processed output data from Fireroad about a course."""

    number: str
    course: str
    subject: str
    terms: list[str]
    prereqs: str
    tba: bool
    sectionKinds: list[str]
    lectureSections: list[tuple[list[tuple[int, int]], str]]
    recitationSections: list[tuple[list[tuple[int, int]], str]]
    labSections: list[tuple[list[tuple[int, int]], str]]
    designSections: list[tuple[list[tuple[int, int]], str]]
    lectureRawSections: list[str]
    recitationRawSections: list[str]
    labRawSections: list[str]
    designRawSections: list[str]
    hass: list[Literal["H", "A", "S", "E"]]
    comms: Literal["", "CI-H", "CI-HW"]
    gir: Literal[
        "", "BIOL", "CAL1", "CAL2", "CHEM", "LAB", "LAB2", "PHY1", "PHY2", "REST"
    ]
    lectureUnits: int
    labUnits: int
    preparationUnits: int
    level: int
    isVariableUnits: bool
    same: str
    meets: str
    quarterInfo: QuarterInfo
    oldNumber: str
    rating: float
    hours: float
    size: int
    description: str
    name: str
    inCharge: str
    virtualStatus: bool


def find_timeslot(day: str, slot: str, is_slot_pm: bool) -> int:
    """
    Finds the numeric code for a timeslot.

    >>> find_timeslot("W", "11.30", False)
    79

    Args:
        day (str): The day of the timeslot
        slot (str): The time of the timeslot
        is_slot_pm (bool): Whether the timeslot is in the evening

    Raises:
        ValueError: If no matching timeslot could be found.

    Returns:
        int: A numeric code for the timeslot
    """
    time_dict = EVE_TIMES if is_slot_pm else TIMES
    if day not in DAYS or slot not in time_dict:  # error handling!
        raise ValueError(f"Invalid timeslot {day}, {slot}, {is_slot_pm}")
    return DAYS[day] + time_dict[slot]


_T = TypeVar("_T")


def zip_strict(*iterables: Iterable[_T]) -> Generator[Tuple[_T, ...], Any, None]:
    """
    Helper function for grouper.
    Groups values of the iterator on the same iteration together.

    Raises:
        ValueError: If iterables have different lengths.

    Yields:
        Tuple[Any, ...]: A generator, which you can iterate over.
    """
    sentinel = object()
    for group in zip_longest(*iterables, fillvalue=sentinel):
        if any(sentinel is t for t in group):
            raise ValueError("Iterables have different lengths")
        yield group  # type: ignore


def grouper(
    iterable: Iterable[_T], group_size: int
) -> Generator[Tuple[_T, ...], Any, None]:
    """
    Groups items of the iterable in equally spaced blocks of group_size items.
    If the iterable's length ISN'T a multiple of group_size, you'll get a
    ValueError on the last iteration.

    >>> list(grouper("ABCDEFGHI", 3))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I')]

    From https://docs.python.org/3/library/itertools.html#itertools-recipes.

    Args:
        iterable (Iterable[Any]): an iterator
        group_size (int): The size of the groups

    Returns:
        Generator[Tuple[Any, ...], Any, None]:
            The result of the grouping, which you can iterate over.
    """
    args = [iter(iterable)] * group_size
    return zip_strict(*args)


def get_term_info(sem_term: Literal["sem", "presem"]) -> dict[str, Any]:
    """
    Gets the latest term info from "../public/latestTerm.json" as a dictionary.
    If sem_term = "sem", looks at semester term (fall/spring).
    If sem_term = "presem", looks at pre-semester term (summer/IAP)

    Args:
        is_semester_term (Literal["sem", "presem"]): whether to look at the semester
            or the pre-semester term.

    Returns:
        Dict[str, Any]: the term info for the selected term from latestTerm.json.
    """
    fname = os.path.join(os.path.dirname(__file__), "../public/latestTerm.json")
    with open(fname, encoding="utf-8") as latest_term_file:
        term_info = json.load(latest_term_file)

    if sem_term == "sem":
        return term_info["semester"]
    return term_info["preSemester"]


def url_name_to_term(url_name: str) -> Term:
    """
    Extract the term (without academic year) from a urlName.

    >>> url_name_to_term("f24")
    <Term.FA: 'fall'>

    Args:
        url_name (string): a urlName representing a term, as found in latestTerm.json.

    Raises:
        ValueError: If the url_name does not start with a valid term character.

    Returns:
        Term: the enum value corresponding to the current term (without academic year).
    """
    if url_name[0] == "f":
        return Term.FA
    if url_name[0] == "i":
        return Term.JA
    if url_name[0] == "s":
        return Term.SP
    if url_name[0] == "m":
        return Term.SU

    raise ValueError(f"Invalid term {url_name[0]}")
