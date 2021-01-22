/*!
    * Start Bootstrap - Grayscale v6.0.3 (https://startbootstrap.com/theme/grayscale)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
    */
    (function ($) {
	"use strict"; // Start of use strict
	     
		$(window).on('load', function() {
			var preloaderFadeOutTime = 650;
			function hidePreloader() {
				var preloader = $('.loader-wrapper');
				setTimeout(function() {
					preloader.fadeOut(preloaderFadeOutTime);
				}, 500);
			}
			hidePreloader();
		});

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 70,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 100,
    });
    

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict

$(document).ready(function () {

    $('.first-button').on('click', function () {
    
      $('.animated-icon1').toggleClass('open');
    });
    });
      $(document).ready(function() {
    
    const $cibil_value = $('.valueSpan2');
    const $cibil = $('#customRange11');
    $cibil_value.html($cibil.val());
    $cibil.on('input change', () => {
    
      $cibil_value.html($cibil.val());
    });
    });
    $(document).ready(function() {
    
    const $mort = $('.mort-acc-range');
    const $mort_acc = $('#mortAcc');
    $mort.html($mort_acc.val());
    $mort_acc.on('input change', () => {
    
      $mort.html($mort_acc.val());
    });
    });
    $(document).ready(function() {
    const $tot_cred = $('.total-cred-range');
    const $total_cred = $('#total-cred');
    $tot_cred.html($total_cred.val());
    $total_cred.on('input change', () => {
    
      $tot_cred.html($total_cred.val());
    });
    });
    $(document).ready(function() {

	const $cibil_value2 = $('.cibil_score2_span');
	const $cibil2 = $('#cibil_score2');
	$cibil_value2.html($cibil2.val());
	$cibil2.on('input change', () => {
	
		$cibil_value2.html($cibil2.val());
	});
	});
	$(document).ready(function() {

	const $cibil_value = $('.cibil_score_span');
	const $cibil = $('#cibil_score');
	$cibil_value.html($cibil.val());
	$cibil.on('input change', () => {
	
		$cibil_value.html($cibil.val());
	});
	});

	$(document).ready(function() {
	const $startYear_value = $('.startYearValue');
	const $startYear = $('#startYear');
	$startYear_value.html($startYear.val());
	$startYear.on('input change', () => {
	
		$startYear_value.html($startYear.val());
	});
	});

	$(document).ready(function() {
	const $endYear_value = $('.endYearValue');
	const $endYear = $('#endYear');
	$endYear_value.html($endYear.val());
	$endYear.on('input change', () => {
	
		$endYear_value.html($endYear.val());
	});
	});

	//Inflation Calculator JS Starts Here
	var $principalAmnt = $('#principalAmount');
	var $prin = $('#prin');
	var $endYear = $('#endYear')
	var $enYear = $('#enYear');
	var $startYear = $('#startYear')
	var $stYear = $('#stYear');
	$(document).ready(function() {
		$startYear.on('input change', () => {
		
			$stYear.html($startYear.val());
		});
	});
	$(document).ready(function() {
	$endYear.on('input change', () => {

		$enYear.html($endYear.val());
	});
	});
	$(document).ready(function() {
	$principalAmnt.on('input change', () => {
	
		$prin.html($principalAmnt.val());
	});
		});
			
	var apiUrl = 'https://www.statbureau.org/calculate-inflation-price-jsonp?jsoncallback=?';
		
	$('#calc').on('click', function calculate() {
	var s = String($startYear.val())+'/1/1';
	var e = String($endYear.val())+'/12/1';
	var p = String($principalAmnt.val());
	$.getJSON(apiUrl, {
		country: 'india',
		start: s,
		end: e,
		amount: p,
		format: true
		})
		.done(function (data) {
		$('#endPrice').html(data);
		});
	});
	




			// EMI Calculator JS Starts Here
            //initial variables
			var loanYear = 20;
			var stepYear = 5;
			var maxLoanYear = 30;
			var paymentCycle = 1;
			var monthlyRepayment = 0;
			var monthlyInterest = 0;
			var amortData = [];
			
			//start up method
			$(function(){
				$(".ul-buttons li").click(function(){
					$(".ul-buttons li").removeClass("selected");
					$(this).addClass("selected");
					paymentCycle = parseInt($(this).attr("data-value"));
					calculateLoan();
				});
				
				//Add on blur event
				$("#txtLoan, #txtInterest").on("blur", function(){
					//Perform a check if loan or interest value has been entered invalid value, if it is, set the default value
					if(isNaN($("#txtLoan").val())) {
						$("#txtLoan").val(1000000);
					}
					
					if(isNaN($("#txtInterest").val())) {
						$("#txtInterest").val(8.99);
					}
					calculateLoan();
				});
			});
			
			//create the noUiSlider
			var range = document.getElementById('yearRange');
			noUiSlider.create(range, {
				range: {
					'min': 5,
					'max': maxLoanYear
				},
				step: stepYear,
				start: [loanYear],
				margin: 300,
				connect: true,
				direction: 'ltr',
				orientation: 'horizontal',
				pips: {
					mode: 'steps',
					stepped: false,
					density: 2
				}
			});
			
			//Add the change event to redraw the graph and calculate loan
			range.noUiSlider.on("change", function(value){
				loanYear = parseInt(value[0]);
				calculateLoan();
			});
			
			//Chart
			google.charts.load('current', {'packages':['corechart']});
			function drawChart() {
				//Hold the loan data array
				var loanData = [];
				
				var dt = new Date();
				var yearCounter = 1;
				
				//Add the graph header
				var headerData = ['Year', 'Interest', 'Interest & Principal', 'Balance'];
				loanData.push(headerData);
				
				for(var i = dt.getFullYear(); i < dt.getFullYear() + loanYear; i++){
					loanData.push([i.toString(), getAmortData("interest", 12 * yearCounter), monthlyRepayment * 12 * yearCounter, getAmortData("balance", 12 * yearCounter)]);
					yearCounter++;
				}
				
				var data = google.visualization.arrayToDataTable(loanData);

				var options = {
				  title: 'Loan Chart',
				  hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}},
				  vAxis: {minValue: 0},
				  pointsVisible: true
				};

				var chart = new google.visualization.AreaChart(document.getElementById('graph-chart'));
				chart.draw(data, options);
			}
			
			//Get amortization data based on type and terms
			function getAmortData(dataType, terms){
				var dataValue = 0;
				switch(dataType){
					case "interest":
						for(var i = 0; i < terms; i++){
							dataValue += parseFloat(amortData[i].Interest);
						}
						break;
					case "balance":
						dataValue = parseFloat(amortData[terms-1].Balance);
						break;
				}
				return Math.round(dataValue);
			}
			
			//calculate function
			function calculateLoan(){
				$("#year-value").html(loanYear);
				var loanBorrow = parseFloat($("#txtLoan").val());
				var interestRate = parseFloat($("#txtInterest").val()) / 1200;
				var totalTerms = 12 * loanYear;
	
				//Monthly
				var schedulePayment = Math.round(loanBorrow * interestRate / (1 - (Math.pow(1/(1 + interestRate), totalTerms))));
				monthlyRepayment = schedulePayment;
				var totalInterestPay = totalTerms * schedulePayment;
				amort(loanBorrow, parseFloat($("#txtInterest").val())/100, totalTerms);
				
				switch(paymentCycle){
					case 2:
						//Fortnightly
						//we multiple by 12 then divided by 52 then multiple by 2
						schedulePayment = Math.round(((schedulePayment * 12) / 52) * 2);
						break;
					case 3:
						//Weekly
						//we multiple by 12 then divided by 52 
						schedulePayment = Math.round((schedulePayment * 12) / 52);
						break;
				}
				
				$("#repayment-value").html(schedulePayment);
				$("#interest-total").html(getAmortData("interest", totalTerms));
				monthlyInterest = (totalInterestPay - loanBorrow) / totalTerms;
				google.charts.setOnLoadCallback(drawChart);
			}
			
			calculateLoan();
			
			//function to calculate the amortization data
			function amort(balance, interestRate, terms)
			{
				amortData = [];
				
				//Calculate the per month interest rate
				var monthlyRate = interestRate/12;
				
				//Calculate the payment
				var payment = balance * (monthlyRate/(1-Math.pow(1+monthlyRate, -terms)));
					
				for (var count = 0; count < terms; ++count)
				{ 
					var interest = balance * monthlyRate;
					var monthlyPrincipal = payment - interest;
					var amortInfo = {
						Balance: balance.toFixed(2),
						Interest: balance * monthlyRate,
						MonthlyPrincipal: monthlyPrincipal
					}
					amortData.push(amortInfo);
					balance = balance - monthlyPrincipal;		
				}
				
			}
			// EMI Calculator JS Ends Here
			
           
