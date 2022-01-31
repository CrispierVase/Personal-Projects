import pyglet

win = pyglet.window.Window()
label = pyglet.text.Label('Hello World',
    font_name='Arial',
    font_size=28,
    x=win.width // 2,
    y=win.height // 2,
    anchor_x='center',
    anchor_y='center'
    )

@win.event
def on_draw():
    win.switch_to()
    win.dispatch_events()
    print('?')
    win.clear()
    label.draw()

pyglet.app.run()