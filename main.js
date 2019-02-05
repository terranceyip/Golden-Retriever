active = "1";

function tabClicked(e) {
	var tabVal = $(this).attr("id");
	var sel = "#" + active;
	$(sel).removeClass("active");
	active = tabVal;
	sel = "#" + active;
	$(sel).addClass("active");
	if (active == "1") {
		changePage("upload.html")
	} else if (active == "2") {
		changePage("status.html")
	} else if (active == "3") {
		changePage("map.html")
	}
}

function changePage(file) {
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", file);
	rawFile.onreadystatechange = function () {
		if (rawFile.readyState === 4) {
			if (rawFile.status === 200 || rawFile.status == 0) {
				var allText = rawFile.responseText;
				var divider = $(".content");
				divider.html(allText);
				if (file == "map.html") {
					map();
				}
			}
		}
	}
	rawFile.send(null);
}

/**
 * Setup all visualization elements when the page is loaded.
 */
function map() {
	// Connect to ROS.
	var ros = new ROSLIB.Ros({
		url: 'ws://192.168.137.66:9090'
	});

	// Create the main viewer.
	var viewer = new ROS2D.Viewer({
		divID: 'map',
		width: 750,
		height: 750
	});

	// Setup the map client.
	var gridClient = new ROS2D.OccupancyGridClient({
		ros: ros,
		rootObject: viewer.scene,
		// Use this property in case of continuous updates            
		continuous: true
	});
	// Scale the canvas to fit to the map
	gridClient.on('change', function () {
		viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height);
		viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
	});
}

$(document).ready(function () {
	/* Set up handlers */
	$(".tab").click(tabClicked); // Handle clicks on "credit cards"
}
);