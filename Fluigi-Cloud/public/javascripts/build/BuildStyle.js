//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size

$(function() {
    $('#side-menu').metisMenu();
});

$(function() {
    $(window).bind("load resize", function() {
        var topOffset = 50;
        var width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        var height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url;
    }).addClass('active').parent();

    while (true) {
        if (element.is('li')) {
            element = element.parent().addClass('in').parent();
        } else {
            break;
        }
    }
});

$(function(){$("#side-menu").metisMenu()}),$(function(){$(window).bind("load resize",function(){var i=50,n=this.window.innerWidth>0?this.window.innerWidth:this.screen.width;n<768?($("div.navbar-collapse").addClass("collapse"),i=100):$("div.navbar-collapse").removeClass("collapse");var e=(this.window.innerHeight>0?this.window.innerHeight:this.screen.height)-1;e-=i,e<1&&(e=1),e>i&&$("#page-wrapper").css("min-height",e+"px")});for(var i=window.location,n=$("ul.nav a").filter(function(){return this.href==i}).addClass("active").parent();;){if(!n.is("li"))break;n=n.parent().addClass("in").parent()}});
