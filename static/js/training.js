document.addEventListener("DOMContentLoaded", () => {
  const saveButton = document.getElementById("save-all-button");

  // drag and drop logic
  document.querySelectorAll(".operator").forEach(op => {
    op.draggable = true;

    op.addEventListener("dragstart", e => {
      e.dataTransfer.setData("text/plain", "");
      window.draggedOperator = op;
      op.classList.add("dragging");
    });

    op.addEventListener("dragend", () => {
      op.classList.remove("dragging");
      window.draggedOperator = null;
    });
  });

  document.querySelectorAll(".status-column").forEach(column => {
    column.addEventListener("dragover", e => {
      e.preventDefault();
    });

    column.addEventListener("drop", e => {
      e.preventDefault();

      const operatorEl = window.draggedOperator;
      if (!operatorEl) return;

      const sourceTrainingId =
        operatorEl.closest(".training").dataset.trainingId;
      const targetTrainingId =
        column.closest(".training").dataset.trainingId;

      if (sourceTrainingId !== targetTrainingId) return;
      column.appendChild(operatorEl);
    });
  });

  // Save All Changes button handler

  saveButton.addEventListener("click", () => {
    const trainingsData = {};

    document.querySelectorAll(".training").forEach(trainingDiv => {
      const trainingId = trainingDiv.dataset.trainingId;
      trainingsData[trainingId] = {};

      trainingDiv.querySelectorAll(".status-column").forEach(col => {
        const status = col.dataset.status;

        col.querySelectorAll(".operator").forEach(opEl => {
          const operatorId = opEl.dataset.operatorId;
          trainingsData[trainingId][operatorId] = status;
        });
      });
    });

    console.log("Saving full state:", trainingsData);

    fetch("/update_statuses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ trainings: trainingsData })
    })
      .then(resp => resp.json())
      .then(data => {
        console.log("Save response:", data);
        alert("All changes saved!");
      });
  });
});

document.getElementById("add-operator").addEventListener("click", () => {
  const name = prompt("Enter operator name:");
  if (!name) return;

  fetch("/operators", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  })
  .then(res => res.json())
  .then(operator => {
    // Add to NOT TRAINED column of every training
    document.querySelectorAll(".training").forEach(trainingDiv => {
      const notTrainedCol = trainingDiv.querySelector(
        ".status-column[data-status='not_trained']"
      );

      const opEl = document.createElement("div");
      opEl.className = "operator";
      opEl.dataset.operatorId = operator.id;
      opEl.textContent = operator.name;
      opEl.draggable = true;

      notTrainedCol.appendChild(opEl);
    });

    location.reload(); // safest while developing
  });
});

let selectedOperator = null;

document.addEventListener("click", e => {
  if (e.target.classList.contains("operator")) {
    document.querySelectorAll(".operator")
      .forEach(op => op.classList.remove("selected"));

    e.target.classList.add("selected");
    selectedOperator = e.target;
  }
});

document.getElementById("delete-operator").addEventListener("click", () => {
  if (!selectedOperator) {
    alert("Select an operator first");
    return;
  }

  const operatorId = selectedOperator.dataset.operatorId;
  if (!confirm("Delete this operator?")) return;

  fetch(`/operators/${operatorId}`, { method: "DELETE" })
    .then(res => res.json())
    .then(() => {
      location.reload();
    });
});

