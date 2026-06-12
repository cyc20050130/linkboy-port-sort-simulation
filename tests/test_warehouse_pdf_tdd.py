from __future__ import annotations

from pathlib import Path

import pytest

from tools.warehouse_tdd_contracts import LabModel, PDFContract, build_pdf_contracts


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "work" / "warehouse_scheduler.lab"


@pytest.fixture(scope="module")
def lab() -> LabModel:
    return LabModel.from_file(LAB)


@pytest.mark.parametrize("contract", build_pdf_contracts(), ids=lambda item: item.name)
def test_pdf_linkboy_stage_contracts(contract: PDFContract, lab: LabModel) -> None:
    result = contract.check(lab)
    assert result.passed, result.message
