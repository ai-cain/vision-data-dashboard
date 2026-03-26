import { useQuery } from "@tanstack/react-query";

import { fetchEvents, fetchEventStats } from "@/lib/api";
import type { EventFilters } from "@/types/models";

export function useEvents(filters: EventFilters) {
  return useQuery({
    queryKey: ["events", filters],
    queryFn: () => fetchEvents(filters),
    refetchInterval: 20_000,
  });
}

export function useEventStats() {
  return useQuery({
    queryKey: ["event-stats"],
    queryFn: fetchEventStats,
    refetchInterval: 30_000,
  });
}
