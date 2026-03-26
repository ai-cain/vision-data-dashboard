import { useQuery } from "@tanstack/react-query";

import { fetchOverview } from "@/lib/api";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard-overview"],
    queryFn: fetchOverview,
    refetchInterval: 30_000,
  });
}
