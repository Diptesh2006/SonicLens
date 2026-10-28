export type Sample = { timestamp: string; values: Record<string, number> };
export type Dataset = { id: string; name: string; domain: string; source: string; unit: string; metrics: string[]; samples: Sample[] };
export type Analysis = { analysis_id: string; mode: string; summary: { count: number; mean: number; max: number; min: number; unit: string; energy_cost: number | null }; focus_indices: number[]; events: { index: number; value: number }[] };
