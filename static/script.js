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
        getAvailableSlots($("#instructor-selector").val(), $('#lesson-booking-date-picker').val())
    })

    $('.time-selector').focus(function(){
        instructor = $(this).parentsUntil($('form')).find($('.instructor-username')).val()
        date = $(this).parentsUntil($('form')).find($('.datepicker')).val()
    
         getAvailableSlots(instructor, date)
    })

    async function getAvailableSlots(instructor, date) {
        console.log(instructor)
        console.log(date)

        response = await fetch(`/get_available_slots?date=${date}&instructor=${instructor.toLowerCase()}`) // Here the python function is being called with the date and instructor variables.
        response.json().then(data => {     
            slots = data.slots  
            let timeSlotsHTML = ''
            $('.time-slot').remove()
            for (slot in slots) {
                if (slots[slot] == 'fully booked'){
                    timeSlotsHTML += `<option class="time-slot" value="" disabled>${slots[slot]}</option>`
                }else{
                    timeSlotsHTML += `<option class="time-slot" value="${slots[slot]}">${slots[slot]}</option>`
                }

            }
            console.log(timeSlotsHTML) // finally this is where the html gets injected into the time-selector input ready for the user to select.
            $('.disabled-select').after(timeSlotsHTML)
                    // Here the data gets turned into json so that it can read the available time slots and add it to the html.
        })
    }


    // This is to set the year of the copyright in the footer of the page, it was taken from the thorin flask project.
    $("#copyright").text(new Date().getFullYear());


})