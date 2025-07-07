from pygame import Rect

def center_text(screen, text, width, height, fontsize=25, font="bitcount", color="black", padding=40):
    rect_width = width - padding * 2
    rect_height = fontsize * 4  # espaço para até 3–4 linhas
    top = height // 2 - rect_height // 2

    safe_rect = Rect(padding, top, rect_width, rect_height)

    screen.draw.textbox(
        text,
        safe_rect,
        fontname=font,
        color=color,
        anchor=(0.5, 0.5)
    )
