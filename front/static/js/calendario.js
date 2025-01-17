document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");
  const popup = document.getElementById("event-popup");
  const overlay = document.querySelector(".popup-overlay");

  const popupDocId = document.getElementById("popup-doc_id");
  const popupEstId = document.getElementById("popup-est_id");
  const popupTurDia = document.getElementById("popup-tur_dia");
  const popupTime = document.getElementById("popup-time");
  const popupPatient = document.getElementById("popup-patient");
  const popupSubmit = document.getElementById("popup-submit");
  const popupCancel = document.getElementById("popup-cancel");

  const blockedDates = [];

  // Mostrar el popup
  function showPopup(date) {
    popupTurDia.value = date;
    popup.style.display = "block";
    overlay.style.display = "block";
  }

  // Ocultar el popup
  function hidePopup() {
    popup.style.display = "none";
    overlay.style.display = "none";
    popupDocId.value = "";
    popupEstId.value = "";
    popupTurDia.value = "";
    popupTime.value = "";
    popupPatient.value = "";
  }

  overlay.addEventListener("click", hidePopup);
  popupCancel.addEventListener("click", hidePopup);

  // Cargar doctores
  async function loadDoctors() {
    try {
      const response = await fetch("http://127.0.0.1:5000/doctors/options");
      if (response.ok) {
        const doctors = await response.json();
        doctors.forEach((doctor) => {
          const option = document.createElement("option");
          option.value = doctor.doc_id;
          option.textContent = `${doctor.doctor_name} - ${doctor.speciality || "Sin especialidad"}`;
          popupDocId.appendChild(option);
        });
      } else {
        throw new Error("Error al cargar los doctores");
      }
    } catch (err) {
      console.error(err.message);
    }
  }

  // Crear un turno
  async function createAppointment() {
    const turDia = popupTurDia.value.trim();
    const turHora = popupTime.value.trim();
    const docId = popupDocId.value.trim();
    const pacId = popupPatient.value.trim();
    const estId = popupEstId.value.trim();

    if (turDia && turHora && docId && pacId && estId) {
      const turno = {
        tur_dia: turDia,
        tur_hora: `${turHora}:00`, // Asegurar formato HH:MM:SS
        doc_id: docId,
        pac_id: pacId,
        est_id: estId,
      };

      try {
        const response = await fetch("http://127.0.0.1:5000/turns", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(turno),
        });

        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          calendar.refetchEvents();
          hidePopup();
        } else {
          const error = await response.json();
          throw new Error(error.error || "Error al crear el turno");
        }
      } catch (err) {
        console.error(err.message);
        alert(`Error: ${err.message}`);
      }
    } else {
      alert("Por favor, complete todos los campos.");
    }
  }

  popupSubmit.addEventListener("click", createAppointment);

  // Procesar días bloqueados
  async function loadBlockedDates() {
    try {
      const response = await fetch("http://127.0.0.1:5000/doctor_availability");
      if (response.ok) {
        const data = await response.json();
        data.forEach((item) => {
          if (item.end) {
            let startDate = new Date(item.start);
            const endDate = new Date(item.end);
            while (startDate <= endDate) {
              blockedDates.push(startDate.toISOString().split("T")[0]);
              startDate.setDate(startDate.getDate() + 1);
            }
          } else {
            blockedDates.push(item.start);
          }
        });
      }
    } catch (err) {
      console.error("Error al cargar días bloqueados:", err);
    }
  }

  // Inicializar calendario
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay",
    },
    events: "http://127.0.0.1:5000/turns",
    selectable: true,
    dateClick: (info) => {
      if (blockedDates.includes(info.dateStr)) {
        alert("Este día está bloqueado.");
        return;
      }
      showPopup(info.dateStr);
    },
    dayCellDidMount: (info) => {
      if (blockedDates.includes(info.date.toISOString().split("T")[0])) {
        info.el.style.backgroundColor = "#f8d7da";
        info.el.style.cursor = "not-allowed";
      }
    },
  });

  // Cargar datos y renderizar
  loadDoctors();
  loadBlockedDates().then(() => calendar.render());
});
