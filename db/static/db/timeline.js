
var isMouseClick = false,
    startPosition = 0,
    lastMouseDelta = 0,
    parseDate = d3.time.format("%Y-%m-%d").parse;

var svg = d3.select(".timeline").append("svg")
    .attr("width", "100%")
    .attr("height", "100%")

var line = svg.append("line")
    .attr("x1", "50%")
    .attr("y1", "0")
    .attr("x2", "50%")
    .attr("y2", "100%");

var container = svg.append('g');

d3.json("/?json2", function (error, jData) {

    if (error) throw error;

    svg.on("mousemove", mousemove)
        .on("mousedown", function () { isMouseClick = true; startPosition = d3.event.clientY; })
        .on("mouseup", function () { isMouseClick = false; lastMouseDelta += (startPosition - d3.event.clientY) * -1 });



    jData.forEach(function (d) {
        d.y = parseDate(d.y);
        d.cnt = d.cnt;
    });

    jData.sort(function (a, b) {
        return a.y - b.y;
    });

    rect_width = d3.scale.linear().range([5, 45]);

    rect_width.domain(d3.extent(jData, function (d) { return d.cnt; }));

    var options = {
        //year: 'numeric',
        month: 'long',
        day: 'numeric'
    };

    cont = container
        .append("text")
        .attr("class", "date")
        .selectAll("tspan")
        .data(jData)
        .enter()
        .append("tspan")
        .attr("x", "40%")
        .attr("y", function (d, i) { return i * 25 + "px" })
        .text(function (d, i) { return i % 5 ? " " : d.y.toLocaleString("ru", options) });

    grap = container
        .selectAll("rect")
        .data(jData)
        .enter()
        .append('a')
        .attr('xlink:href', '/')
        .append("rect")
        .attr("width", function (d) { return rect_width(d.cnt)+"%" } )
        .attr("class", "cnt_rect")
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
        .attr('class', "title shadow")
        .attr("x", "40%")
        .attr("y", "55%");

    link_to_news = svg
        .append('a')
        .attr('xlink:href', '/')

    text = link_to_news
        .append("text")
        .attr("class", "title")
        .attr("x", "40%")
        .attr("y", "60%");

    var text_post = svg.append("text")
        .attr('class', "title shadow")
        .attr("x", "40%")
        .attr("y", "65%");

    function getText(id) {
        if (id < 0 || id >= grap[0].length) return " ";
        var n_text = grap[0][id].__data__.n;
        return n_text.length > 20 ? n_text.substring(0, 35) + "..." : n_text;
    }

    function getUrl(id) {
        if (id < 0 || id >= grap[0].length) return "/";
        return "/news/id" + grap[0][id].__data__.i;
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

            link_to_news.attr("href", getUrl(n_id));
        }
    }
})



