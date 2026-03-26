import type { HTMLAttributes, PropsWithChildren } from "react";

import { cn } from "@/lib/utils";

export function Card({ children, className, ...props }: PropsWithChildren<HTMLAttributes<HTMLDivElement>>) {
  return (
    <div
      className={cn(
        "rounded-[28px] border border-ink/10 bg-paper/90 p-5 shadow-panel backdrop-blur",
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardTitle({ children, className, ...props }: PropsWithChildren<HTMLAttributes<HTMLHeadingElement>>) {
  return (
    <h3 className={cn("text-lg font-semibold text-ink", className)} {...props}>
      {children}
    </h3>
  );
}

export function CardDescription({
  children,
  className,
  ...props
}: PropsWithChildren<HTMLAttributes<HTMLParagraphElement>>) {
  return (
    <p className={cn("text-sm text-ink/65", className)} {...props}>
      {children}
    </p>
  );
}
