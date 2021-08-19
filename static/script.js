$(document).ready(function () {

    let today = new Date() 
    // This is the js required to initialize the Materialize elements.
    $(".sidenav").sidenav({
        edge: "right"
    });
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $("select").formSelect();
    $('.modal').modal();
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


    // The edit users button that removes the disabled attribute from inputs in the form.
    $(".editUserButton").click(function () {
        $('.input-field').children(':disabled').removeAttr('disabled')
        $('select').removeAttr('disabled')
    })

    // This is the code that injects the time slots into the booking form, suggested by my mentor Akshat Garg.
    $('.refresh-time-slots').click(function(){
        response = getAvailableSlots($("#instructor-selector").val(), $('#lesson-booking-date-picker').val())
        response.then(html =>{
            console.log(html)
            $('#time-selector').html(html)
        })
        
    })

    $('.time-selector').focus(function(){
        html = getAvailableSlots($("#instructor-username").text(), $(".datepicker:visible").value)
    })

    async function getAvailableSlots(instructor, date) {
        console.log(instructor)
        console.log(date)

        response = await fetch(`/get_available_slots?date=${date}&instructor=${instructor.toLowerCase()}`) // Here the python function is being called with the date and instructor variables.
        response.json().then(data => {      
            slots = data.slots            // Here the data gets turned into json so that it can read the available time slots and add it to the html.
            let timeSlotsHTML = $('#disabled-select').outerHTML;
            for (slot in slots) {
                timeSlotsHTML += `<option value="${slots[slot]}">${slots[slot]}</option>`
            }
            console.log(timeSlotsHTML) // finally this is where the html gets injected into the time-selector input ready for the user to select.
            return timeSlotsHTML
        })
    }


    // This is to set the year of the copyright in the footer of the page, it was taken from the thorin flask project.
    $("#copyright").text(new Date().getFullYear());


})