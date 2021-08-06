$(document).ready(function () {
    $(".sidenav").sidenav({
        edge: "right"
    });
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $("select").formSelect();
    $(".datepicker").datepicker({
        format: "dd, mm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        },
        onSelect: function (date) {
            console.log(date.toString())
        }
    })


    // The edit users button that removes the disabled attribute.

    $(".editUserButton").click(function () {
        $('.input-field').children(':disabled').removeAttr('disabled')
        $('select').removeAttr('disabled')
    })

})