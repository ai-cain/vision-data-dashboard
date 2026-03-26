import type { SelectHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={cn(
        "h-11 rounded-2xl border border-ink/15 bg-white px-4 text-sm text-ink outline-none transition focus:border-teal focus:ring-2 focus:ring-teal/20",
        props.className,
      )}
      {...props}
    />
  );
}
