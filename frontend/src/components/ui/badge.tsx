import type { HTMLAttributes, PropsWithChildren } from "react";

import { cn } from "@/lib/utils";

export function Badge({ children, className, ...props }: PropsWithChildren<HTMLAttributes<HTMLSpanElement>>) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-1 font-mono text-xs uppercase tracking-[0.16em]",
        className,
      )}
      {...props}
    >
      {children}
    </span>
  );
}
