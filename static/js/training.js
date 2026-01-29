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
