import os
import mpd
import tornado.httpserver
import tornado.web

PORT = 8080
URI = "https://17813.live.streamtheworld.com/KUOWFM_HIGH_MP3.mp3"
DEBUG = False

def DBG(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

#--------------------------------------------------------------------
# M P D
#--------------------------------------------------------------------
mpc = mpd.MPDClient()

def mpd_init():
    """Initialize MPD."""
    mpc.connect("localhost", 6600)
    mpc.stop()
    mpc.clear()
    mpc.add(URI)
    mpc.close()
    mpc.disconnect()

def mpd_stop():
    """Stop playback."""
    try:
        mpc.connect("localhost", 6600)
        mpc.stop()
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_play():
    """Play specified track index."""
    try:
        mpc.connect("localhost", 6600)
        mpc.play()
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_change_vol(amount):
    """Change volume by amount in percent."""
    try:
        mpc.connect("localhost", 6600)
        mpc.volume(amount)
        mpc.close()
        mpc.disconnect()
    except:
        pass

#--------------------------------------------------------------------
# T O R N A D O
#--------------------------------------------------------------------
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web_radio.html")

class ButtonHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        DBG("GET")
        try:
            btn_id = int(self.get_argument("btn_id"))
            DBG("btn_id:", btn_id)
            if btn_id==1:
                mpd_stop()
            if btn_id==2:
                mpd_play()
            if btn_id==3:
                mpd_change_vol(10)
            if btn_id==4:
                mpd_change_vol(-10)
        except MissingArgumentError:
            pass

class MainServerApp(tornado.web.Application):
    """Main Server application."""
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
            (r"/button", ButtonHandler),
        ]

        tornado.web.Application.__init__(self, handlers)

#--------------------------------------------------------------------
# M A I N
#--------------------------------------------------------------------
if __name__ == '__main__':
    mpd_init()
    tornado.httpserver.HTTPServer(MainServerApp()).listen(PORT)
    print("Server starting on", PORT)
    tornado.ioloop.IOLoop.instance().start()