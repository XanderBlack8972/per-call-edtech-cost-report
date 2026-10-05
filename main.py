from datetime import date

from edtech_cost import LearnerDeadline, summarize


def main() -> None:
    item = LearnerDeadline("Mina", "Algebra foundations", date(2026, 9, 20), 6, 10)
    report = summarize([item], today=date(2026, 9, 10))[0]
    print(f"{report.learner}: {report.status} - {report.report}")
    print(f"embedding cost: {report.embedding_cost_usd or 'header unavailable'}")
    print(f"report cost: {report.report_cost_usd or 'header unavailable'}")


if __name__ == "__main__":
    main()
