from app.core.config import settings
from app.services.analysis_service import AnalysisService
from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader


def test_real_dataset_grouped_analysis_returns_expected_dimensions() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()
    service = AnalysisService()

    cleaned = cleaner.clean(loader.load())

    production_lines = service.calculate_defect_rate_by(
        cleaned,
        dimension="production_line",
    )
    shifts = service.calculate_defect_rate_by(
        cleaned,
        dimension="shift",
    )
    suppliers = service.calculate_defect_rate_by(
        cleaned,
        dimension="supplier_id",
    )
    components = service.calculate_defect_rate_by(
        cleaned,
        dimension="component_category",
    )

    assert len(production_lines) == 4
    assert len(shifts) == 3
    assert len(suppliers) == 12
    assert len(components) == 6


def test_real_dataset_grouped_analysis_is_sorted_by_defect_rate() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()
    service = AnalysisService()

    cleaned = cleaner.clean(loader.load())

    results = service.calculate_defect_rate_by(
        cleaned,
        dimension="production_line",
    )

    defect_rates = [item.defect_rate for item in results]

    assert defect_rates == sorted(defect_rates, reverse=True)