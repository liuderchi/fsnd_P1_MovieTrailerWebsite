"""entertainment_center.py

Created Date: 20151031
Credits: adarsh0806 @Github
Repo: https://github.com/adarsh0806/ud036_StarterCode
Description: UDND P1. Use following code to generate a HTML file
"""

import webbrowser
import os
import re
import media # user defined media module from media.py

# Styles and scripting for the page
# Use triple single quotes to escape double quotes
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Welcome to my entertainment center!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">My Entertainment Center</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
    <p style="text-align: left">{storyline}</p>
</div>
'''


def create_movie_tiles_content(movies):
    """Generates HTML content of movie media."""
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            storyline=movie.storyline
        )
    return content


def open_movies_page(movies):
    """Generates main page HTML file and opens in browser.

    Final HTML page is generated by joining header,
    base-content and movie_tiles_content.
    """
    # Create or overwrite the output file
    output_file = open('entertainment_center.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))
    # format() usage: https://docs.python.org/2/library/stdtypes.html#str.format
    # "The sum of 1 + 2 is {0}".format(1+2)

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)


movie_i_robot = media.Movie("I, Robot",
                            ("In 2035 a technophobic cop investigates a crime "
                            "that may have been perpetrated by a robot, which "
                            "leads to a larger threat to humanity."),
                            "https://upload.wikimedia.org/wikipedia/en/3/3b/Movie_poster_i_robot.jpg",
                            "https://www.youtube.com/watch?v=rL6RRIOZyCM")

movie_big_hero_6 = media.Movie("Big Hero 6",
                                ("The special bond that develops between "
                                "plus-sized inflatable robot Baymax, and prodigy"
                                " Hiro Hamada, who team up with a group of friends"
                                " to form a band of high-tech heroes."),
                                "https://upload.wikimedia.org/wikipedia/en/4/4b/Big_Hero_6_%28film%29_poster.jpg",
                                "https://www.youtube.com/watch?v=rD5OA6sQ97M")

movie_minions = media.Movie("Minions",
                            ("Minions Stuart, Kevin and Bob are recruited by "
                            "Scarlett Overkill, a super-villain who, alongside "
                            "her inventor husband Herb, hatches a plot to take "
                            "over the world."),
                            "https://upload.wikimedia.org/wikipedia/en/3/3d/Minions_poster.jpg",
                            "https://www.youtube.com/watch?v=o8hxFE7RpSg")

movies = [movie_i_robot, movie_big_hero_6, movie_minions]
print('Generating web page of your %d movies...' %  len(movies) )
open_movies_page(movies)
