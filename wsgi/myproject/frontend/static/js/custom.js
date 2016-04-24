var map;

var latLng, geoIpData, geoOptions = {
    enableHighAccuracy: false,
    timeout: 5000, // Wait 5 seconds
    maximumAge: 300000 //  Valid for 5 minutes
};

var userLocationFound = function(position){
    latLng = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
    centerMap(latLng);
    window.console.log("User confirmed! Location found: " + latLng.lat + ", " + latLng .lng);
}

// Fallback to London, UK
var userLocationNotFound = function(){

    if (geoIpData) {
        latLng = {
            lat: geoIpData.lat, // fallback lat
            lng: geoIpData.lon  // fallback lng
        }
        $('#location').val(geoIpData.city + ", " + geoIpData.country);
    } else {
        latLng = {
            lat: 51.500152, // fallback lat
            lng: -0.126236  // fallback lng
        };
    }
    centerMap(latLng);
    window.console.log("Fallback set: ", latLng, geoIpData);
}

var geoIp = function(){
    $.getJSON("http://ip-api.com/json/?callback=?", function(data) {
        geoIpData = data;
    });
}

var centerMap = function(location) {
    if (map) {
        var position = new google.maps.LatLng(location.lat, location.lng);
        map.setCenter(position);
        //loadNearbyItems(location);
    }
}

setTimeout(function () {
    if (!latLng) {
        window.console.log("No confirmation from user, using fallback");
        userLocationNotFound();
    }
}, geoOptions.timeout + 1000); // Wait extra second


