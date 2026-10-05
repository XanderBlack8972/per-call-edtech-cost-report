from datetime import date

from edtech_cost import LearnerDeadline, _status


def test_deadline_decision_prioritizes_completion_then_due_date() -> None:
    today = date(2026, 9, 10)
    assert _status(LearnerDeadline("A", "Course", date(2026, 9, 1), 10, 10), today) == "complete"
    assert _status(LearnerDeadline("B", "Course", date(2026, 9, 1), 4, 10), today) == "overdue"
    assert _status(LearnerDeadline("C", "Course", date(2026, 9, 20), 4, 10), today) == "on_track"
