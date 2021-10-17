import vlc
Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(r'file:///C:/Users/aviro/Desktop/Video%20Player%20QT5/UI/Stream%20Testing/the-100.mp4')
Media.get_mrl()

player.set_media(Media)
player.play()
while True:
    pass
