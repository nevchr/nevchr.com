(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const revealItems = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 },
    );
    revealItems.forEach((item) => observer.observe(item));
  }

  const header = document.querySelector("[data-header]");
  let lastScroll = window.scrollY;
  window.addEventListener(
    "scroll",
    () => {
      const currentScroll = window.scrollY;
      header?.classList.toggle("is-hidden", currentScroll > lastScroll && currentScroll > 120);
      lastScroll = currentScroll;
    },
    { passive: true },
  );

  const orbit = document.querySelector("[data-orbit]");
  const disc = orbit?.querySelector(".hero-disc");
  if (orbit && disc && !reduceMotion) {
    window.addEventListener("pointermove", (event) => {
      const x = (event.clientX / window.innerWidth - 0.5) * 8;
      const y = (event.clientY / window.innerHeight - 0.5) * 8;
      disc.style.transform = `rotateX(${58 - y}deg) rotateY(${x}deg) rotateZ(-18deg)`;
    });
  }

  document.querySelector("[data-to-top]")?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
  });
})();
