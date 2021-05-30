// make wss later
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

$("#send-oz-response").click(function(){
    // TODO: top send button from working and change class to disabled
    var send_button_element = document.getElementById( 'send-oz-response' );
    if (send_button_element.classList.contains('disabled')) {
        console.log("Send button enabled, cannot click");
    }
    else {
        // Disable send
        send_button_element.classList.add('disabled');
        console.log("Send button disabled until get new msg from helpee");

        // Get oz_response and clear contents in textarea
        var oz_response = $('#oz-response').val();
        console.log("You clicked send " + oz_response);
        document.getElementById( 'oz-response' ).value = "";

                // Get image values
        var style = getComputedStyle(document.body);
        var image_values = {
            "ol":document.getElementById('olslider').value,
            "ow":document.getElementById('owslider').value,
            "oh":document.getElementById('ohslider').value,
            "sf":document.getElementById('sfslider').value
        };

        // Build message
        var msg = {
            'from': 'Student',
            'text': oz_response,
            'image': image_values
        };

        // Send message via websocket
        chatSocket.send(JSON.stringify(msg));
        console.log("Oz response sent. " + JSON.stringify(msg));
    }
});

// when receive message
chatSocket.onmessage = function(event) {
    console.log("Received message: " + event.data);
    if (JSON.parse(event.data).from=="Teacher") {
        // Add user/teacher response as a new bubble under the other bubbles
        var new_bubble ;
        new_bubble = document.createElement( 'div' );
        new_bubble.className = 'bubble1 p-2 m-0 position-relative';
        new_bubble.setAttribute('data-author', 'Teacher');
        new_bubble.innerHTML = '<a class="float-right">' + JSON.parse(event.data).text + '</a>' ;
        var bubbles_block ;
        container_block = document.getElementById( 'bubbles' );
        container_block.appendChild( new_bubble );
    }

    if (JSON.parse(event.data).from=="Student") {
        // Add student response as a new bubble under the other bubbles
        new_bubble = document.createElement( 'div' );
        new_bubble.className = 'bubble2 p-2 m-0 position-relative';
        new_bubble.setAttribute('data-author', 'Student');
        new_bubble.innerHTML = '<a id="thinking" class="float-left">' + JSON.parse(event.data).text + '</a>' ;
        var bubbles_block ;
        bubbles_block = document.getElementById( 'bubbles' );
        bubbles_block.appendChild( new_bubble );
    }

    if (JSON.parse(event.data).from=="Helpee") {
        // Add response to textarea, enable Send button.
        document.getElementById( 'oz-response' ).value = JSON.parse(event.data).text;
        document.getElementById( 'send-oz-response' ).classList.remove('disabled');
    }

    if (JSON.parse(event.data).from=="System") {
        // Add student response as a new user bubble under the other bubbles
        new_bubble = document.createElement('div');
        new_bubble.className = 'alert alert-warning';
        new_bubble.innerHTML = JSON.parse(event.data).text;
        var bubbles_block;
        bubbles_block = document.getElementById('bubbles');
        bubbles_block.appendChild(new_bubble);
        var send_button_element = document.getElementById('send-user-response');
        if (send_button_element.classList.contains('disabled')) {
            console.log("Send button already disabled");
        } else {
            send_button_element.classList.add('disabled');
            console.log("Send button now disabled");
        }
    }
    // update image
    do_when_new_img_data_recieved(JSON.parse(event.data).image);


    // Scroll to bottom
    var bubbles_block ;
    bubbles_block = document.getElementById( 'bubbles' );
    var bubbles_block_height = bubbles_block.scrollHeight;
    //console.log("Height = " + bubbles_block_height);
    bubbles_block.scrollTop = bubbles_block_height; // Not moving the scrollbar :(
    document.getElementById( 'bubbles_container' ).scrollTop = bubbles_block_height;
};


// when error
chatSocket.onerror = function(event) {
    console.error("WebSocket error observed:", event);
    var thinking_bubble;
    thinking_bubble = document.getElementById('thinking');
    thinking_bubble.innerHTML = "Error occurred communicating with the server :( <br>Make sure you are connected to the internet and try again";
    thinking_bubble.id = "donethinking";
};

// when closed
chatSocket.onclose = function(event) {
    console.error('WebSocket closed unexpectedly: '+ event.data);
};
