document.addEventListener("DOMContentLoaded", function () {
  // Elementos del DOM relacionados con el calendario y los popups
  const calendarEl = document.getElementById("calendar"); // Contenedor del calendario
  const popup = document.getElementById("event-popup"); // Popup para crear o editar un turno
  const detailsPopup = document.getElementById("details-popup"); // Popup para ver detalles de un turno
  const overlay = document.querySelector(".popup-overlay"); // Fondo para desactivar interacción fuera del popup

  // Elementos del formulario dentro del popup
  const popupDocId = document.getElementById("popup-doc_id"); // Selector de doctores
  const popupEstId = document.getElementById("popup-est_id"); // Campo de estado del turno
  const popupTurDia = document.getElementById("popup-tur_dia"); // Campo de fecha del turno
  const popupTime = document.getElementById("popup-time"); // Selector de horarios disponibles
  const popupPatient = document.getElementById("popup-patient"); // Selector de pacientes
  const popupSubmit = document.getElementById("popup-submit"); // Botón para guardar el turno
  const popupCancel = document.getElementById("popup-cancel"); // Botón para cancelar el formulario

  // Elementos para mostrar los detalles de un turno seleccionado
  const detailsDoc = document.getElementById("details-doc"); // Muestra el nombre del doctor
  const detailsPatient = document.getElementById("details-patient"); // Muestra el nombre del paciente
  const detailsDate = document.getElementById("details-date"); // Muestra la fecha del turno
  const detailsTime = document.getElementById("details-time"); // Muestra la hora del turno
  const detailsStatus = document.getElementById("details-status"); // Muestra el estado del turno
  const detailsEdit = document.getElementById("details-edit"); // Botón para editar el turno
  const detailsCancel = document.getElementById("details-cancel"); // Botón para cancelar el turno
  const detailsClose = document.getElementById("details-close"); // Botón para cerrar el popup de detalles

  // Variables para manejar la lógica del calendario
  const blockedDates = []; // Almacena los días bloqueados por vacaciones o feriados
  let selectedEvent = null; // Guarda el evento actualmente seleccionado para editar o eliminar

  /**
   * Función para mostrar el popup de creación o edición de turnos
   * @param {string} date Fecha seleccionada en formato YYYY-MM-DD
   */
  function showPopup(date) {
    popupTurDia.value = date; // Prellenar el campo de fecha
    popup.style.display = "block"; // Mostrar el popup
    overlay.style.display = "block"; // Mostrar el fondo de superposición
  }

  /**
   * Función para mostrar los detalles de un turno
   * @param {Object} event Evento seleccionado del calendario
   */
  function showDetailsPopup(event) {
    selectedEvent = event; // Guardar el evento seleccionado
    detailsDoc.textContent =
      event.extendedProps?.doctor_name || "No especificado";
    detailsPatient.textContent =
      event.extendedProps?.patient_name || "No especificado";
    detailsDate.textContent = event.startStr.split("T")[0]; // Extrae la fecha
    detailsTime.textContent = event.startStr.split("T")[1].split("-")[0];
 // Extrae la hora
    detailsStatus.textContent =
      event.extendedProps?.status || "No especificado";

    detailsPopup.style.display = "block"; // Mostrar el popup de detalles
    overlay.style.display = "block"; // Mostrar el fondo de superposición
  }

  /**
   * Función para ocultar todos los popups
   */
  function hidePopup() {
    popup.style.display = "none";
    detailsPopup.style.display = "none";
    overlay.style.display = "none";

    // Limpiar los valores del formulario
    popupDocId.value = "";
    popupEstId.value = "";
    popupTurDia.value = "";
    popupTime.innerHTML = ""; // Limpiar los horarios disponibles
    popupPatient.value = "";
    selectedEvent = null; // Limpiar la selección de eventos
  }

  overlay.addEventListener("click", hidePopup); // Ocultar popups al hacer clic en el fondo
  popupCancel.addEventListener("click", hidePopup); // Ocultar popup de creación
  detailsClose.addEventListener("click", hidePopup); // Ocultar popup de detalles

  /**
   * Carga los doctores disponibles en el selector del popup
   */
  async function loadDoctors() {
    try {
      const response = await fetch("http://127.0.0.1:5000/doctors/options");
      if (response.ok) {
        const doctors = await response.json();
        doctors.forEach((doctor) => {
          const option = document.createElement("option");
          option.value = doctor.doc_id;
          option.textContent = `${doctor.doctor_name} - ${
            doctor.speciality || "Sin especialidad"
          }`;
          popupDocId.appendChild(option);
        });
      } else {
        throw new Error("Error al cargar los doctores");
      }
    } catch (err) {
      console.error("Error al cargar doctores:", err.message);
    }
  }

  /**
   * Carga los pacientes disponibles en el selector del popup
   */
  async function loadPatients() {
    try {
      const response = await fetch("http://127.0.0.1:5000/patients/options");
      if (response.ok) {
        const patients = await response.json();
        patients.forEach((patient) => {
          const option = document.createElement("option");
          option.value = patient.pac_id;
          option.textContent = patient.patient_name;
          popupPatient.appendChild(option);
        });
      } else {
        throw new Error("Error al cargar los pacientes");
      }
    } catch (err) {
      console.error("Error al cargar pacientes:", err.message);
    }
  }

  /**
   * Carga los estados disponibles en el selector del popup
   */
  async function loadStates() {
    try {
      const response = await fetch("http://127.0.0.1:5000/states/options");
      if (response.ok) {
        const states = await response.json();
        states.forEach((state) => {
          const option = document.createElement("option");
          option.value = state.est_id;
          option.textContent = state.est_nombre;
          popupEstId.appendChild(option);
        });
      } else {
        throw new Error("Error al cargar los estados");
      }
    } catch (err) {
      console.error("Error al cargar estados:", err.message);
    }
  }

  // Crear o actualizar un turno
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
        doc_id: parseInt(docId),
        pac_id: parseInt(pacId),
        est_id: parseInt(estId),
      };

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/turns${
            selectedEvent ? "/" + selectedEvent.id : ""
          }`,
          {
            method: selectedEvent ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(turno),
          }
        );

        if (response.ok) {
          const result = await response.json();
          alert(result.message);

          // Refrescar eventos y ocultar el popup
          calendar.refetchEvents();
          hidePopup();
        } else {
          const error = await response.json();
          throw new Error(error.error || "Error al guardar el turno");
        }
      } catch (err) {
        console.error("Error al guardar el turno:", err.message);
        alert(`Error: ${err.message}`);
      }
    } else {
      alert("Por favor, complete todos los campos.");
    }
  }

  // Cargar horarios disponibles dinámicamente
  async function loadAvailableSlots(docId, date) {
    popupTime.innerHTML = ""; // Limpiar horarios previos

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
      console.error("Error al cargar horarios:", err.message);
    }
  }

  // Escuchar cambios en doctor y fecha
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

  // Llamar al cargar los horarios disponibles al abrir para editar
  detailsEdit.addEventListener("click", () => {
    if (selectedEvent) {
      const docId = selectedEvent.extendedProps.doc_id;
      const date = selectedEvent.startStr.split("T")[0];

      // Prellenar los campos con los valores del turno seleccionado
      popupDocId.value = docId;
      popupPatient.value = selectedEvent.extendedProps.pac_id;
      popupEstId.value = selectedEvent.extendedProps.est_id;
      popupTurDia.value = date;

      // Cargar horarios disponibles para ese doctor y fecha
      loadAvailableSlots(docId, date);

      // Mostrar el popup para editar
      popup.style.display = "block";
      detailsPopup.style.display = "none";
    }
  });

  popupSubmit.addEventListener("click", createAppointment);

  // Cancelar un turno
  async function cancelAppointment() {
    if (!selectedEvent) {
      alert("No hay un turno seleccionado para cancelar.");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/turns/${selectedEvent.id}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        const result = await response.json();
        alert(result.message);
        calendar.refetchEvents();
        hidePopup();
      } else {
        const error = await response.json();
        throw new Error(error.error || "Error al cancelar el turno");
      }
    } catch (err) {
      console.error("Error al cancelar el turno:", err.message);
      alert(`Error: ${err.message}`);
    }
  }

  detailsCancel.addEventListener("click", cancelAppointment);

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
    eventClick: ({ event }) => showDetailsPopup(event),
  });

  async function loadAvailableSlots(docId, date) {
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

  loadDoctors();
  loadPatients();
  loadStates();
  loadBlockedDates().then(() => calendar.render());
});
