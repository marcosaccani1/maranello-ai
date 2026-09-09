from fastapi import APIRouter, HTTPException, status

from app.models.analysis import (
    AnalysisRequest,
    AnalysisResponse,
)
from app.services.data_analysis_service import (
    DataAnalysisService,
)

router = APIRouter()

analysis_service = DataAnalysisService()


@router.post(
    "/analysis",
    response_model=AnalysisResponse,
)
def analyze(
    request: AnalysisRequest,
) -> AnalysisResponse:
    try:
        result = analysis_service.analyze_question(
            request.question
        )

        return AnalysisResponse(
            success=True,
            result=result,
        )

    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc