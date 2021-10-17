import vlc
Instance = vlc.Instance()
player = Instance.media_player_new()
# Media = Instance.media_new('http://localhost/postcard/GWPE.avi')
Media = Instance.media_new_path('the-100.mp4')
print(Media.get_mrl())
print(dir(Media))
player.set_media(Media)
player.play()
while True:
    pass