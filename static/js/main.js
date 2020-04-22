$(function(){
    $("#form-register").validate({
        rules: {
            password : {
                required : true,
            },
            confirm_password: {
                equalTo: "#password"
            }
        },
        messages: {
            username: {
                required: "Please provide an username"
            },
            email: {
                required: "Please provide an email"
            },
            password: {
                required: "Please provide a password"
            },
            confirm_password: {
                required: "Please provide a password",
                equalTo: "Please enter the same password"
            }
        }
    });
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        // enableAllSteps: true,
        autoFocus: true,
        transitionEffectSpeed: 500,
        titleTemplate : '<div class="title">#title#</div>',
        labels: {
            previous : 'Back',
            next : '<i class="zmdi zmdi-arrow-right"></i>',
            finish : '<i class="zmdi zmdi-arrow-right"></i>',
            current : ''
        },
        onStepChanging: function (event, currentIndex, newIndex) { 
            var year = $('#year').val();
            var salary = $('#salary').val();
            var hra = $('#hra').val();
            var rent = $('#rent').val();
            var spa = $('#spa').val();
            var lta = $('#lta').val();
            var expe = $('#exp').val();
	    var interest = $('#interest').val();
            var fda = $('#fda').val();
	    var agr = $('#agr').val();
            var gifts = $('#gifts').val();
            var ppf = $('#ppf').val();
            var epf = $('#epf').val();
            var elss = $('#elss').val();
            var lip = $('#lip').val();
            var mip1 = $('#mip1').val();
            var mip2 = $('#mip2').val();
            var fees = $('#fees').val();
            var nps = $('#nps').val();
            var don = $('#don').val();



            $('#year-val').select(year);
            $('#salary-val').text(salary);
            $('#hra-val').text(hra);
            $('#rent-val').text(rent);
            $('#spa-val').text(spa);
            $('#lta-val').text(lta);
            $('#exp-val').text(expe);
            $('#interest-val').text(interest);
            $('#fda-val').text(fda);
            $('#agr-val').text(agr);
            $('#gifts-val').text(gifts);
            $('#ppf-val').text(ppf);
            $('#epf-val').text(epf);
            $('#elss-val').text(elss);
            $('#lip-val').text(lip);
            $('#mip1-val').text(mip1);
            $('#mip2-val').text(mip2);
            $('#fees-val').text(fees);
            $('#nps-val').text(nps);
            $('#don-val').text(don);
		

            $("#form-register").validate().settings.ignore = ":disabled,:hidden";
            return $("#form-register").valid();
        }
    });
});
