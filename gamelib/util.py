def center_sprite(sprite, x=False, y=False):
    img = sprite.image
    if x is False:
        img.anchor_x = img.width / 2
    else:
        img.anchor_x = x
    if y is False:
        img.anchor_y = img.height / 2
    else:
        img.anchor_y = y
    return sprite

