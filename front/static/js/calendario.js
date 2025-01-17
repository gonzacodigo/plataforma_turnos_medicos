document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");
    const popup = document.getElementById("event-popup");
    const overlay = document.querySelector(".popup-overlay");
  
    const popupIdDoctor = document.getElementById("popup-doc_id");
    const popupIdState = document.getElementById("popup-est_id");
    const popupTurDia = document.getElementById("popup-tur_dia");
    const popupTime = document.getElementById("popup-time");
    const popupPatient = document.getElementById("popup-patient");
    const popupSubmit = document.getElementById("popup-submit");
    const popupCancel = document.getElementById("popup-cancel");
    const blockedDates = []; // Lista de fechas bloqueadas
  
    // Función para mostrar el popup
    function showPopup(date) {
      popupTurDia.value = date; // Autocompletar la fecha en el popup
      popup.style.display = "block";
      overlay.style.display = "block";
    }
  
    // Función para ocultar el popup
    function hidePopup() {
      popup.style.display = "none";
      overlay.style.display = "none";
      popupTime.value = "";
      popupPatient.value = "";
      popupIdDoctor.value = "";
      popupIdState.value = "";
    }
  
    overlay.addEventListener("click", hidePopup);
  
    // Inicializar FullCalendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay",
      },
      events: "http://127.0.0.1:5000/turns", // Carga eventos desde la API
      selectable: true,
      dateClick: function (info) {
        // Validar si el día está bloqueado
        if (blockedDates.includes(info.dateStr)) {
          alert("Este día está bloqueado. No se pueden sacar turnos.");
          return;
        }
        showPopup(info.dateStr);
      },
      dayCellDidMount: function (info) {
        // Resaltar días bloqueados
        if (blockedDates.includes(info.date.toISOString().split("T")[0])) {
          info.el.classList.add("fc-disabled-day");
          info.el.style.backgroundColor = "#f8d7da"; // Color para días bloqueados
          info.el.style.cursor = "not-allowed";
        }
      },
    });
  
    // Crear un turno al hacer clic en "Crear Turno"
    popupSubmit.addEventListener("click", function () {
      const tur_dia = popupTurDia.value.trim(); // Fecha seleccionada (YYYY-MM-DD)
      const tur_hora = popupTime.value.trim(); // Hora seleccionada (HH:MM o HH:MM:SS)
      const doc_id = popupIdDoctor.value.trim(); // ID del doctor
      const pac_id = popupPatient.value.trim(); // ID del paciente
      const est_id = popupIdState.value.trim(); // ID del estado
  
      // Verificar que todos los campos estén completos
      if (tur_dia && tur_hora && doc_id && pac_id && est_id) {
        const horaCompleta = tur_hora.includes(":") && tur_hora.split(":").length === 2
          ? `${tur_hora}:00` // Asegurar formato HH:MM:SS
          : tur_hora;
  
        fetch("http://127.0.0.1:5000/turns", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            tur_dia: tur_dia,
            tur_hora: horaCompleta,
            doc_id: doc_id,
            pac_id: pac_id,
            est_id: est_id,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              return response.json().then((err) => {
                throw new Error(err.error || "Error en la solicitud.");
              });
            }
            return response.json();
          })
          .then((data) => {
            alert(data.message); // Mostrar mensaje de éxito
            calendar.refetchEvents(); // Actualizar eventos en el calendario
            hidePopup(); // Ocultar el popup
          })
          .catch((err) => {
            console.error("Error al crear turno:", err.message);
            alert(`Hubo un error al intentar crear el turno: ${err.message}`);
          });
      } else {
        alert("Por favor, complete todos los campos antes de continuar."); // Validación de campos vacíos
      }
    });
  
    // Procesar días bloqueados desde el backend
    function processBlockedDates(data) {
      data.forEach((item) => {
        if (item.end) {
          // Rango de fechas
          let startDate = new Date(item.start);
          let endDate = new Date(item.end);
          while (startDate <= endDate) {
            blockedDates.push(startDate.toISOString().split("T")[0]);
            startDate.setDate(startDate.getDate() + 1);
          }
        } else {
          // Fecha única
          blockedDates.push(item.start);
        }
      });
    }
  
    // Obtener días bloqueados desde el backend
    fetch("http://127.0.0.1:5000/doctor_availability")
      .then((response) => response.json())
      .then((data) => {
        processBlockedDates(data); // Procesar y cargar los días bloqueados
        calendar.render();
      })
      .catch((err) => {
        console.error("Error al cargar los días bloqueados:", err);
      });
  });
  