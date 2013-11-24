<script src="/js/jquery-1.7.1.min.js"></script>
<script src="/js/typed.js" type="text/javascript"></script>
<script>
    $(function(){
        $.getJSON("/tweets/${CHAPTER}").done(function(data) {
            $("#${TYPED_DIV_VAL}").typed({
                strings: data['tweet_msgs'],
                typeSpeed: 20,
                backTypeSpeed: 5,
                backDelay: 500,
                loop: false,
                loopCount: false,
                callback: function(){ 
                    $("#${LINK_DIV_VAL}").html(data['next_link']); 
                }
            });
        });
    });
    function OpenInNewTab(url )
    {
      var win=window.open(url, '_blank');
      win.focus();
    }
</script>
