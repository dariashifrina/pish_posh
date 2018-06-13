var compareDates = function(date1, date2) { //accepts UNIX timestamps
    var tempd1 = new Date(date1 * 1000)
    tempd1.setHours(0, 0, 0, 0);
    var tempd2 = new Date(date2 * 1000)
    tempd2.setHours(0, 0, 0, 0);
    console.log(tempd1);
    console.log(tempd2);
    return tempd1===tempd2;
}
console.log('hi');

var unixToISO = function(unix) {
    var t = new Date(unix * 1000);
    t.setHours(0, 0, 0, 0);
    return t.toISOString().split('T')[0];
}

var updateEvents = function(assignments) {
    var dates = document.getElementsByClassName('hello-week__day');//d3.selectAll('.hello-week__day');
    for (var i = 0; i < dates.length; i++) {
        for (var j = 0; j < assignments.length; j++) {
            cdate = unixToISO(dates[i].getAttribute("data-timestamp"));
            adate = assignments[j][2]
            if (adate === cdate) {
                console.log(assignments[j]);
            }
        }
    }
    return dates;
}

var getAllAssignments = function() {
    $.ajax({
        url: "/calendarhelp",
        type: "GET",
        async: true,
        beforeSend: function() {
        },
        success: function(result) {
            assignments=JSON.parse(result);
            updateEvents(assignments)
        },
        error: function(a,b,c) {
            console.log('nope');
        }
    })
}