function initialize() {
    var mapOptions = {
        zoom: 11,
        styles:[{
            featureType: "poi",
            stylers: [{visibility: "off" }]
        }]
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    window.navigator.geolocation.getCurrentPosition(userLocationFound, userLocationNotFound, geoOptions);
}

function handleNoGeolocation() {
    var options = {
        map: map,
        position: new google.maps.LatLng(60, 105)
    };

    var infowindow = new google.maps.InfoWindow('Unable to detect your location');
    map.setCenter(options.position);
}
function drawMarker(item)
{
    var infowindow = new google.maps.InfoWindow();
    var itemPos = new google.maps.LatLng(
            item.location.lat_position,
            item.location.long_position
            );
    var marker = new google.maps.Marker({
        position: itemPos,
        map: map,
        title: item.name,
        icon: '/thumb/circle/' + item.id + '/25.png'
    });
    google.maps.event.addListener(marker, 'click', (function(marker, item) {
        return function() {
            infowindow.setContent(
                '<div class="info"><h3>' + item.name + '</h3> \
                <a onclick="iWantThis(\'' + Base64.encode(JSON.stringify(item)) + '\')"> \
                <div class="iWantThis"><button class=\"btn btn-primary\">' + gettext('I want this!') + '</button></div> \
                </a>\
                <div id="' + item.id + '" class="popupImage"> \
                <img src="' + item.image + '" alt="' + item.name + '" class="img-item img-circle"/> \
                <div> \
                <h5>' + gettext('Description') + '</h5> \
                <p> ' + item.description + '</p></div>'
                );
            infowindow.open(map, marker);
        }
    })(marker, item));
}

function addToGrid(item) {
    var tmp = $.templates('#itemsListTmpl');
    var html = tmp.render({
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "location": item.location.location,
        "created": $.format.date(item.created, 'dd/MM/yyyy HH:mm:ss'),
        "data": Base64.encode(JSON.stringify(item)),
    });
    $('#itemsGrid').append(html);
}
function loadNearbyItems(position) {
   $.getJSON("/api/items?lat=" + position.lat +  "&lon=" + position.lng, function(data) {
       for (var i in data) {
           var item = data[i];
           //console.log(item);
           drawMarker(item);
           addToGrid(item);
       }
   });
}

function showTooltip(element, msg)
{
    $(element)
        .tooltip({"trigger":"manual", "title": msg})
        .tooltip('show');
    setTimeout(function(){
        $(element).tooltip('hide')
    }, 1000);
}

function showAlert(element, type, heading, message)
{
    var template = '<div class="alert alert-{{:type}}" id="{{:type}}-alert"> \
            <button type="button" class="close" data-dismiss="alert">x</button> \
                <strong>{{:heading}}</strong> {{:message}} \
        </div>';
    var tmp = $.templates(template);
    var html = tmp.render({"type": type, "message": message, "heading": heading});
    $(element).html(html);
    $("#" + type + "-alert").alert();
    $("#" + type + "-alert").fadeTo(2000, 500).slideUp(500, function() {
        $("#" + type + "-alert").alert('close');
    });
}

function iWantThis(item) {
    var item = jQuery.parseJSON(Base64.decode(item));
    item.created = $.format.date(item.created, 'dd/MM/yyyy HH:mm:ss');
    console.log(item);
    var template = $.templates('#iWantThisTmpl');
    $('#iWantThisModal').html(template.render(item)).modal('show');
    $('.img-container img').magnify();

    if (item.expires_on) {
        $('#iWantThisExpiresBlock').removeClass('hidden');
        $('#iWantThisExpiresOn')
            .countdown(
                    $.format.date(item.expires_on, 'yyyy/MM/dd HH:mm:ss'),
                    function(event) {
                        $(this).text(
                            event.strftime('%D ' + gettext('days') + ' %H:%M:%S')
                        );
                    }
            );
    }
    $('#iWantThisRate').rating({'size':'xs', 'showCaption': false, 'clearButton': ''});
    $('.rating-container').attr('data-toggle', 'tooltip');
    $('.rating-container').attr('data-placement', 'bottom');
    //$('.rating-container').attr('title', 'test!!!');
    $('#iWantThisRate').rating('update', item.user_rating);
    $('#iWantThisRate').on('rating.change', function(event, value) {
        $.ajax({
            dataType: "json",
            url: "/vote/" + item.id + '/?punctuation=' + value,
            success: function(data) {
                $('#iWantThisRate').rating('update', data.rating);
                showTooltip('.rating-container', gettext("Thanks for your vote!"));
            },
            error: function (e, msg) {
                var errorMsg = $.parseJSON(e.responseText);
                $('#iWantThisRate').rating('update', item.user_rating);
                showTooltip('.rating-container', errorMsg ? errorMsg['error'] : e.responseText);
            }
        });
    });
    $('#iWantThisRate').on('rating.clear', function(event) {
        console.log("rating.clear");
    });

    $('#iWantThisContact').click(function() {
        var id = $('#iWantThisId').val();
        console.log('clicked!', id);

        var message = $('#iWantThisComment').val();
        if (!$('#iWantThisComment').val()) {
            message = $('#iWantThisComment').attr('placeholder');
        }
        console.log(JSON.stringify({"message": message}));
        $.ajax({
            type: "POST",
            url: '/request/' + id + '/',
            dataType: 'json',
            async: false,
            data: JSON.stringify({"message": message}),
            success: function (data) {
                console.log(data);
                var msg = gettext('We have contacted the owner of the item regarding your interest in this item. Hopefully, he will get back to you shortly.');
                showAlert('#iWantThisMsg', 'success', 'Success!', msg);
                $('#iWantThisContact').attr('disabled', true);
            },
            error: function(data, errorMsg) {
                var msg = data.responseText;
                // CSRF Verification fail, not logged in
                if (data.status == 403) {
                    msg = gettext('Please, log in first and try again.');
                } else {
                    var errorMsg = $.parseJSON(e.responseText);
                    msg = errorMsg ? errorMsg['error'] : errorMsg;
                }
                showAlert('#iWantThisMsg', 'danger', 'Error!', msg);
            }
        })
    return true;
    });
}
function createItem() {
    $('#createItemModal').modal('show');
}

var giveAwayItemSubmit = function (node) {
    if (!$('#location').val()) {
        $('#lat_position').val(latLng.lat);
        $('#long_position').val(latLng.lng);
    } else {
        $('#lat_position').val('');
        $('#long_position').val('');
    }

    var formData = new FormData($(node)[0]);

    $.ajax({
        url: '/api/items',
        type: 'POST',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        success: function (response) {
            var msg = gettext('Thank you. Your item will be reviewed and pushed to live within the next 24 hours.');
            showAlert('#giveAwayItemMsg', 'success', gettext('Success!'), msg);
            $(node)[0].reset();
        },
        error: function (response) {
            showAlert('#giveAwayItemMsg', 'danger', gettext('Error!'), gettext('An error ocurred, please try again'));
        }
    });
}

var options = {
    labels: {
        'name': gettext('Name'),
        'description': gettext('Description'),
        'image': gettext('Image'),
        'expires_on': gettext('Expires On'),
        'category': gettext('Category')
    },
    submit: {
        settings: {
            allErrors: true,
            errorListClass: "alert alert-danger",
        },
        callback: {
            onSubmit: giveAwayItemSubmit
        }
    }
};

$(document).ready(function() {
    geoIp();
    $.ajaxSetup({
        headers: { "X-CSRFToken": $.cookie("csrftoken") }
    });
    $('[data-toggle="popover"]').popover().on('click', function() { $("#q").focus(); });
    $('.datetimepicker').datetimepicker({format:'Y-m-d H:i'});

    // Locale for validation messages
    $.alterValidationRules({
            rule: 'NOTEMPTY',
            message: gettext('$ must not be empty')
    });
    $('#giveAwayItemForm').validate(options);

    // New item form submission
    $('.createItem').click(createItem);
    // Contact Us form
    $("#contactUsForm").submit(function( event ) {
        event.preventDefault();
        $.ajax({
            url: '/contact-us/',
            type: 'POST',
            data: $($(this)[0]).serialize(),
            success: function (response) {
                showAlert('#contactUsMsg', 'success', gettext('Success!'), gettext('Message successfully sent'));
                $($(this)[0]).reset();
            },
            error: function (response) {
                showAlert('#contactUsMsg', 'danger', gettext('Error!'), gettext('An error ocurred, please try again'));
            }
        });
    });

});

if ($('#map-canvas').length == 1) {
    initialize();
}
