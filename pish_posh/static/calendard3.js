var compareDates = function(date1, date2) { //accepts UNIX timestamps
    var tempd1 = new Date(date1 * 1000)
    tempd1.setHours(0, 0, 0, 0);
    var tempd2 = new Date(date2 * 1000)
    tempd2.setHours(0, 0, 0, 0);
    return tempd1===tempd2;
}

var unixToISO = function(unix) {
    var t = new Date(unix * 1000);
    t.setHours(0, 0, 0, 0);
    return t.toISOString().split('T')[0];
}

var updateEvents = function(assignments) {
    var dates = document.getElementsByClassName('hello-week__day');//d3.selectAll('.hello-week__day');
    var currentDate = (new Date()).toISOString().split('T')[0];
    for (var i = 0; i < dates.length; i++) {
        for (var j = 0; j < assignments.length; j++) {
            cdate = unixToISO(dates[i].getAttribute("data-timestamp"));
            adate = assignments[j][2]
            if (adate === cdate) {
                var type = assignments[j][1] == 0 ? "Assignment" : "Test";
                d3.select(dates[i]).classed('tool', true).attr('title', type + ": " + assignments[j][3]).attr('data-placement', 'bottom');
                if ((new Date(cdate))-(new Date) > 0) {
                    if (assignments[j][1] == 0) {
                        d3.select(dates[i]).style("background-color", "red");
                    }
                    else {
                        d3.select(dates[i]).style("background-color", "blue");
                    }
                }
                else {
                    if (assignments[j][1] == 0) {
                        d3.select(dates[i]).style("background-color", "green");
                    }
                    else {
                        d3.select(dates[i]).style("background-color", "yellow");
                    }                }
            }
        }
    }
    $('.tool').tooltip()
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

$(document).ready(function() {
    getAllAssignments()
    $('.tool').tooltip()
});
