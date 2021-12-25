
// handle curved rows style
$('.curved').each(function () {
    let startIndex = 0
    let numberOfSeats = $(this).children().length
    console.log(numberOfSeats)
    $(this).children().each(function (index) {
        if (index + 1 < numberOfSeats / 2) {
            $(this).css('margin-top',  4 * startIndex + 'px')
            $(this).css('margin-bottom',  -2 * startIndex + 'px')
            startIndex ++
        } else if (index + 1 === numberOfSeats / 2){
            $(this).css('margin-top',  4 * startIndex + 'px')
            $(this).css('margin-bottom',  -2 * startIndex + 'px')
        } else {
            $(this).css('margin-top',  4 * startIndex + 'px')
            $(this).css('margin-bottom',  -2 * startIndex + 'px')
            startIndex --
        }
    })
})

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})
