
    // Capturar el formulario
    const form = document.getElementById('availability-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (event) => {
      event.preventDefault(); // Evitar el envío predeterminado del formulario

      // Obtener los valores del formulario
      const doc_id = document.getElementById('doc_id').value;
      const start_time = document.getElementById('start_time').value;
      const end_time = document.getElementById('end_time').value;
      const status = document.getElementById('status').value;

      // Crear un objeto con los datos
      const data = {
        id: Math.floor(Math.random() * 100000), // Generar un ID único (puedes cambiar esta lógica)
        doc_id: doc_id,
        start_time: start_time,
        end_time: end_time,
        status: status
      };

      try {
        // Enviar los datos al backend
        const response = await fetch('http://127.0.0.1:5000/doctor_availability', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          const result = await response.json();
          messageDiv.textContent = result.message; // Mostrar el mensaje del backend
          messageDiv.style.color = 'green';
          form.reset(); // Limpiar el formulario
        } else {
          const error = await response.json();
          messageDiv.textContent = error.error || 'Error al registrar la disponibilidad';
          messageDiv.style.color = 'red';
        }
      } catch (err) {
        console.error(err);
        messageDiv.textContent = 'Error al conectarse con el servidor';
        messageDiv.style.color = 'red';
      }
    });
