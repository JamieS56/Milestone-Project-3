$(document).ready(function () {
    // This is the js required to initialize the Materialize elements.
    $(".sidenav").sidenav({
        edge: "right",
    });
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $("select").formSelect();
    $(".modal").modal();
    $(".datepicker").datepicker({
        format: "dd/mm/yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select",
        },
        minDate: new Date(),
        autoClose: true,
    });


    // The edit users button that removes the disabled attribute from inputs in the form.
    $(".editUserButton").click(function () {
        $(".input-field").children(":disabled").removeAttr("disabled");
        $("select").removeAttr("disabled");
    });

    // This is the code that injects the time slots into the booking form, suggested by my mentor Akshat Garg.
    $(".refresh-time-slots").click(function () {
        getAvailableSlots($("#instructor-selector").val(), $("#lesson-booking-date-picker").val());
    });

    $(".time-selector").focus(function () {
        instructor = $(this).parentsUntil($("form")).find($(".instructor-username")).val();
        date = $(this).parentsUntil($("form")).find($(".datepicker")).val();
        getAvailableSlots(instructor, date);
    });

    async function getAvailableSlots(instructor, date) {
        response = await fetch(`/get_available_slots?date=${date}&instructor=${instructor.toLowerCase()}`); // Here the python function is being called with the date and instructor variables.
        response.json().then((data) => {
            // Here the data gets turned into json so that it can read the available time slots and add it to the html.
            slots = data.slots;
            let timeSlotsHTML = "";
            $(".time-slot").remove();
            for (slot in slots) {
                if (slots[slot] == "fully booked") {
                    timeSlotsHTML += `<option class="time-slot" value="" disabled>${slots[slot]}</option>`; // if the day is fully booked it willl return a disabled option telling the user it's fully booked.
                } else {
                    timeSlotsHTML += `<option class="time-slot" value="${slots[slot]}">${slots[slot]}</option>`;
                }
            }

            $(".disabled-select").after(timeSlotsHTML); // finally this is where the html gets injected into the time-selector input ready for the user to select.
        });
    }

    // This is to set the year of the copyright in the footer of the page, it was taken from the thorin flask project.
    $("#copyright").text(new Date().getFullYear());
});
