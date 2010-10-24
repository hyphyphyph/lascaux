jQuery.fn.clearonfocus = function() {
  jQuery(this)
      .bind('focus', function() {
          // Set the default value if it isn't set
          if ( !this.defaultValue ) this.defaultValue = this.value;
          // Check to see if the value is different
          if ( this.defaultValue && this.defaultValue != this.value ) return;
          // It isn't, so remove the text from the input
          this.value = '';
      })
      .bind('blur', function() {
          // If the value is blank, return it to the defaultValue
          if ( this.value.match(/^\s*$/) )
              this.value = this.defaultValue;
      });
};

(function(A) {
    A.fn.hasEvent = function(C) {
       var B = this.data("events");
       return( B && B[C] )
    }
}) (jQuery)

var characteristics = (function(){
    var c = {},
        index = 1,
        html;
    
    function updateIndex() {
        $('#characteristics_highest_index').val(index);
        index = index+1;
    }
    
    function createNewCharacteristic(domElement) {
        html = '<div class="char-set">';
        html += '<div class="widget textfield"><label for="char_attr_'+index+'">Question</label><input type="text" name="char_attr_'+index+'" value="" /></div>';
        html += '<div class="widget textfield"><label for="char_val_'+index+'">Answer</label><input type="text" name="char_val_'+index+'" value="" /></div>';
        html += '<div class="actions">';
        html += '<a href="#" class="delete" id="delChar-'+index+'">Delete</a>';
        html += '</div>';
        html += '</div>';
        
        $(html).insertAfter(domElement).children();
        $('#delChar-'+index).bind('click', function() {
            $(this).parent().parent().remove();
            return false;
        });
        
        updateIndex();
    }
    
    c.init = function() {        
        $('.actions .add').bind('click', function() {
            createNewCharacteristic( $(this).parent().parent() );
            return false;
        });
    };
    
    return c;
}());

var map = (function(){
    var m = {},
        map,
        marker,
        domId = 'map',
        geocoder = new google.maps.Geocoder(),
        defaultLat = 45.504298,
        defaultLng = -73.579691,
        defaultCoord = defaultLat+','+defaultLng,
        overlays = [];
         
    function addMarker(location) {
        marker = new google.maps.Marker({
            position: location,
            map: map,
            //draggable: true
        });
        overlays.push(marker);
        
        //google.maps.event.addListener(marker, 'dragend', function() {
        //    
        //});
    }
    
    function deleteOverlays() {
      if (overlays) {
        for (i in overlays) {
          overlays[i].setMap(null);
        }
        overlays.length = 0;
      }
    }
    
    function populateLatLngFields(lat, lng) {
        $('#locationLat').val(lat);
        $('#locationLng').val(lng);
    }
    
    function placeMarker(address) {
        if( address !== $('#searchLocation').val() ) return;
        deleteOverlays();
        geocoder.geocode( { 'address': address }, function(results, status) {
              if (status == google.maps.GeocoderStatus.OK) {
                  map.setCenter(results[0].geometry.location);
                  $('#searchLocation').parent().removeClass('error');
                  addMarker( results[0].geometry.location );
                  populateLatLngFields(results[0].geometry.location.lat(), results[0].geometry.location.lng());
              } else {
                  $('#searchLocation').parent().addClass('error');
              }
            });
        addMarker();
    }
    
    m.init = function() {
        var latlng = new google.maps.LatLng(defaultLat, defaultLng);
        var myOptions = {
            zoom: 14,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById(domId), myOptions);
        
        addMarker(latlng);
        
        $('#searchLocation').bind('keyup', function() {
            var address = $('#searchLocation').val()
            setTimeout(function () { placeMarker( address ) }, 500);
        });
        
    };
    
    return m;
}());
