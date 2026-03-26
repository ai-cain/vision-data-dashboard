import { useQuery } from "@tanstack/react-query";

import { fetchDevice, fetchDevices } from "@/lib/api";

export function useDevices() {
  return useQuery({
    queryKey: ["devices"],
    queryFn: fetchDevices,
    refetchInterval: 30_000,
  });
}

export function useDevice(deviceId: string | null) {
  return useQuery({
    queryKey: ["device", deviceId],
    queryFn: () => fetchDevice(deviceId as string),
    enabled: Boolean(deviceId),
    refetchInterval: 30_000,
  });
}
