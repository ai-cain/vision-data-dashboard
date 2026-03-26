import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { applyLiveEventToOverview, buildEventsWebSocketUrl, isVisionEventPayload } from "@/lib/live-stream";
import type { DashboardOverview, LiveStreamEnvelope } from "@/types/models";

export function useDashboardLiveStream() {
  const queryClient = useQueryClient();
  const [connectionState, setConnectionState] = useState<"connecting" | "open" | "closed" | "error">(
    "connecting",
  );

  useEffect(() => {
    const socket = new WebSocket(buildEventsWebSocketUrl());

    socket.addEventListener("open", () => {
      setConnectionState("open");
    });

    socket.addEventListener("error", () => {
      setConnectionState("error");
    });

    socket.addEventListener("close", () => {
      setConnectionState("closed");
    });

    socket.addEventListener("message", (messageEvent) => {
      try {
        const payload = JSON.parse(messageEvent.data) as LiveStreamEnvelope;
        const liveEvent = payload.data;
        if (payload.event !== "event.created" || !isVisionEventPayload(liveEvent)) {
          return;
        }

        queryClient.setQueryData<DashboardOverview>(["dashboard-overview"], (current) =>
          current ? applyLiveEventToOverview(current, liveEvent) : current,
        );
        void queryClient.invalidateQueries({ queryKey: ["events"] });
        void queryClient.invalidateQueries({ queryKey: ["event-stats"] });
        void queryClient.invalidateQueries({ queryKey: ["devices"] });
        void queryClient.invalidateQueries({ queryKey: ["device", liveEvent.device_id] });
      } catch {
        setConnectionState("error");
      }
    });

    return () => {
      socket.close();
    };
  }, [queryClient]);

  return connectionState;
}
