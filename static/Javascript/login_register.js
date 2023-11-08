const text = "Welcome to GUSH inventory";
const typingSpeed = 100; // Adjust the speed (milliseconds per character)
const typingElement = document.getElementById("welcome_message");

let charIndex = 0;

function typeText() {
    if (charIndex < text.length) {
        typingElement.innerHTML += text.charAt(charIndex);
        charIndex++;
        setTimeout(typeText, typingSpeed);
    }
}

// Start typing when the page loads
document.addEventListener("DOMContentLoaded", () => {
    typeText();
});
