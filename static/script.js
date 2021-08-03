
$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $("select").formSelect();
    $(".datepicker").datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    })

    $(".editUserButton").click(function(){
        $('.input-field').children(':disabled').removeAttr('disabled')
        $('select').removeAttr('disabled')
    })
    
})

