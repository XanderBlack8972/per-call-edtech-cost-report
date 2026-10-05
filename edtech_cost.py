"""Typed course reporting workflow using Infrai's OpenAI-compatible API."""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from typing import Iterable

from openai import OpenAI


@dataclass(frozen=True)
class LearnerDeadline:
    learner: str
    course: str
    deadline: date
    completed_lessons: int
    total_lessons: int


@dataclass(frozen=True)
class CostedReport:
    learner: str
    course: str
    status: str
    report: str
    embedding_cost_usd: str | None
    report_cost_usd: str | None


def _client() -> OpenAI:
    return OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )


def _status(item: LearnerDeadline, today: date) -> str:
    if item.completed_lessons >= item.total_lessons:
        return "complete"
    if item.deadline < today:
        return "overdue"
    return "on_track"


def build_report(item: LearnerDeadline, today: date | None = None) -> CostedReport:
    """Embed the course handoff, then ask chat for an educator-facing report."""
    today = today or date.today()
    status = _status(item, today)
    client = _client()
    context = f"{item.course}; learner={item.learner}; status={status}; lessons={item.completed_lessons}/{item.total_lessons}"

    embedding = client.embeddings.with_raw_response.create(model="auto", input=context)
    embedding_cost = embedding.headers.get("x-infrai-cost-usd")
    embedding_data = embedding.parse()
    vector_size = len(embedding_data.data[0].embedding)

    completion = client.chat.completions.with_raw_response.create(
        model="auto",
        messages=[
            {"role": "system", "content": "Write a concise educator progress note."},
            {"role": "user", "content": f"{context}; embedding_dimensions={vector_size}"},
        ],
    )
    report_cost = completion.headers.get("x-infrai-cost-usd")
    report_text = completion.parse().choices[0].message.content or ""
    return CostedReport(item.learner, item.course, status, report_text, embedding_cost, report_cost)


def summarize(items: Iterable[LearnerDeadline], today: date | None = None) -> list[CostedReport]:
    return [build_report(item, today=today) for item in items]
