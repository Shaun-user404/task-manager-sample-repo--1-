const form = document.querySelector("#add-task-form");
const input = document.querySelector("#new-task");
const list = document.querySelector("#task-list");
const remainingCount = document.querySelector("#remaining-count");
const clearCompletedButton = document.querySelector("#clear-completed");

function updateRemainingCount() {
  remainingCount.textContent = String(
    list.querySelectorAll("input[type=checkbox]:not(:checked)").length
  );
}

function addTask(title) {
  const item = document.createElement("li");
  const checkbox = document.createElement("input");
  const label = document.createElement("label");
  const id = `task-${Date.now()}`;

  item.className = "task-row";
  checkbox.type = "checkbox";
  checkbox.id = id;
  label.htmlFor = id;
  label.textContent = title;
  item.append(checkbox, label);
  list.append(item);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  addTask(title);
  input.value = "";
  updateRemainingCount();
  input.focus();
});

list.addEventListener("change", updateRemainingCount);

clearCompletedButton.addEventListener("click", () => {
  list.querySelectorAll("input[type=checkbox]:checked").forEach((checkbox) => {
    checkbox.closest("li").remove();
  });
  updateRemainingCount();
});
