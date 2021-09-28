function countdown(elementName, minutes, seconds) {
    var element, endTime, hours, mins, msLeft, time;

    function twoDigits(n) {
        return (n <= 9 ? "0" + n : n);
    }

    function updateTimer() {
        msLeft = endTime - (+new Date);
        if (msLeft < 1000) {
            element.innerHTML = "Time is up!";
            document.getElementById("textInput").disabled = true;
            document.getElementById("textInput").placeholder = "Thank you for the exam";
            document.getElementById("send").remove();
//            window.location="/submit";

            console.log("before");
            var token =  $('input[name="csrfToken"]').attr('value');
            console.log(token)
            $.ajax({
                type: "POST",
                url: "/get_bot_response",
                data: { 'msg':'','end':'yes','csrfmiddlewaretoken': token}
                })
                .done(function( msg ) {
                window.location = "/account/logout";
                });

            console.log("after");

        } else {
            time = new Date(msLeft);
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits(mins) : mins) + ':' + twoDigits(time
                .getUTCSeconds());
            setTimeout(updateTimer, time.getUTCMilliseconds() + 500);
        }
    }

    element = document.getElementById(elementName);
    endTime = (+new Date) + 1000 * (60 * minutes + seconds) + 500;
    updateTimer();
}

function get_timer() {

         $.ajax({
                type: "GET",
                url: "/get_timer",
                success:function (result,status,xhr){
                console.log(result);
                if (result.timer) {
                    countdown("ten-countdown", 10, 30);
                    console.log("inside timer");
                    }
                },
                error:function (xhr,status,error){
                console.log(error)
                }

                });
//                return 0;

}
get_timer();

//     $.ajax({
//                type: "GET",
//                url: "/get_timer",
//
//                })
//                .done(function( timer ) {
//                   t=timer.timer
//                   return t;
//                });





