/*
 * What is the best way to center a div on the screen using jQuery?
 * From: http://stackoverflow.com/questions/210717/what-is-the-best-way-to-center-a-div-on-the-screen-using-jquery
 */

jQuery.fn.center = function () {
    this.css("position","absolute");
    this.css("top", ( $(window).height() - this.height() ) / 2+$(window).scrollTop() + "px");
    this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
    return this;
}


function createPopupDiv(options, htmlText) {
    var mydiv = $(document.createElement('div'));
    mydiv.css('border', '5px solid red');
    mydiv.css({'position': 'absolute', 'z-index': '90000', 'background-color': 'white', 'padding': '15px', 'padding-bottom': '5px'});
    mydiv.css(options);
    mydiv.html(htmlText);
    $('body').append(mydiv);    
    mydiv.expose();

    var close_div = $(document.createElement('div'));
    close_div.html('<strong>[Close]</strong>');
    close_div.css({
        'position': 'relative',
        'z-index': '91000',
        'background-color': 'white',
        'padding-top': '5px',
        'margin-top': '5px',
        'left': '0',
        'bottom': '0',
        'border-top': '1px solid red'
    });

    $(close_div).click(function() {
        $(this).hide();
        $(mydiv).hide();
        $.mask.close();
    });    

    $(mydiv).append(close_div);

    return mydiv;
}

