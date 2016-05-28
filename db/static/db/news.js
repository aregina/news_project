const linePosition = 50;
const emoLineTop = 10;
const lineStart = 20;
const lineStop = 80;

var svg = d3.select(".svg").append("svg")
    .attr("width", "100%")
    .attr("height", "100%")

var line_h = svg.append("line")
    .attr("x1", lineStart + "%")
    .attr("y1", emoLineTop + "%")
    .attr("x2", lineStop + "%")
    .attr("y2", emoLineTop + "%");

var line = svg.append("line")
    .attr("x1", linePosition + "%")
    .attr("y1", (5 + emoLineTop) + "%")
    .attr("x2", linePosition + "%")
    .attr("y2", 95 + "%");

var img_1 = svg.append("image")
    .attr("x", 15 + "%")
    .attr("y", emoLineTop + "%")
    .attr("height", "30px")
    .attr("width", "30px")
    .attr("xlink:href", "/static/db/happy.svg")
    .attr("transform", "translate(-15,-15)");;

var img_1 = svg.append("image")
    .attr("x", 85 + "%")
    .attr("y", emoLineTop + "%")
    .attr("height", "30px")
    .attr("width", "30px")
    .attr("xlink:href", "/static/db/sad.svg")
    .attr("transform", "translate(-15,-15)");



var parseDate = Date.parse
var jDD = new Object;
var timeline = d3.time.scale()
    .range([5 + emoLineTop, 95]);

function startOfDay(date) {
    return new Date(date.getFullYear(),
        date.getMonth(),
        date.getDate());
}

function endOfDay(date) {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59);
}


d3.json("?json", function (error, jData) {
    if (error) throw error;

    var options = {
        month: 'long',
        day: 'numeric'
    };

    jData.forEach(function (d) {
        d.date = new Date(parseDate(d.date));
        var news_date = d.date.toLocaleString("ru", options);
        if (!jDD.hasOwnProperty(news_date)) 
            jDD[news_date] = new Array;
        jDD[news_date].push(d);
    });

    jData.sort(function (a, b) {
        return a.date - b.date;
    });

    timeline.domain([startOfDay(jData[0].date),
        endOfDay(jData[jData.length - 1].date)]);

    var newDate = new Date();
    newDate.setTime(jData[0].date.getTime());
    
    var rectHeight = Math.min(3, (timeline(newDate.setDate(newDate.getDate() + 1)) - timeline(jData[0].date)));
    var dateDistanse = 7


    c = svg.append("g")
        .selectAll('rect')
        .data(Object.keys(jDD))
        .enter()
        .append("rect")
        .attr("x", linePosition + "%")
        .attr("y", function (d) {
            var startDay = startOfDay(jDD[d][0].date);
            return timeline(startDay) + "%";
        })
        .attr("width", function (d) { return (jDD[d].length * 2) + "%" })
        .attr("height", rectHeight + "%")
        .attr("class", "news_line");

    var t = svg.append("g");
    
    var tg = t.append("text")
        .attr("class", "date");
        
    var tgg = tg.selectAll("tspan")
        .data(Object.keys(jDD))
        .enter()
        .append("tspan")
        .attr("x", linePosition + "%")
        .attr("y", function (d) {
            var startDay = startOfDay(jDD[d][0].date);
            return timeline(startDay) + "%";
        })
        .text(function (d, i) { return i % dateDistanse ? " " : d });

    tg.attr("text-anchor", "end")
        .attr("transform", "translate(-5,7)");
});
