document.querySelector("form").addEventListener("submit", function (event) {
    const healthProblem = document.querySelector("textarea[name='health_problem']").value.trim();
    if (!healthProblem) {
        event.preventDefault();
        alert("Please enter a health problem.");
    }
});