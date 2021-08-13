$(document).ready(function () {

    let today = new Date()

    $(".sidenav").sidenav({
        edge: "right"
    });
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $("select").formSelect();
    $(".datepicker").datepicker({
        format: "dd/mm/yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        },
        minDate: today,
        autoClose: true,
    })


    // The edit users button that removes the disabled attribute.

    $(".editUserButton").click(function () {
        $('.input-field').children(':disabled').removeAttr('disabled')
        $('select').removeAttr('disabled')
    })


    $('.refresh-time-slots').click(getAvailableSlots)


    async function getAvailableSlots(_eventdata, instructor = $("#instructor-selector").val(), date = $('#lesson-booking-date-picker').val()) {

        response = await fetch(`/get_available_slots?date=${date}&instructor=${instructor}`)
        response.json().then(data => {
            slots = data.slots
            let timeSlotsHTML = `<option value="" disabled selected>Choose Time Slot</option>`;
            for (slot in slots) {
                timeSlotsHTML += `<option value="${slots[slot]}">${slots[slot]}</option>`
            }
            console.log(timeSlotsHTML);
            document.getElementById('time-selector').innerHTML = timeSlotsHTML;
        })
    }

    // Stepper js taken from


})