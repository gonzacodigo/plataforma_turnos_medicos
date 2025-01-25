document.addEventListener("DOMContentLoaded", function () {
  // Referencias a elementos del DOM
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

  const blockedDates = []; // Almacena días bloqueados

  // Mostrar el popup para crear un turno
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
    popupTime.innerHTML = ""; // Limpiar horarios disponibles
    popupPatient.value = "";
  }

  overlay.addEventListener("click", hidePopup);
  popupCancel.addEventListener("click", hidePopup);

  // Cargar doctores en el selector
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
      console.error("Error al cargar doctores:", err.message);
    }
  }

  // Crear un turno y enviarlo al backend
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
        console.error("Error al crear el turno:", err.message);
        alert(`Error: ${err.message}`);
      }
    } else {
      alert("Por favor, complete todos los campos.");
    }
  }

  popupSubmit.addEventListener("click", createAppointment);

  // Cargar días bloqueados desde el backend
  async function loadBlockedDates() {
    try {
      const response = await fetch("http://127.0.0.1:5000/doctor_availability");
      if (response.ok) {
        const data = await response.json();
        data.forEach((item) => {
          blockedDates.push({
            start: item.start,
            end: item.end,
            overlap: false,
            rendering: "background",
            color: "#ff9f89",
          });
        });
      }
    } catch (err) {
      console.error("Error al cargar días bloqueados:", err);
    }
  }

  // Configurar FullCalendar
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay",
    },
    events: "http://127.0.0.1:5000/turns",
    selectable: true,
    select: (info) => {
      const isBlocked = blockedDates.some((block) => {
        return (
          new Date(block.start) <= new Date(info.start) &&
          new Date(block.end) >= new Date(info.end)
        );
      });
      if (isBlocked) {
        alert("Este rango está bloqueado.");
        return;
      }
      showPopup(info.startStr);
    },
    eventSources: [
      {
        events: blockedDates,
      },
    ],
  });

  async function loadAvailableSlots(docId, date) {
    const popupTime = document.getElementById("popup-time");
    popupTime.innerHTML = ""; // Limpiar opciones previas
  
    if (!docId || !date) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "Seleccione un doctor y una fecha primero";
      popupTime.appendChild(option);
      return;
    }
  
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/available_slots?doc_id=${docId}&date=${date}`
      );
  
      if (response.ok) {
        const slots = await response.json();
  
        if (slots.length === 0) {
          const option = document.createElement("option");
          option.value = "";
          option.textContent = "No hay horarios disponibles";
          popupTime.appendChild(option);
          return;
        }
  
        // Agregar horarios disponibles al selector
        slots.forEach((slot) => {
          const option = document.createElement("option");
          option.value = slot;
          option.textContent = slot;
          popupTime.appendChild(option);
        });
      } else {
        console.error("Error al cargar horarios:", await response.text());
        alert("No se pudieron cargar los horarios disponibles.");
      }
    } catch (err) {
      console.error("Error al cargar horarios:", err);
    }
  }
  
  // Escuchar cambios en el doctor y la fecha seleccionados

  
  popupDocId.addEventListener("change", () => {
    const docId = popupDocId.value;
    const date = popupTurDia.value;
    loadAvailableSlots(docId, date);
  });
  
  popupTurDia.addEventListener("change", () => {
    const docId = popupDocId.value;
    const date = popupTurDia.value;
    loadAvailableSlots(docId, date);
  });
  
  // Cargar datos iniciales y renderizar el calendario
  loadDoctors();
  loadBlockedDates().then(() => calendar.render());
});
