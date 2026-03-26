function initializeMermaid() {
  if (typeof window.mermaid === "undefined") {
    return;
  }

  window.mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme: "neutral"
  });

  window.mermaid.run({
    querySelector: ".mermaid"
  });
}

if (typeof window.document$ !== "undefined") {
  window.document$.subscribe(function () {
    initializeMermaid();
  });
} else {
  window.addEventListener("load", function () {
    initializeMermaid();
  });
}
