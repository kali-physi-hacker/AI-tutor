from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CodeRunRequest(BaseModel):
    language: str
    code: str
    tests: str | None = None


@router.post("/code-run")
async def code_run(_: CodeRunRequest):
    # Placeholder secure runner: intentionally not executing arbitrary code at MVP stage
    return {"stdout": "", "stderr": "", "results": {"executed": False, "reason": "disabled"}}


class QuizGenRequest(BaseModel):
    topic: str | None = None
    lesson_id: int | None = None
    count: int = 5
    difficulty: str = "medium"


@router.post("/quiz/generate")
async def quiz_generate(req: QuizGenRequest):
    # Basic stub quiz
    items = [
        {
            "type": "mcq",
            "question_md": f"Q{i+1}. Placeholder question about {req.topic or 'lesson'}",
            "options_json": {"options": ["A", "B", "C", "D"]},
            "correct_json": {"answer": "A"},
        }
        for i in range(req.count)
    ]
    return {"items": items}


class QuizGradeRequest(BaseModel):
    answers: list[str]


@router.post("/quiz/grade")
async def quiz_grade(req: QuizGradeRequest):
    # Simple equal weight score
    score = 0.0
    rubric = {"criteria": ["correctness", "reasoning", "clarity"]}
    return {"score": score, "rubric": rubric, "feedback_md": "Grading service stub"}


class MathSolveRequest(BaseModel):
    latex: str | None = None
    text: str | None = None


@router.post("/math/solve")
async def math_solve(req: MathSolveRequest):
    # Stub symbolic math solver
    return {"steps_md": "1) Parse 2) Solve 3) Simplify", "result": "N/A"}

