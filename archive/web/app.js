//Header
// Nav Padding
const pageHeader = document.querySelector(".page-header"); //unique
const pageHeaderHeight = pageHeader.offsetHeight;

document.documentElement.style.setProperty(
  "--page-header-padding",
  pageHeaderHeight + "px"
);

//Menu Toggle
const menuToggle = document.querySelector(".menu-toggle"); //unique
const primaryNavigation = document.querySelector(".primary-navigation"); //unique
const navLinks = document.querySelectorAll(".nav-link"); //list

menuToggle.addEventListener("click", () => {
  const isOpened = menuToggle.getAttribute("aria-expanded") === "true";
  if (isOpened ? closeMenu() : openMenu());
});
function openMenu() {
  menuToggle.setAttribute("aria-expanded", "true");
  primaryNavigation.setAttribute("data-state", "opened");
}
function closeMenu() {
  menuToggle.setAttribute("aria-expanded", "false");
  primaryNavigation.setAttribute("data-state", "closing");
  primaryNavigation.addEventListener(
    "animationend",
    () => {
      primaryNavigation.setAttribute("data-state", "closed");
    },
    { once: true }
  );
}

//Footer
// Set Year on Copyright
document.getElementById("currentYear").innerHTML = new Date().getFullYear();

// Media Query
const mediaQuery = window.matchMedia("(min-width: 900px)");
mediaQuery.addListener(screenChange);
screenChange(mediaQuery);

function screenChange(query) {
  if (query.matches) {
    primaryNavigation.setAttribute("data-state", "open");
    // Remove all nav_link event listeners
    navLinks.forEach(function (nav_link) {
      nav_link.removeEventListener("click", closeMenu);
    });
  } else {
    primaryNavigation.setAttribute("data-state", "closed");
    // Add nav_link event listeners
    navLinks.forEach(function (nav_link) {
      nav_link.addEventListener("click", closeMenu);
    });
  }
}

// Miscellaneous
// Clicking an anchor with a button
const buttons = document.querySelectorAll(".cta-btn");
buttons.forEach(function (button) {
  const link = button.querySelector("a");

  button.addEventListener("click", function () {
    link.click();
  });
});
