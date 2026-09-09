export interface DataAgentRequest {
  question: string;
}

export interface DataAgentAnalysisResult {
  analysis_type:
    | "global_kpis"
    | "grouped_defect_rate"
    | "monthly_trend";
  summary: string;
  data: unknown;
  chart_url: string | null;
}

export interface DataAgentResponse {
  success: boolean;
  result: DataAgentAnalysisResult | null;
  error: string | null;
}