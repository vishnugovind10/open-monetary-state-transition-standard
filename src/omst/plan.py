from decimal import Decimal

from .models import TransitionPlan


def validate_plan(plan: TransitionPlan) -> list[str]:
    errors: list[str] = []
    if not plan.steps:
        return ["plan contains no steps"]
    for index, step in enumerate(plan.steps):
        if step.requirements.minimum_liquidity <= Decimal(0):
            errors.append(f"step {index + 1} has non-positive liquidity requirement")
        if not step.failure_path:
            errors.append(f"step {index + 1} has no failure path")
        if index > 0 and plan.steps[index - 1].target != step.source:
            errors.append(f"step {index + 1} breaks state continuity")
    if any(step.requirements.minimum_liquidity != plan.steps[0].requirements.minimum_liquidity for step in plan.steps):
        errors.append("plan breaks quantity continuity")
    return errors
