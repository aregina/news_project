
var isMouseClick = false,
    previosMousePosition = 0,
    timeLinePosition = 0,
    parseDate = d3.time.format("%Y-%m-%d").parse;

const elementHeight = 25;
const linePosition = 50;
const dateDistanse = 5;
const graphWidth = (100-linePosition)-10


var svg = d3.select(".timeline").append("svg")
    .attr("width", "100%")
    .attr("height", "100%")

var line = svg.append("line")
    .attr("x1", linePosition + "%")
    .attr("y1", "0")
    .attr("x2", linePosition + "%")
    .attr("y2", "100%");

var container = svg.append('g');

d3.json("/?json2", function (error, jData) {
    if (error) throw error;

    svg.on("mousemove", mousemove)
        .on("mousedown", function () {
            isMouseClick = true;
            previosMousePosition = d3.event.clientY;
        })
        .on("mouseup", function () {isMouseClick = false;});

    jData.forEach(function (d) {
        d.y = parseDate(d.y);
        d.cnt = d.cnt;
    });

    jData.sort(function (a, b) {
        return a.y - b.y;
    });

    jData.reverse();

    var rect_width = d3.scale
        .linear()
        .range([1, graphWidth])
        .domain(d3.extent(jData, function (d) { return d.cnt; }));

    var options = {
        //year: 'numeric',
        month: 'long',
        day: 'numeric'
    };

    var pubDate = container
        .append("text")
        .attr("text-anchor","end")
        .attr("class", "date")
        .selectAll("tspan")
        .data(jData)
        .enter()
        .append("tspan")
        .attr("x", (linePosition-1)+"%")
        .attr("y", function (d, i) { return i * elementHeight + "px" })
        .text(function (d, i) { return i % dateDistanse ? " " : d.y.toLocaleString("ru", options) });

    var graphic = container
        .selectAll("rect")
        .data(jData)
        .enter()
        .append('a')
        .attr('xlink:href', '/')
        .append("rect")
        .attr("width", function (d) { return rect_width(d.cnt) + "%" })
        .attr("class", "cnt_rect")
        .attr("height", elementHeight + "px")
        .attr("x", linePosition + "%")
        .attr("y", function (d, i) { return i * elementHeight + "px" });

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
        if (id < 0 || id >= graphic[0].length) return " ";
        var n_text = graphic[0][id].__data__.n;
        return n_text.length > 20 ? n_text.substring(0, 35) + "..." : n_text;
    }

    function getUrl(id) {
        if (id < 0 || id >= graphic[0].length) return "/";
        return "/news/id" + graphic[0][id].__data__.i;
    }

    function mousemove() {
        if (isMouseClick) {
            var currPos = d3.mouse(this)[1];
            moveTimeLine((previosMousePosition - currPos))
            previosMousePosition = currPos;
        }
    }
    
    function moveTimeLine(delta) {
        timeLinePosition += -delta
        container.transition()
                .duration(1500)
                .ease("elastic")
                .attr("transform", "translate(0," + timeLinePosition + ")");
        var n_id = Math.floor(timeLinePosition / elementHeight) * -1;
        text_prev.text(getText(n_id - 1));
        text.text(getText(n_id));
        text_post.text(getText(n_id + 1));

        link_to_news.attr("href", getUrl(n_id));
    }
    
    var timer = setInterval(
        function(){
            moveTimeLine(elementHeight);
        },
        1000
    )
})



