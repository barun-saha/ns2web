// DOM ready

$(document).ready(function() {

    var NS2_BASE_URL = '/ns2web/ns2web/';
    // Dev
    //var NS2_BASE_URL = '/ns2web/';
    
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

    /**
    **/


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

       //$('div.ns2-code-output').empty();
       $('div.ns2-code-output').text('');
       $('textarea.ns2-trace-text').text('');
       
       var contents = {'ns2code': editAreaLoader.getValue('ns2code')}; 
       $('div.ns2-code-output').text(contents);

       if ( ! $('input[@name="trace-file-mode"]:checked').val() ) {
            alert('Please specify a simulation mode (to determine the output trace file format)!');
            return false;
       }

       // Now determine what are the metrics set for analysis, if any

       var all_metrics = [];
       $('#analysis-metrics div').each(function(index) {
            var this_metric = $.trim( $(this).text() );
            if ( this_metric.length > 0 ) {
                //alert( this_metric );
                var json_obj = $.parseJSON(this_metric);
                //all_metrics.push( json_obj );
                all_metrics.push( this_metric );
                //alert(json_obj['name']);
            }            
       });

       //contents['metrics'] = all_metrics;
       contents = { 'ns2code': editAreaLoader.getValue('ns2code'), 'metrics': JSON.stringify(all_metrics) };
               
               
       var ajax_loading = $(document.createElement('img'));
       ajax_loading
       .attr({'src': MEDIA_PREFIX+'images/ajax/ajax_loader.gif', 'alt': 'Loading ...'})
       .css({
                'width': 'auto', 'height': 'auto', 
                'border': 0, 'margin': 0, 
                'padding-left': '44.5%', 'padding-right': '44.5%', 'padding-top': '25px', 'padding-bottom': '25px'
       })
       

       //$('div.ns2-trace-text textarea').html(ajax_loading);
       
       // Uncheck the radio buttons for simulation mode -- this will force users
       // to select again if they runs the simulation again
       //$('.trace-file-mode').removeAttr('checked');
       // alert( JSON.stringify(contents['metrics']) );
       // Use AJAX to post the code
       $('div.ns2-code-output').html('');
       $('div.ns2-code-output').append(ajax_loading);
       $('textarea.ns2-trace-text')
       .val('Please be patient -- running the simulation and loading the trace file could take considerable amount of time (especially in Internet Explorer).');
       
        $.ajax({
            type: 'POST',
            url: NS2_BASE_URL+'batch/ns2_submit/',
            data: contents,
            cache: false,
            success: function(mesg, textStatus, XMLHttpRequest) {
                // Get the task #
                var jObj = $.parseJSON(mesg);
                //alert(jObj['id']);                                              
                                                
                if ( jObj['id'] ) {                    
                    var disp_mesg = '<p>Simulation has been submitted. Please click on your <b><a href="' + NS2_BASE_URL +
                                    'batch/result/' + 
                                    jObj['id'] + 
                                    '/">job ID</a></b> to view the results.</p>';
                                
                    // Display task #
                    $('div.ns2-code-output')
                    .html(disp_mesg)
                    .css('text-align', 'center')
                    .addClass('sim-start-mesg');                                     
                    
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

        //$('.trace-file-mode').attr('disabled', 'true');
        $('.toolbar').css({visibility: 'visible'}).slideDown('slow');        
    });


    // General statistics
    /*
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
    */

    // Average thruput for a given node
    /*
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
    */

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
            
            //$(this).attr('disabled', 'true');                  
            var metric_json = {'name': 'e2e-delay', 'parameters': [src, dst, scale], 'mode': $('input[@class=trace-file-mode]:checked').val() };
            
            $('#analysis-metrics').append(
                $(document.createElement('div'))
                .css({'margin-bottom': '10px'})
                .text( JSON.stringify(metric_json) )
            );
            
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

            //$(this).attr('disabled', 'true');            
            var metric_json = {'name': 'pkt-retransmission', 'parameters': [src, dst], 'mode': $('input[@class=trace-file-mode]:checked').val() };
            
            $('#analysis-metrics').append(
                $(document.createElement('div'))
                .css({'margin-bottom': '10px'})
                .text( JSON.stringify(metric_json) )
            );
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
                alert('Node # must be a non-negative integer -- please revise your input!');
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

            //var url = NS2TRACE_URL + 'bytes_rcvd/' + node_id + '/';
            //if (trace_levels != '')
            //    url += trace_levels + '/';

            $('div.slide-dialog').remove();     

            var metric_json = {'name': 'bytes-rcvd', 'parameters': [node_id, trace_levels], 'mode': $('input[@class=trace-file-mode]:checked').val() };
            
            $('#analysis-metrics').append(
                $(document.createElement('div'))
                .css({'margin-bottom': '10px'})
                .text( JSON.stringify(metric_json) )
            );                   
            
        })
        $(container).append(btn);

        createSlidingDiv2(container, '', 0);
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

            //$(this).attr('disabled', 'true');
            var metric_json = {'name': 'hop-count', 'parameters': [src_node, src_port, dst_node, dst_port], 'mode': $('input[@class=trace-file-mode]:checked').val()};
            
            $('#analysis-metrics').append(
                $(document.createElement('div'))
                .css({'margin-bottom': '10px'})
                .text( JSON.stringify(metric_json) )
            );
        });
        
        $(container).append(btn);
        createSlidingDiv2(container, '', 0);
    });
    
});
