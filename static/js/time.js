// Set the date we're counting down to

function countdown(){
    var xhReq = new XMLHttpRequest();
    xhReq.open("GET", "/start_time", false);
    xhReq.send(null);
    var t = JSON.parse(xhReq.responseText);
    console.log(t.time);
    countDownDate = new Date(t.time).getTime()+ 602000 ;
//    602000
    // Update the count down every 1 second
    var x = setInterval(function() {

      // Get today's date and time
      var now = new Date().getTime() ;

      // Find the distance between now and the count down date
      var distance = countDownDate-now;

      // Time calculations for days, hours, minutes and seconds
          var days = Math.floor(distance / (1000 * 60 * 60 * 24));
          var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
          var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      // Output the result in an element with id="demo"
      document.getElementById("ten-countdown").innerHTML = minutes + "m " + seconds + "s ";

      // If the count down is over, write some text
      if (distance < 0) {
                clearInterval(x);
                document.getElementById("ten-countdown").innerHTML = "Time is up!";
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
      }
    }, 1000);
}
//    var now = new Date("Apr 28, 2021 15:19:32").getTime();
function get_timer() {

         $.ajax({
                type: "GET",
                url: "/get_timer",
                success:function (result,status,xhr){
                console.log(result);
                if (result.timer) {
                    countdown();
                    // console.log("inside timer");
                    }
                },
                error:function (xhr,status,error){
                console.log(error)
                }

                });
//                return 0;

}
get_timer();

