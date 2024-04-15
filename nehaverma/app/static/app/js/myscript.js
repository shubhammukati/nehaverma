$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true, // Enable infinite loop
    margin: 20, // Set margin between items
    responsiveClass: true,
    responsive: {
        0: {
            items: 1, // Display one item on smaller screens
            nav: false, // Hide navigation arrows
            dots: true, // Show pagination dots
            autoplay: true, // Enable autoplay
            autoplayTimeout: 3000, // Set autoplay interval to 3 seconds
            autoplayHoverPause: true, // Pause autoplay on mouse hover
            animateOut: 'fadeOut', // Apply fade-out effect
            mouseDrag: true, // Enable mouse dragging
        },
        600: {
            items: 4, // Display four items on medium screens
            nav: true, // Show navigation arrows
            dots: false, // Hide pagination dots
            autoplay: true, // Enable autoplay
            autoplayTimeout: 4000, // Set autoplay interval to 4 seconds
            autoplayHoverPause: true, // Pause autoplay on mouse hover
            animateOut: 'fadeOut', // Apply fade-out effect
            mouseDrag: true, // Enable mouse dragging
        },
        1000: {
            items: 4, // Display four items on larger screens
            nav: true, // Show navigation arrows
            dots: false, // Hide pagination dots
            loop: true, // Enable infinite loop
            autoplay: true, // Enable autoplay
            autoplayTimeout: 5000, // Set autoplay interval to 5 seconds
            autoplayHoverPause: true, // Pause autoplay on mouse hover
            animateOut: 'fadeOut', // Apply fade-out effect
            mouseDrag: true, // Enable mouse dragging
        }
    }
});

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Corrected accessing parent node

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity;
            $('#amount').text(data.amount); // Updated jQuery syntax for selecting and updating element
            $('#totalamount').text(data.totalamount); // Updated jQuery syntax for selecting and updating element
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Corrected accessing parent node

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity;
            $('#amount').text(data.amount); // Updated jQuery syntax for selecting and updating element
            $('#totalamount').text(data.totalamount); // Updated jQuery syntax for selecting and updating element
        }
    });
});

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Corrected accessing parent node

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data){
            $('#amount').text(data.amount); // Updated jQuery syntax for selecting and updating element
            $('#totalamount').text(data.totalamount); // Updated jQuery syntax for selecting and updating element
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    });
});



