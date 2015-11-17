// DOM ready

$(document).ready(function() {

    var NS2_BASE_URL = '/ns2web/ns2web/';
    // Dev
    //var NS2_BASE_URL = '/ns2web/';
    var NS2TRACE_URL = '/ns2web/ns2web/ns2trace/';
    //var NS2TRACE_URL = '/ns2web/ns2trace/';
    var MEDIA_PREFIX = '/ns2web/xmedia/';
    var MAX_NODES = 100;
    var MAX_PORT = 50;
    var INITIAL_POLL_INTERVAL  = 2000 ;     // in milliseconds    
    
    
    $('textarea.resizable:not(.processed)').TextAreaResizer();

    // initialisation     
    editAreaLoader.window_loaded();
    editAreaLoader.init({
        id: "ns2code"	// id of the textarea to transform
        ,start_highlight: true	// if start with highlight
        ,allow_resize: "both"
        ,allow_toggle: false
        ,word_wrap: true
        ,language: "en"
        ,syntax: "php"
        ,replace_tab_by_spaces: 4
    });
    
    
    // Warn IE users
    if ($.browser.msie) {
        $('div.ns2-code').before(
            $(document.createElement('div'))
            .html("You're using <span style='color: red;'>Internet Explorer</span> -- please note that your browser could become non-responsive while running long simulations and/or loading large trace file!")
            .css({'padding': '7px', 'border': '1px dotted silver', 'width': '100%', 'font-weight': 'bold', 'margin': '5px'})
        );
    }    
    
    // Plotting
    var plot_data = [];                
    var placeholder = $("#plotarea");
    var alreadyFetchedPlotData = {};                
    var options = {
        series: {lines: {show: true, lineWidth: 1}, shadowSize: 0},
        //xaxis: { tickDecimals: 0, tickSize: 10, tickLength: 0, alignTicksWithAxis: 1 },
        xaxis: {zoomrange: [0, 100], panrange: [0, 10]},
        yaxis: {zoomrange: [0, 100], panrange: [0, 10]},
        grid: {show: true, borderWidth: 1, hoverable: true},
        crosshair: {mode: 'x'},
        zoom: {interactive: false},
        pan: {interactive: false},
        legend: {
            show: true,
            container: $('#graphs-plotted'),
            labelFormatter: function(label, series) {
                return ('<span class="plot-legend-wrapper" title="Click to remove"><a href="/" class="plot-legend">' + label + '</a><span>');
            }
        }
    };        
    var plot_handle = $.plot(placeholder, plot_data, options);
    
    // Fetch the data with jQuery
    function onDataReceived(series, xaxisLabel, yaxisLabel) {
        // let's add it to our current data

        if ( series.data.length == 0 ) {
            alert('No data found for ' + series.label);
            return;
        }
        //alert(series.data.length);
        //if (!alreadyFetchedPlotData[series.label]) {
            //alreadyFetchedPlotData[series.label] = true;
        
        // If a series with a given label already exists, then append (i) to it i.e.
        // 'Bytes received by 4' would become 'Bytes received by 4 (1)'
        var nSimilarSeries = 0;
        var nNumbered = 0;    
        var nmax = 0;
        for (var iSeries in plot_data) {
            // series.label will always be in pure form, without any (i)
            if ( plot_data[iSeries].label.indexOf(series.label) >= 0 ) {
                ++ nSimilarSeries;

                if ( plot_data[iSeries].label.indexOf('(#') > 0 ) {       
                    ++ nNumbered;
                    var cur_num = parseInt( plot_data[iSeries].label.split('(#')[1].split(')')[0] ) || -1;
                    if (nmax < cur_num)
                        nmax = cur_num;                    
                }                  
            }                                
        }

        //var k = (nmax >= nSimilarSeries) ? nmax : nSimilarSeries;
        var k = 0;    
        if ( (nNumbered < nSimilarSeries) || (nmax > 0) )
            k = nmax + 1;
        else if ( nSimilarSeries && (nNumbered == 1) )
            k = 1;

        //alert(k);
        if (k > 0)
            series.label += ' (#' + k + ')';
        
        plot_data.push(series);
        // and plot all we got
        options.xaxis.axisLabel = xaxisLabel;
        options.yaxis.axisLabel = yaxisLabel;
        $.plot(placeholder, plot_data, options);
        //alert('$.plot');
    }


    function createSlidingDiv(mesg, title, nDelay) {
        $('div.slide-dialog').remove();

        var slide_div = $(document.createElement('div'));
        slide_div.html(mesg);
        slide_div.attr('class', 'slide-dialog').css('width', '890px');

        var close_div = $(document.createElement('div'));
        close_div.html('<strong>' + title + '</strong>')
        close_div
        .attr('class', 'close-dialog');


        $(close_div).click(function() {
            $(this).slideUp('slow');
            $(this).parent()
            .stop(true, true)
            .slideUp('slow', function() {
                $(this).remove();
            });
        });

        slide_div.prepend(close_div);
        slide_div.css('display', 'none')

        // If nDelay > 0, the dialog will automatically disappear after that time (in ms)
        // Otherwise user needs to close it
        if (nDelay > 0)
            slide_div.insertAfter('div.toolbar')
            .not(":animated")
            .slideDown('slow')
            .delay(nDelay)
            .slideUp('slow', function() {
                $(this).remove();
            });
        else
            slide_div.insertAfter('div.toolbar').slideDown('slow');
    }

    function createSlidingDiv2(elements, title, nDelay) {
        $('div.slide-dialog').remove();

        var slide_div = $(document.createElement('div'));
        slide_div.append(elements);
        slide_div.attr('class', 'slide-dialog').css('width', '890px');

        var close_div = $(document.createElement('div'));
        close_div.html('<strong>' + title + '</strong>')
        close_div
        .attr('class', 'close-dialog');


        $(close_div).click(function() {
            $(this).slideUp('slow');
            $(this).parent()
            .stop(true, true)
            .slideUp('slow', function() {
                $(this).remove();
            });
        });

        slide_div.prepend(close_div);
        slide_div.css('display', 'none')

        // If nDelay > 0, the dialog will automatically disappear after that time (in ms)
        // Otherwise user needs to close it
        if (nDelay > 0)
            slide_div.insertAfter('div.toolbar')
            .not(":animated")
            .slideDown('slow')
            .delay(nDelay)
            .slideUp('slow', function() {
                $(this).remove();
            });
        else
            slide_div.insertAfter('div.toolbar').slideDown('slow');
    }


    function showTooltip(x, y, contents) {
        $(document.createElement('div'))
        .attr('id', 'tooltip')
        .text(contents)
        .css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
            border: '1px solid #fcc',
            padding: '2px',
            'background-color': '#fed',
            opacity: 0.90
        })
        .appendTo("body").fadeIn(200);
    }

    var popup_top = $(placeholder).css('top');
    var popup_left = $(placeholder).css('right');
    var popup_options = {
        'position': 'absolute',
        'border':   '1px solid blue',
        'background-color': 'white',
        'z-index':  '98765',
        'top':      popup_top,
        'left':     popup_left
    };
    $(placeholder).bind("plothover",  function (event, pos, item) {
        $("#tooltip").remove();
        if (item) {
            var x = item.datapoint[0].toFixed(2),
            y = item.datapoint[1].toFixed(2);

            showTooltip(item.pageX, item.pageY, '( '+ x + ', ' + y + ' )');
        }
    });

    // Click on a plot legend to remove it from being displayed
    $('.plot-legend').live('click', function(event) {
        event.preventDefault();
        var new_data = [];

        if ($('.plot-legend').length > 1) {
            // Currently there are more than one plots
            // So, on removing a single plot, there will still remain atleast one plot
            for (var k in plot_data) {
                //alert(plot_data[k].label + ': ' + plot_data[k].length)
                if (plot_data[k].label != $(this).text()) {
                    new_data.push(plot_data[k]);
                }
                else {
                    //alreadyFetchedPlotData[plot_data[k].label] = false;
                }
            }            
            // Update the data set -- this is * absolutely * essential
            plot_data = new_data;                        
        } else {
            // When the last plot (and it's legend) has been removed, color of the
            // plot still appears inside this div. So, empty all it's children
            //$('#graphs-plotted').empty();
        }
        $(this).parent().remove();
        $.plot(placeholder, plot_data, options);
    });    


    /** */

    $('div.ns2-form button#clear').click(function(event) {
        $('div.ns2-code-output').text('');
        $('div.ns2-trace-text').text('');
    });


    /*
     *  Execute simulation code
     */
    $('div.ns2-form button#run').click(function(event) {
       event.preventDefault();

       $('div.ns2-code-output').text('');
       $('textarea.ns2-trace-text').text('');
       
       var contents = {'ns2code': editAreaLoader.getValue('ns2code')}; 
       $('div.ns2-code-output').text(contents);

       //var ajax_loading = "<img src='/ns2web/xmedia/images/ajax/ajax_loader.gif' alt='Loading ...' style='width: auto; height: auto; border: 0; margin: 0; padding-left: 44.5%; padding-right: 44.5%; padding-top: 25px; padding-bottom: 25px;'>"
       var ajax_loading = $(document.createElement('img'));
       ajax_loading
       .attr({'src': MEDIA_PREFIX+'images/ajax/ajax_loader.gif', 'alt': 'Loading ...'})
       .css({
                'width': 'auto', 'height': 'auto', 
                'border': 0, 'margin': 0, 
                'padding-left': '44.5%', 'padding-right': '44.5%', 'padding-top': '25px', 'padding-bottom': '25px'
       })
       $('div.ns2-code-output').append(ajax_loading);
       $('textarea.ns2-trace-text')
       .val('Please be patient -- running the simulation and loading the trace file could take considerable amount of time (especially in Internet Explorer).');

       //$('div.ns2-trace-text textarea').html(ajax_loading);
       
       // Uncheck the radio buttons for simulation mode -- this will force users
       // to select again if they runs the simulation again
       $('.trace-file-mode').removeAttr('checked');

       // Use AJAX to post the code
        $.ajax({
            type: 'POST',
            url: NS2_BASE_URL+'ns2_submit/',
            data: contents,
            cache: false,
            success: function(mesg, textStatus, XMLHttpRequest) {
                // Get the task #
                var jObj = $.parseJSON(mesg);
                var disp_mesg = 'Simulation # <b>' + jObj['id'] + '</b> has been submitted. \n\
                <br>The result will appear here shortly.'                               
                                                
                if ( jObj['id'] ) {
                    
                    // Display task #
                    $(document.createElement('p'))
                    .html(disp_mesg)
                    .css('text-align', 'center')
                    .attr('class', 'sim-start-mesg')
                    .appendTo ('div.ns2-code-output');
                    
                    /*
                     * Credits: https://github.com/blog/467-smart-js-polling
                     */
                    // Poll until task is done; then display the result
                    $.poll(INITIAL_POLL_INTERVAL, function(retry) {
                        
                        $.getJSON(NS2_BASE_URL + 'cel/state/' + jObj['id'] + '/', function(data) {
                            
                            if ( data['state'] && (data['state'].toUpperCase() == 'SUCCESS') ) {
                                //alert(data['state']);
                                $('p.sim-start-mesg')
                                .html('Simulation completed <br><b>Loading trace file ...</b>');
                                
                                $.getJSON(NS2_BASE_URL + 'cel/result/' + jObj['id'] + '/', function(result_data) {                                    
                                    var resultObj = result_data; 
                                    $('div.ns2-code-output').html(resultObj['mesg'].replace(/\n/g, '<br>'));                                    
                                    var output = '';
                                    for (var line_num in resultObj['trace']) {
                                        output += resultObj['trace'][line_num] + '';                                        
                                    }
                                    $('textarea.ns2-trace-text').val(output);
                                    $('textarea.ns2-trace-text').css('height', '250px');
                                    alert('Loaded trace file of size ' + $('.ns2-trace-text').val().length/1024.0 + ' KB');                
                                    $('.trace-file-mode').removeAttr('disabled');
                                })                                                                
                            } 
                            else {
                              retry();
                            }
                        })
                    })
                }                                                                      
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $('div.ns2-code-output').html('Error: ' + textStatus + '; ' +  errorThrown + '; ' +  XMLHttpRequest.responseText);
            },
            dataType: 'html'
        });
        return false;
    });

    /** */
    
    
    // Dialog to take input (or show textual output) for ns2 trace analysis    

    /*
     * Toolbar buttons
     */

    // Set the simulation mode when an option is selected
    // Initially, no mode is selected. For the first selection, toolbar buttons are
    // also to be displayed
    $('.trace-file-mode').click(function() {
        //alert('Click' + $(this).val());

        if ($(this).val() == 'Satellite') {
            alert('Please choose the \'Wired\' mode to analyze trace files for exercises on satellite networks.');
            return;
        }
        else if ($(this).val() == 'Mixed') {
            alert('This mode is currently not supported!');
            return;
        }

        $('.trace-file-mode').attr('disabled', 'true');
        $('.toolbar').css({visibility: 'visible'}).slideDown('slow');
        $.ajax({
            url:    NS2TRACE_URL + $(this).val() + '/' ,
            type:   'GET',
            success: function(mesg, txtStatus, XMLHttpRequest) {
                createSlidingDiv(mesg, 'Mode Changed', 5000);
                $('.trace-file-mode').removeAttr('disabled');

                //$('.toolbar').css('display', 'visible').slideDown('slow');
                $('.toolbar').css({visibility: 'visible'}).slideDown('slow');

            },
            error: function(XMLHttpRequest, txtStatus, errorThrown) {
                createSlidingDiv(errorThrown, 'Error', 0);
                $('.trace-file-mode').removeAttr('disabled');
            }
        });
    });


    // General statistics
    $('#gen-stats').click(function(event) {
        event.preventDefault();
        $.ajax({
            type:   'GET',
            url:    NS2TRACE_URL + 'general_stats/',
            success:function(mesg, textStatus, XMLHttpRequest) {
                createSlidingDiv(mesg, 'Title', 5000);
            },
            error:  function(XMLHttpRequest, textStatus, errorThrown) {
                createSlidingDiv('' + errorThrown, 'Error', 0);
            },
            dataType: 'html'
        });
    });

    // Average thruput for a given node
    $('#avg-thruput-dialog').click(function(event) {
        event.preventDefault();

        var container = $(document.createElement('div'));
        var label = $(document.createElement('label')).text('Please type in node # (starts from 0): ');
        var input = $(document.createElement('input'));
        input.attr({
            type:   'text',
            id:     'avg-thruput-node',
            'name':   'avg-thruput-node'
        }).css('width', '30px');
        $(container).append(label).append(input);

        var btn = $(document.createElement('input'));
        btn.attr({
            type:   'button',
            id:     'avg-thruput',
            value:  'Show'
        })
        .click(function() {
            var node_id = parseInt( $('#avg-thruput-node').val() ) ;
            if (isNaN(node_id) || node_id < 0) {
                alert('Node # can only be a non-negative integer -- please revise your input!');
                $('#avg-thruput-node').focus();
                $('#avg-thruput-node').val('');
                return;
            } else if (node_id > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#avg-thruput-node').val('');
                $('#avg-thruput-node').focus();
                return;
            }

            $(this).attr('disabled', 'true');
            $.ajax({
                type:   'GET',
                url:    NS2TRACE_URL + 'avg_thruput/' + node_id + '/',
                success:function(mesg, txtStatus, XMLHttpRequest) {
                    //$('#sim-avg-thruput-node').text(mesg);
                    createSlidingDiv(mesg, 'Average throughput of node #' + node_id + ' (in Kbps)', 5000);
                },
                error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                    createSlidingDiv('' + errorThrown, 'Error', 0);
                },
                dataType: 'html'
            });
        });
        $(container).append(btn);
        createSlidingDiv2(container, '', 0);
    });

    // End to end delay
    $('#e2e-delay-dialog').click(function(event) {
        event.preventDefault();

        var container = $(document.createElement('div'));
        var label = $(document.createElement('label')).text('Please type in source node # (starts from 0): ');
        var input = $(document.createElement('input'));  
        input.attr({
            type:   'text',
            id:     'e2e-delay-src-node',
            'name':   'e2e-delay-src-node'
        }).css('width', '30px');
        $(container).append(label).append(input);
        
        var label = $(document.createElement('label')).text('Please type in destination node # (starts from 0): ');
        var input = $(document.createElement('input'));
        input.attr({
            type:   'text',
            id:     'e2e-delay-dst-node',
            'name':   'e2e-delay-dst-node'
        }).css('width', '30px');
        $(container).append($('<br>')).append(label).append(input);
        
        // (Rev #28: #4)
        var label = $(document.createElement('label')).text('Please type in scaling factor [optional]: ');
        var input = $(document.createElement('input'));    
        input.attr({
            type:   'text',
            id:     'delay-scale',
            'name':   'delay-scale',
            value:  1
        }).css('width', '30px');    
        $(container).append($(document.createElement('br'))).append(label).append(input);

        var btn = $(document.createElement('input'));
        btn.attr({
            type:   'button',
            value:  'Plot',
            id:     'e2e-delay'
        })
        .click(function() {
            var src = parseInt( $('#e2e-delay-src-node').val() ) ;
            if (isNaN(src) || src < 0) {
                alert('Source node # can only be a non-negative integer -- please revise your input!');
                $('#e2e-delay-src-node').val('');
                $('#e2e-delay-src-node').focus();
                return;
            } else if (src > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#e2e-delay-src-node').val('');
                $('#e2e-delay-src-node').focus();
                return;
            }

            var dst = parseInt( $('#e2e-delay-dst-node').val() ) ;
            if (isNaN(dst) || dst < 0) {
                alert('Destination node # can only be a non-negative integer -- please revise your input!');
                $('#e2e-delay-dst-node').val('');
                $('#e2e-delay-dst-node').focus();
                return;
            } else if (dst > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#e2e-delay-dst-node').val('');
                $('#e2e-delay-dst-node').focus();
                return;
            }
            
            var scale = parseInt( $('#delay-scale').val() ) ;
            if (isNaN(scale) || scale == 0) {
                alert('Scale factor can only be a non-zero number -- please revise your input!');
                $('#delay-scale').val('');
                $('#delay-scale').focus();
                return;
            } 
            
            $(this).attr('disabled', 'true');
            
            $.ajax({
                type:   'GET',
                url:    NS2TRACE_URL + 'plot/end2end_delay/' + src + '/' + dst + '/' + scale,
                //url:    NS2TRACE_URL + 'plot/end2end_delay/0/3',
                success:function(mesg, txtStatus, XMLHttpRequest) {
                    createSlidingDiv(mesg, 'End-to-end delay between nodes ' + src + ' and ' + dst, 5000);
                    if (mesg['error'])
                        alert('Error:' + mesg['error']);
                    else
                        onDataReceived(mesg, 'Packet sequence #', 'End-to-end delay (in s)');
                },
                error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                    createSlidingDiv('' + errorThrown + txtStatus, 'Error', 0);
                },
                dataType: 'json'
            });
        });
        $(container).append(btn);

        createSlidingDiv2(container, '', 0);
    });

    // Packet retransmission
    $('#pkt-retransmit-dialog').click(function(event) {
        event.preventDefault();

        var container = $(document.createElement('div'));
        var label = $(document.createElement('label')).text('Please type in source node # (starts from 0): ');
        var input = $(document.createElement('input'));
        input.attr({
            type:   'text',
            id:     'pkt-retransmit-src-node',
            'name':   'pkt-retransmit-src-node'
        }).css('width', '30px');
        $(container).append(label).append(input);

        var label = $(document.createElement('label')).text('Please type in destination node # (starts from 0): ');
        var input = $(document.createElement('input'));
        input.attr({
            type:   'text',
            id:     'pkt-retransmit-dst-node',
            'name':   'pkt-retransmit-dst-node'
        }).css('width', '30px');
        $(container).append($('<br>')).append(label).append(input);

        var btn = $(document.createElement('input'));
        btn.attr({
            id:     'pkt-retransmit',
            value:  'Plot',
            type:   'button'
        });
        btn.click(function() {
            var src = parseInt( $('#pkt-retransmit-src-node').val() ) ;
            if (isNaN(src) || src < 0) {
                alert('Source node # can only be a non-negative integer -- please revise your input!');
                $('#pkt-retransmit-src-node').val('');
                $('#pkt-retransmit-src-node').focus();
                return;
            } else if (src > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#pkt-retransmit-src-node').val('');
                $('#pkt-retransmit-src-node').focus();
                return;
            }

            var dst = parseInt( $('#pkt-retransmit-dst-node').val() ) ;
            if (isNaN(dst) || dst < 0) {
                alert('Destination node # can only be a non-negative integer -- please revise your input!');
                $('#pkt-retransmit-dst-node').val('');
                $('#pkt-retransmit-dst-node').focus();
                return;
            } else if (dst > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#pkt-retransmit-dst-node').val('');
                $('#pkt-retransmit-dst-node').focus();
                return;
            }

            $(this).attr('disabled', 'true');
            $.ajax({
                type:   'GET',
                url:    NS2TRACE_URL + 'plot/pkt_retransmits/' + src + '/' + dst + '/',
                success:function(mesg, txtStatus, XMLHttpRequest) {
                    createSlidingDiv(mesg, 'Packet retransmission count between nodes ' + src + ' and ' + dst, 5000);
                    if (mesg['error'])
                        alert('Error:' + mesg['error']);
                    else
                        onDataReceived(mesg, 'Sequence #', '# of transmissions');
                },
                error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                    createSlidingDiv('' + errorThrown + txtStatus, 'Error', 0);
                },
                dataType: 'json'
            });
        });
        $(container).append(btn);

        createSlidingDiv2(container, '', 0);

    });

    // Bytes received
    $('#bytes-rcvd-dialog').click(function(event) {
        event.preventDefault();

        var container = $(document.createElement('div'));
        var label = $(document.createElement('label')).text('Please type in node # (starts from 0): ');
        $(container).append(label);
        
        var input = $(document.createElement('input'));
        input.attr({
            type:   'text',
            id:     'bytes-rcvd-node',
            'name':   'bytes-rcvd-node'
        }).css('width', '30px');
        $(container).append(input);
        $(container).append($('<br>'));

        var text = $(document.createElement('span')).text('(For wireless scenario) At layer: ');
        $(container).append(text);

        var chkbox = $(document.createElement('input'));
        chkbox.addClass('bytes-rcvd-layer');
        chkbox.attr({
            type:   'checkbox',
            'name':   'bytes-rcvd-layer',
            value:  'MAC'
        });
        var text = $(document.createElement('span')).text('MAC').css('padding-right', '4px');
        $(container).append(chkbox).append(text);

        var chkbox = $(document.createElement('input'));
        chkbox.addClass('bytes-rcvd-layer');
        chkbox.attr({
            type:   'checkbox',
            'name':   'bytes-rcvd-layer',
            value:  'RTR'
        });
        var text = $(document.createElement('span')).text('RTR').css('padding-right', '4px');
        $(container).append(chkbox).append(text);

        var chkbox = $(document.createElement('input'));
        chkbox.addClass('bytes-rcvd-layer');
        chkbox.attr({
            type:   'checkbox',
            'name':   'bytes-rcvd-layer',
            value:  'AGT'
        });
        var text = $(document.createElement('span')).text('AGT').css('padding-right', '4px');
        $(container).append(chkbox).append(text);

        var btn = $(document.createElement('input'));
        btn.attr({
            type:   'button',
            id:     'bytes-rcvd2',
            value:  'Plot'
        });
        btn.click(function() {
            var node_id = parseInt( $('#bytes-rcvd-node').val() ) ;
            if (isNaN(node_id) || node_id < 0) {
                alert('Node # can only be a non-negative integer (' + node_id + ') -- please revise your input!');
                $('#bytes-rcvd-node').val('');
                $('#bytes-rcvd-node').focus();
                return false;
            } else if (node_id > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#bytes-rcvd-node').val('');
                $('#bytes-rcvd-node').focus();
                return false;
            }

            $(this).attr('disabled', 'true');

            // Trace levels
            var trace_levels = '';  // An empty string -- no spaces
            $('.bytes-rcvd-layer').each(function() {
                if ($(this).is(':checked')) {
                    trace_levels += $(this).val() + '|'
                }
            });

            var url = NS2TRACE_URL + 'plot/bytes_rcvd/' + node_id + '/';
            if (trace_levels != '')
                url += trace_levels + '/';
            else
                url += 'X/';

            $('div.slide-dialog').remove();
            
            $.ajax({
                type:   'GET',
                url:    url,
                success:function(mesg, txtStatus, XMLHttpRequest) {
                    //createSlidingDiv(mesg, 'Bytes received by node #' + node_id, 5000);
                    if (mesg['error'])
                        alert('Error: ' + mesg['error']);
                    else
                        onDataReceived(mesg, 'Time (in s)', 'Kbits received');
                },
                error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                    createSlidingDiv('' + errorThrown, 'Error', 0);
                },
                dataType: 'json'
            });
        })
        $(container).append(btn);

        createSlidingDiv2(container, '', 0);
    });

    // Clear session (trace file name and mode)
    $('#clear-session').click(function(event) {
        event.preventDefault();
        $.ajax({
            url:    NS2TRACE_URL + 'clear_session/',
            type:   'GET',
            success:function(mesg, txtStatus, XMLHttpRequest) {
                createSlidingDiv(mesg, '', 5000);
            },
            error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                createSlidingDiv('' + errorThrown, 'Error', 0);
            },
            dataType: 'html'
        })
    });


    // (Rev #28: #3)
    // # Of hops vs. packet sequence # plot
    $('#hop-cnt-vs-seq-num-dialog').click(function(event) {
        event.preventDefault();

        var container = $(document.createElement('div'));
        var label = $(document.createElement('label')).text('Please type in source node # (starts from 0): ');
        var input = $(document.createElement('input'));
        var label2 = $(document.createElement('label')).text('Please type in source port # (starts from 0): ');
        var input2 = $(document.createElement('input'));
        var label3 = $(document.createElement('label')).text('Please type in destination node # (starts from 0): ');
        var input3 = $(document.createElement('input'));
        var label4 = $(document.createElement('label')).text('Please type in destination port # (starts from 0): ');
        var input4 = $(document.createElement('input'));
        
        input.attr({
            type:   'text',
            id:     'src-node',
            'name':   'src-node'
        }).css('width', '30px');
        input2.attr({
            type:   'text',
            id:     'src-port',
            'name':   'src-port',
            value:  0
        }).css('width', '30px');
        input3.attr({
            type:   'text',
            id:     'dst-node',
            'name':   'dst-node'
        }).css('width', '30px');
        input4.attr({
            type:   'text',
            id:     'dst-port',
            'name':   'dst-port',
            value:  0
        }).css('width', '30px');
        $(container).append(label).append(input);
        $(container).append($('<br>')).append(label2).append(input2);
        $(container).append($('<br>')).append(label3).append(input3);
        $(container).append($('<br>'))
        .append(label4)
        .append(input4)    
        .append( $(document.createElement('div'))
                .text('Please turn MAC trace on for wireless scenarios')
                .css('border-top', '1px dotted silver')
        );

        var btn = $(document.createElement('input'));
        btn.attr({
            type:   'button',
            id:     'hop-count',
            value:  'Plot'
        })
        .click(function() {
            var src_node = parseInt( $('#src-node').val() ) ;
            if (isNaN(src_node) || src_port < 0) {
                alert('Node # can only be a non-negative integer -- please revise your input!');
                $('#src-node').focus();
                $('#src-node').val('');
                return;
            } else if (src_node > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#src-node').val('');
                $('#src-node').focus();
                return;
            }
            var src_port = parseInt( $('#src-port').val() ) ;
            if (isNaN(src_port) || src_port < 0) {
                alert('Port # can only be a non-negative integer -- please revise your input!');
                $('#src_port').focus();
                $('#src_port').val('');
                return;
            }
            var dst_node = parseInt( $('#dst-node').val() ) ;
            if (isNaN(dst_node) || dst_node < 0) {
                alert('Node # can only be a non-negative integer -- please revise your input!');
                $('#dst-node').focus();
                $('#dst-node').val('');
                return;
            } else if (dst_node > MAX_NODES) {
                alert('Sorry, currently we can support upto 100 nodes!');
                $('#dst-node').val('');
                $('#dst-node').focus();
                return;
            }
            var dst_port = parseInt( $('#dst-port').val() ) ;
            if (isNaN(dst_port) || dst_port < 0) {
                alert('Port # can only be a non-negative integer -- please revise your input!');
                $('#dst_port').focus();
                $('#dst_port').val('');
                return;
            }

            $(this).attr('disabled', 'true');
            var url = NS2TRACE_URL + ['plot/hop_cnt_seq_num', src_node, src_port, dst_node, dst_port].join('/');        
            $.ajax({
                type:   'GET',
                url:    url,
                success:function(mesg, txtStatus, XMLHttpRequest) {
                    //$('#sim-avg-thruput-node').text(mesg);
                    createSlidingDiv(mesg, 'Hop count vs. packet sequence # plot', 5000);
                    if (mesg['error'])
                        alert('Error: ' + mesg['error']);
                    else
                        onDataReceived(mesg, 'Packet sequence #', 'Hop count');
                },
                error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                    createSlidingDiv('' + errorThrown, 'Error', 0);
                },
                dataType: 'json'
            });
        });
        $(container).append(btn);
        createSlidingDiv2(container, '', 0);
    });

    // Filter the output of simulation based on search pattern
    $('#filter-btn').click(function(event) {
        var count = 0;
        var pattern = $.trim( $('#filter-pattern').val() );
        
        if (pattern.length == 0) {
            alert('Please type in a pattern to search!');
            $('#filter-pattern').focus();
            return;            
        }

        var inputs = [];
        var output = '';        
        var contents = $('.ns2-code-output').html();
        if ( contents.search('<br>') >= 0 )
            inputs = contents.split('<br>');
        else
            inputs = contents.split('<BR>');    // Stupid IE           
                
        for (var i in inputs) {
            if ( inputs[i].match(pattern) ) {
                ++count;            
                output = [ output, inputs[i] ].join('<br>');                
            }
        }      

        $('.filtered-output').html( output );                    
        $('#pattern-match-count').text(count);
    });


    $('#custom-plot').click(function(e) {
        e.preventDefault();
        // Read the inputs from the text area, and store them in 
        // [ [x1, y1], [x2, y2], ... ] format
        
        if (! $('#custom-plot-data').val() ) {
            alert('Please type in some data to be plotted!')
            return;
        }
        var plot_label = ( $('#plot-label').val().length ? $('#plot-label').val() : 'plot-label' );
        var x_axis_label = ( $('#x-axis-label').val().length ? $('#x-axis-label').val() : 'x-axis' );
        var y_axis_label = ( $('#y-axis-label').val().length ? $('#y-axis-label').val() : 'y-axis' );
        
        var input_data = $('#custom-plot-data').val().split('\n');
        var data = [];
        
        for (var i = 0; i < input_data.length; i++) {
            var line = $.trim( input_data[i] );
            
            if ( ! line.length || line.indexOf(',') < 0 )
                continue;
            
            var xval = line.split(',')[0];
            var yval = line.split(',')[1];
            data.push( [xval, yval] );
        }        
        
        var mesg = {
            'data': data,
            'label': plot_label
        }
        onDataReceived(mesg, x_axis_label, y_axis_label);        
    });
});
