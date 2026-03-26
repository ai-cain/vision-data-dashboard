import { useQuery } from "@tanstack/react-query";

import { fetchInspectionSummary, fetchInspections } from "@/lib/api";
import type { InspectionFilters } from "@/types/models";

export function useInspections(filters: InspectionFilters) {
  return useQuery({
    queryKey: ["inspections", filters],
    queryFn: () => fetchInspections(filters),
    refetchInterval: 20_000,
  });
}

export function useInspectionSummary() {
  return useQuery({
    queryKey: ["inspection-summary"],
    queryFn: fetchInspectionSummary,
    refetchInterval: 30_000,
  });
}
