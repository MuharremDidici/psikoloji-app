document.addEventListener('DOMContentLoaded', () => {
    const appointmentForm = document.getElementById('appointment-form');

    appointmentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic form validation
        const name = this.querySelector('input[type="text"]').value.trim();
        const email = this.querySelector('input[type="email"]').value.trim();
        const phone = this.querySelector('input[type="tel"]').value.trim();
        const service = this.querySelector('select').value;

        if (!name || !email || !phone || !service) {
            alert('Lütfen tüm alanları doldurunuz.');
            return;
        }

        // Email format validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Lütfen geçerli bir e-posta adresi giriniz.');
            return;
        }

        // Phone number validation (basic Turkish phone number format)
        const phoneRegex = /^(05|5)[0-9]{9}$/;
        if (!phoneRegex.test(phone.replace(/\s/g, ''))) {
            alert('Lütfen geçerli bir telefon numarası giriniz.');
            return;
        }

        // Simulated form submission (replace with actual backend logic)
        alert('Randevu talebiniz alınmıştır. En kısa sürede sizinle iletişime geçeceğiz.');
        this.reset();
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

$(document).ready(function() {
    function initializeCalendar() {
        $('#calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            height: 500, // Set the height of the calendar
            selectable: true,
            selectHelper: true,
            select: function(start, end) {
                const selectedDate = start.format('YYYY-MM-DD');
                const psychologistId = $('#psychologist').val();
                if (psychologistId) {
                    fetchAvailableTimeSlots(psychologistId, selectedDate);
                }
            },
            eventRender: function(event, element) {
                if (!event.available) {
                    element.css('background-color', '#ff9999');
                }
            }
        });
    }

    initializeCalendar();

    $('#psychologist').change(function() {
        var psychologistId = $(this).val();
        if (psychologistId) {
            $('#calendar').show(); // Show the calendar
            $.ajax({
                url: '/availability/' + psychologistId,
                method: 'GET',
                success: function(dates) {
                    $('#calendar').fullCalendar('removeEvents'); // Clear previous events
                    $('#calendar').fullCalendar('addEventSource', dates.map(date => ({
                        start: date,
                        rendering: 'background',
                        color: '#4CAF50'
                    })));
                },
                error: function() {
                    console.error('Error fetching availability');
                }
            });
        } else {
            $('#calendar').hide(); // Hide the calendar if no psychologist is selected
        }
    });
});
