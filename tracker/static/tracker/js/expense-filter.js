document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".category-link").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();  // Prevent page reload

            let selectedCategory = this.getAttribute("data-category");

            // Highlight the selected category
            document.querySelectorAll(".category-link").forEach(link => link.classList.remove("active"));
            this.classList.add("active");

            // Fetch filtered expenses via AJAX
            fetch(`/filter_expenses/?category=${selectedCategory}`)
                .then(response => response.json())
                .then(data => {
                    let tableBody = document.querySelector("#expense-table tbody");
                    tableBody.innerHTML = "";  // Clear existing rows

                    if (data.expenses.length > 0) {
                        data.expenses.forEach(expense => {
                            let row = `
                                <tr>
                                    <td>${expense.title}</td>
                                    <td>₹${expense.amount}</td>
                                    <td>${expense.category}</td>
                                    <td>${expense.date}</td>
                                   <td>
                                    <a href="/edit/${expense.id}/" class="text-warning">
                                        <i class="fa-solid fa-pen-to-square"></i> <!-- Edit Icon -->
                                    </a>
                                    &nbsp; <!-- Space between icons -->
                                    <a href="/delete/${expense.id}/" 
                                    class="text-danger"
                                    onclick="return confirm('Are you sure you want to delete this expense?');">
                                        <i class="fa-solid fa-trash"></i> <!-- Red Trash Bin Icon -->
                                    </a>
                                </td>
                            </tr>
                            `;
                            tableBody.innerHTML += row;
                        });
                    } else {
                        tableBody.innerHTML = `<tr><td colspan="5" class="text-center">No expenses found.</td></tr>`;
                    }
                })
                .catch(error => console.error("Error fetching data:", error));
        });
    });
});