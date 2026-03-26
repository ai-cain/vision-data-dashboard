import type { ButtonHTMLAttributes, PropsWithChildren } from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-full border text-sm font-medium transition hover:-translate-y-0.5 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "border-ember bg-ember px-4 py-2 text-white shadow-panel hover:bg-[#c75f2c]",
        secondary: "border-ink/15 bg-paper px-4 py-2 text-ink hover:border-ink/30",
        ghost: "border-transparent bg-transparent px-3 py-2 text-ink hover:bg-ink/5",
      },
    },
    defaultVariants: {
      variant: "primary",
    },
  },
);

type ButtonProps = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> &
    VariantProps<typeof buttonVariants> & {
      asChild?: boolean;
    }
>;

export function Button({ children, className, variant, asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp className={cn(buttonVariants({ variant }), className)} {...props}>
      {children}
    </Comp>
  );
}
