/* 67 MASSAGE — interactions */
(function () {
  "use strict";

  // sticky header background on scroll
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // mobile drawer toggle
  var burger = document.querySelector(".burger");
  var scrim = document.querySelector(".scrim");
  var toggle = function () { document.body.classList.toggle("menu-open"); };
  if (burger) burger.addEventListener("click", toggle);
  if (scrim) scrim.addEventListener("click", toggle);
  // close drawer after tapping a link
  document.querySelectorAll(".drawer a").forEach(function (a) {
    a.addEventListener("click", function () { document.body.classList.remove("menu-open"); });
  });

  // reveal on scroll
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  // current year in footer
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
