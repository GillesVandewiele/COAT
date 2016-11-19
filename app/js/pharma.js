var app = angular.module('pharma', []);

app.controller('pharmaController', ['$scope','$http', function($scope, $http) {

	$('#routeUpload').change(function(e) {
		var file = e.target.files[0];

		  var reader = new FileReader();
		  reader.onload = function(progressEvent){
		  	route_file = ''
		    // By lines
		    var lines = this.result.split('\n');
		    for(var line = 0; line < lines.length; line++){
		      route_file += lines[line];
		    }
		  	drawMap(route_file);
		  };
		  reader.readAsText(file);
	});

	var getSessions = function(training_csv){

	}

	$('#trainingUpload').change(function(e) {

		$scope.sessions = {}
		var file = e.target.files[0];

		Papa.parse(file, {
			complete: function(results) {
				columns = results.data[0];
				for (i = 1; i < results.data.length; i++) { 
					entry = results.data[i];
					console.log(entry[0] in $scope.sessions);
					if (!(entry[0] in $scope.sessions)){
						if(entry[1] != ''){
							$scope.sessions[entry[0]] = {}
							$scope.sessions[entry[0]]['name'] = entry[1]
							$scope.sessions[entry[0]]['trainTime'] = entry[2]
							$scope.sessions[entry[0]]['trainBPM'] = entry[3]
							$scope.sessions[entry[0]]['trainZone'] = entry[4]
							$scope.sessions[entry[0]]['blocks'] = []
							if (entry[5] != ''){
								$scope.sessions[entry[0]]['repetitions'] = entry[5]
								console.log($scope.sessions[entry[0]]['blocks']);
								$scope.sessions[entry[0]]['blocks'].push({'blockTime': entry[6], 'blockBPM': entry[7], 'blockZone': entry[8]})
							}
						} 
					} else if (entry[6] != ''){
						$scope.sessions[entry[0]]['blocks'].push({'blockTime': entry[6], 'blockBPM': entry[7], 'blockZone': entry[8]})
					}
				}
				console.log($scope.sessions);
				$scope.$apply();
			}
		});

		$('#questionairePanel').show();
	});

	$('#questionaireBtn').click(function(e) {
		$('#posteriorPanel').show();
	});

	$scope.loadSession = function(key){
		$scope.activeSession = $scope.sessions[key];
		// Generate the timeline
		timeline = []
		if($scope.activeSession['blocks'].length > 1){

		} else {
			totalDuration = $scope.activeSession['trainTime'];
			nrParts = $scope.activeSession['repetitions'] + 2;
			durationPart = totalDuration / nrParts;
			timeline.push({'time': 0, 'zone': $scope.activeSession['trainZone']});
			for (i = 0; i < nrParts; i++) { 
				timeline.push({'time': , 'zone':});
			}
		}
	}

	var drawMap = function(gpx){
		if($scope.mymap != undefined) $scope.mymap.remove();
		$scope.mymap = L.map('mapid').setView([0, 0], 3);

		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}).addTo($scope.mymap);

		new L.GPX(gpx, {async: true}).on('loaded', function(e) {
		  $scope.mymap.fitBounds(e.target.getBounds());
		}).addTo($scope.mymap);
	};

	var drawLineChart = function(id, data_file){
		var svg = d3.select(id),
	    margin = {top: 20, right: 20, bottom: 30, left: 50},
	    width = +$(id).parent().width()/2 - margin.left - margin.right,
	    height = +$(id).parent().height()/1.2 - margin.top - margin.bottom,
	    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		var parseTime = d3.timeParse("%d-%b-%y");

		var x = d3.scaleTime()
		    .rangeRound([0, width]);

		var y = d3.scaleLinear()
		    .rangeRound([height, 0]);

		var line = d3.line()
		    .x(function(d) { return x(d.date); })
		    .y(function(d) { return y(d.close); });

		d3.tsv(data_file, function(d) {
		  d.date = parseTime(d.date);
		  d.close = +d.close;
		  return d;
		}, function(error, data) {
		  if (error) throw error;

		  x.domain(d3.extent(data, function(d) { return d.date; }));
		  y.domain(d3.extent(data, function(d) { return d.close; }));

		  g.append("g")
		      .attr("class", "axis axis--x")
		      .attr("transform", "translate(0," + height + ")")
		      .call(d3.axisBottom(x));

		  g.append("g")
		      .attr("class", "axis axis--y")
		      .call(d3.axisLeft(y))
		    .append("text")
		      .attr("fill", "#000")
		      .attr("transform", "rotate(-90)")
		      .attr("y", 6)
		      .attr("dy", "0.71em")
		      .style("text-anchor", "end")
		      .text("Price ($)");

		  g.append("path")
		      .datum(data)
		      .attr("class", "line")
		      .attr("d", line);
		});
	}

	drawLineChart('#priorLine', '../data/line.tsv');
	drawLineChart('#posteriorLine', '../data/line.tsv');

	$("input[type='image']")
    .focus(function() { $(this).css("border","solid 1px #f00"); })
    .blur(function() { $(this).css("border","0"); });
	
}]);