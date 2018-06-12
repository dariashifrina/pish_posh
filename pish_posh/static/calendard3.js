var compareDates = function(date1, date2) { //accepts UNIX timestamps
    var tempd1 = new Date(date1 * 1000).setHours(0, 0, 0, 0);
    var tempd2 = new Date(date2 * 1000).setHours(0, 0, 0, 0);
    console.log(tempd1);
    console.log(tempd2);
    return tempd1===tempd2;
}
console.log('hi');

var updateEvents = function() {

}
