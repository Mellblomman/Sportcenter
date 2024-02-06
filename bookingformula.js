var currentDateTime = new Date();
    var year = currentDateTime.getFullYear();
    var month = (currentDateTime.getMonth() + 1);
    var date = (currentDateTime.getDate() + 1);

    if (date < 10) {
      date = '0' + date;
    }
    if (month < 10) {
      month = '0' + month;
    }

    var startHour = 7; // Start time
    var endHour = 17;  // End time

    var startTime = ("0" + startHour).slice(-2) + ":00";
    var endTime = ("0" + endHour).slice(-2) + ":00";

    var dateTomorrow = year + "-" + month + "-" + date + "T" + startTime;
    var checkinElem = document.querySelector("#checkin-date");
    var checkoutElem = document.querySelector("#checkout-date");

    checkinElem.setAttribute("min", dateTomorrow);

    checkinElem.onchange = function () {
      checkoutElem.setAttribute("min", this.value);

      // Update max attribute to limit check-out time
      var selectedDate = new Date(this.value);
      var maxTime = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate(), endHour);
      checkoutElem.setAttribute("max", maxTime.toISOString().slice(0, -8));
    }