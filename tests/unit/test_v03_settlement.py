from omst.data import synthetic_settlement_intent
from omst.enums import TransitionEvaluationStatus
from omst.graph import MoneyGraph
from omst.settlement import evaluate_settlement, plan_transition
from omst.stress import stress_test


def test_plan_transition_has_ordered_cash_leg_steps() -> None:
    plan = plan_transition(synthetic_settlement_intent())

    assert plan.status == "PLANNED"
    assert [step.source for step in plan.steps] == ["EUR-X", "CBM"]
    assert [step.target for step in plan.steps] == ["CBM", "EUR-Y"]


def test_evaluate_settlement_returns_machine_readable_compatibility() -> None:
    result = evaluate_settlement(synthetic_settlement_intent())

    assert result.status in {
        TransitionEvaluationStatus.COMPATIBLE,
        TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE,
    }
    assert result.confidence == "synthetic-reference"
    assert result.required_transitions


def test_stress_test_reports_liquidity_shock_ladder() -> None:
    result = stress_test("liquidity-shock")

    assert result["scenario"] == "liquidity-shock"
    assert len(result["results"]) == 3
    assert result["results"][-1]["compatible"] is False


def test_graph_mermaid_output_contains_edge_labels() -> None:
    graph = MoneyGraph()
    assert graph.to_mermaid() == "flowchart LR"
