<script src="/js/jquery-1.7.1.min.js"></script>
<script src="/js/typed.js" type="text/javascript"></script>
<script>

    $(function(){
        $.getJSON("/tweets/${CHAPTER}/${OFFSET}").done(function(data) {
            
            function UpdateTweetUrlsByIndex(index) {
                // index is 1-based
                $('.with-icn.retweet.js-tooltip').attr('href', '/chapter/${CHAPTER}/' + index);
                $('.with-icn.js-action-reply.js-tooltip').attr('href', data['tweet_urls'][index-1]);
            }
            UpdateTweetUrlsByIndex(${OFFSET});
            $("#${TYPED_DIV_VAL}").typed({
                strings: data['tweet_msgs'],
                typeSpeed: 20,
                backTypeSpeed: 5,
                backDelay: 500,
                loop: false,
                loopCount: false,
                inter_callbefore: function(self) {
                        index = self.arrayPos + 1 + (${OFFSET} - 1);
                        UpdateTweetUrlsByIndex(index);
                    }, // call before each item in strings
                callback: function(){ 
                    $("#${LINK_DIV_VAL}").html(data['next_link']); 
                }
            });
        });
        $('.prev_chapter').html('${PREV_CHAPTER}');
        $('.next_chapter').html('${NEXT_CHAPTER}');

    });

    function OpenInNewTab(url )
    {
      var win=window.open(url, '_blank');
      win.focus();
    }

    function PauseButtonClicked() {
        val = $('.typing-status').html();
        $('.typing-status').html(val == "Play " ? play_int() : play_pause());
    }

    function play_int() {
        $('.typing-status').html("Pause");
        // do play
    }

    function play_pause() {
        $('.typing-status').html("Play ");
        // do pause
    }

</script>
