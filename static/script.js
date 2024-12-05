$(document).ready(function() {
    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultView: 'agendaWeek',
        height: 650,
        contentHeight: 600,
        aspectRatio: 2,
        timezone: 'local',
        selectable: true,
        selectHelper: true,
        editable: false,
        eventColor: '#28a745',
        slotDuration: '01:00:00',
        minTime: '09:00:00',
        maxTime: '18:00:00',
        allDaySlot: false,
        buttonText: {
            today: 'Bugün',
            month: 'Ay',
            week: 'Hafta',
            day: 'Gün'
        },
        monthNames: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz',
            'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
        ],
        monthNamesShort: ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz',
            'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'
        ],
        dayNames: ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba',
            'Perşembe', 'Cuma', 'Cumartesi'
        ],
        dayNamesShort: ['Paz', 'Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt'],
        select: function(start, end) {
            var selectedSlot = start.format('YYYY-MM-DD HH:mm:ss');
            var psychologistId = $('#psychologist').val();
            
            if (!psychologistId) {
                alert('Lütfen önce bir psikolog seçiniz.');
                $('#calendar').fullCalendar('unselect');
                return;
            }

            var title = prompt('İsminizi giriniz:');
            if (title) {
                $.ajax({
                    url: '/make_appointment',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        psychologist_id: psychologistId,
                        client_name: title,
                        appointment_date: selectedSlot
                    }),
                    success: function(response) {
                        alert('Randevunuz başarıyla oluşturuldu!');
                        loadPsychologistAvailability(psychologistId);
                    },
                    error: function() {
                        alert('Randevu oluşturulurken bir hata oluştu.');
                    }
                });
            }
            $('#calendar').fullCalendar('unselect');
        }
    });

    $('#psychologist').change(function() {
        var psychologistId = $(this).val();
        if (psychologistId) {
            loadPsychologistAvailability(psychologistId);
        } else {
            $('#calendar').fullCalendar('removeEvents');
        }
    });

    function loadPsychologistAvailability(psychologistId) {
        $('#calendar').fullCalendar('removeEvents');
        $.ajax({
            url: '/appointments/' + psychologistId,
            method: 'GET',
            success: function(events) {
                $('#calendar').fullCalendar('addEventSource', events);
            },
            error: function() {
                alert('Takvim verileri yüklenirken bir hata oluştu.');
            }
        });
    }
});
