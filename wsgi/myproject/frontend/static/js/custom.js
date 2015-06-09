var map;

var latLng, geoOptions = {
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
    latLng = {
        lat: 51.500152, // fallback lat
        lng: -0.126236  // fallback lng
    };
    centerMap(latLng);
    window.console.log("Fallback set: ", latLng);
}

var centerMap = function(location) {
    if (map) {
        var position = new google.maps.LatLng(location.lat, location.lng);
        map.setCenter(position);
        loadNearbyItems(location);
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
        zoom: 12
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

function loadNearbyItems(position) {
   var infowindow = new google.maps.InfoWindow();
   $.getJSON("/api/items?lat=" + position.lat +  "&lon=" + position.lng, function(data) {
       for (var i in data) {
           var item = data[i];
           console.log(item);
           var itemPos = new google.maps.LatLng(
               item.location.lat_position,
               item.location.long_position
               );

           var marker = new google.maps.Marker({
                  position: itemPos,
                  map: map,
                  title: item.name,
                  icon: '/static/img/marker.png'
           });
           google.maps.event.addListener(marker, 'click', (function(marker, i) {
               return function() {
                   infowindow.setContent(
                       '<h3>' + data[i].name + '</h3> \
                       <a onclick="iWantThis(\'' + escape(JSON.stringify(data[i])) + '\')"> \
                       <div class="iWantThis"><button class=\"btn btn-primary\">I want this!</button></div> \
                       </a>\
                       <div id="' + data[i].id + '" style="width:100%;text-align:center"> \
                       <!--<img id="loading-' + data[i].id + '" src="img/loading.gif" align="middle" alt="Loading..." style="margin-top:5px"/>--> \
                       <img src="' + data[i].image + '" alt="' + data[i].name + '" style="margin-top:5px" width="200" height="200" class="img-circle"/> \
                       <div> \
                       <h5>Description</h5> \
                       <p> ' + data[i].text + '</p>'
                       );
                   infowindow.open(map, marker);
                   //api.getInfoPoint(points.stations[i].station_code, points.stations[i].lines);
               }
           })(marker, i));
       }
   });
}

function iWantThis(item) {
    $('#iWantThisSuccessMsg').hide();
    $('#iWantThisErrorMsg').hide();
    console.log('iwanthis clicked');
    var item = jQuery.parseJSON(unescape(item));
    console.log(item);
    var template = $.templates('#iWantThisTmpl');
    $('#iWantThisModal').html(template.render(item)).modal('show');
    $('#iWantThisContact').click(function() {
        var id = $('#iWantThisId').val();
        console.log('clicked!', id);
        console.log(JSON.stringify({"message": $('#iWantThisComment').val()}));
        $.ajax({
            type: "POST",
            url: '/request/' + id + '/',
            dataType: 'json',
            async: false,
            data: JSON.stringify({"message": $('#iWantThisComment').val()}),
            success: function (data) {
                console.log(data);
                $('#iWantThisSuccessMsg').show();
                $('#iWantThisSuccessMsg .msg').html('We have contacted the owner of the item regarding your interest in this item. Hopefully, he will get back to you shortly.');
            },
            error: function(data, errorMsg) {
                console.log(data);
                console.log(errorMsg);
                $('#iWantThisErrorMsg').show();
                $('#iWantThisErrorMsg .msg').html(data.responseText);
            }
        })
    return true;
    });
}
function createItem() {
    $('#createItemModal').modal('show');
}

var giveAwayItemSubmit = function (node) {
    $('#giveAwayItemSuccessMsg').hide();
    $('#giveAwayItemErrorMsg').hide();

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
            $('#giveAwayItemSuccessMsg .msg').html('Thank you. Your item will be reviewed and pushed to live within the next 24 hours.');
            $('#giveAwayItemSuccessMsg').show();
            $(node)[0].reset();
        },
        error: function (response) {
            console.log(response);
            $('#giveAwayItemErrorMsg .msg').html('An error ocurred, please try again');
            $('#giveAwayItemErrorMsg').show();
        }
    });
}

var options = {
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
    $.ajaxSetup({
        headers: { "X-CSRFToken": $.cookie("csrftoken") }
    });
    if ($('#map-canvas').length == 1) {
        initialize();
    }
    $('#giveAwayItemForm').validate(options);
    $('#createItem').click(createItem);
});


