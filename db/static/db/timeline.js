
d3.json("/?json2", function (error, jData) {

    var isMouseClick = false,
        startPosition = 0,
        lastMouseDelta = 0,
        parseDate = d3.time.format("%Y-%m-%d").parse;

    var svg = d3.select(".timeline").append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .on("mousemove", mousemove)
        .on("mousedown", function () { isMouseClick = true; startPosition = d3.event.clientY; })
        .on("mouseup", function () { isMouseClick = false; lastMouseDelta += (startPosition - d3.event.clientY) * -1 });

    var line = svg.append("line")
        .attr("x1", "50%")
        .attr("y1", "0")
        .attr("x2", "50%")
        .attr("y2", "100%");

    var container = svg.append('g');


    if (error) throw error;
    jData.forEach(function (d) {
        d.y = parseDate(d.y);
        d.cnt = d.cnt;
    });

    jData.sort(function (a, b) {
        return a.y - b.y;
    });
    var options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };

    cont = container
        .append("text")
        .selectAll("tspan")
        .data(jData)
        .enter()
        .append("tspan")
        .attr("x", "30%")
        .attr("y", function (d, i) { return i * 25 + "px" })
        .text(function (d) { return d.y.toLocaleString("ru", options) });

    grap = container
        .selectAll("rect")
        .data(jData)
        .enter()
        .append("rect")
        .attr("width", function (d, i) { return d.cnt / 10 + "px" })
        .attr("height", "25px")
        .attr("x", "50%")
        .attr("y", function (d, i) { return i * 25 + "px" });

    var rect = svg.append("rect")
        .attr("width", "50%")
        .attr("height", "20%")
        .attr("x", "35%")
        .attr("y", "50%")
        .attr("rx", "5")
        .attr("ry", "5");

    var text_prev = svg.append("text")
        .attr('class', "shadow")
        .attr("x", "40%")
        .attr("y", "55%");

    var text = svg.append("text")
        .attr("x", "40%")
        .attr("y", "60%");

    var text_post = svg.append("text")
        .attr('class', "shadow")
        .attr("x", "40%")
        .attr("y", "65%");

    function getText(id) {
        var n_text = grap[0][id].__data__.n;
        return n_text.length > 20 ? n_text.substring(0, 35) + "..." : n_text;
    }

    function heightInPersent(d) { return d * 100 + "%"; }

    function mousemove() {
        if (isMouseClick) {
            mouseDelta = lastMouseDelta + (startPosition - d3.mouse(this)[1]) * -1;
            container.transition()
                .duration(1500)
                .ease("elastic")
                .attr("transform", "translate(0," + mouseDelta + ")");
            var n_id = Math.abs(Math.floor(mouseDelta / 15));
            text_prev.text(getText(n_id - 1));
            text.text(getText(n_id));
            text_post.text(getText(n_id + 1));
        }
    }
})



