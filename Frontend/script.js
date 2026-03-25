const API_BASE_URL = "http://127.0.0.1:8000/api";

async function fetchAndRenderData() {
  try {
    const revRes = await fetch(`${API_BASE_URL}/revenue`);
    const revData = await revRes.json();

    const revLabels = revData.map((d) => d.order_year_month);
    const revAmounts = revData.map((d) => d.amount);

    new Chart(document.getElementById("revenueChart"), {
      type: "line",
      data: {
        labels: revLabels,
        datasets: [
          {
            label: "Revenue ($)",
            data: revAmounts,
            borderColor: "#3b82f6",
            backgroundColor: "rgba(59, 130, 246, 0.1)",
            borderWidth: 2,
            fill: true,
            tension: 0.2,
          },
        ],
      },
    });

    const catRes = await fetch(`${API_BASE_URL}/categories`);
    const catData = await catRes.json();

    const catLabels = catData.map((d) => d.category);
    const catAmounts = catData.map((d) => d.total_revenue);

    new Chart(document.getElementById("categoryChart"), {
      type: "bar",
      data: {
        labels: catLabels,
        datasets: [
          {
            label: "Revenue ($)",
            data: catAmounts,
            backgroundColor: [
              "#3b82f6",
              "#10b981",
              "#f59e0b",
              "#ef4444",
              "#8b5cf6",
            ],
            borderRadius: 4,
          },
        ],
      },
    });
  } catch (error) {
    console.error("Dashboard failed to load:", error);
  }
}

document.addEventListener("DOMContentLoaded", fetchAndRenderData);
