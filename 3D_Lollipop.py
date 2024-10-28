import math
import cairo

WIDTH, HEIGHT = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)


def draw_lollipop_head(context, center_x, center_y, radius):
    # Create radial gradient for the lollipop head
    gradient = cairo.RadialGradient(center_x - radius * 0.5, center_y - radius * 0.5, radius * 0.2,
                                    center_x, center_y, radius)
    gradient.add_color_stop_rgb(1, .55, .14, .11)
    gradient.add_color_stop_rgb(0, 1, 0.5, 0)   #Orange
    gradient.add_color_stop_rgb(.5, 1, 0.35, 0)   #Orange
    gradient.add_color_stop_rgb(1, .9, 0.45, 0.27)   #Yellow highlights
    gradient.add_color_stop_rgb(1, 1, 0.5, 0.27)   #Yellow highlights
    gradient.add_color_stop_rgb(1, 1, 0.8, 0.2)   #Yellow highlights
    gradient.add_color_stop_rgb(.9, 0.7, 0.2, 0.2)   # Red shadows

    context.set_source(gradient)
    context.arc(center_x, center_y, radius,0, 2 * math.pi)
    context.fill()


def draw_lollipop_stick(context, center_x, center_y, stick_height):
    stick_x = center_x - 15         # Centers the stick
    stick_y_start = center_y + 98   # Starts below the lollipop head
    stick_y_end = stick_y_start + stick_height

    context.set_source_rgba(1, .9, 0.45, 0.27)
    context.move_to(stick_x + 2, stick_y_start + 2)
    context.rectangle(stick_x, stick_y_start, 33, stick_height)
    context.fill()
    # Draw stick with linear gradient for a 3D effect

    gradient = cairo.LinearGradient(stick_x, stick_y_start, stick_x, stick_y_end )

    gradient.add_color_stop_rgb(.01, .4, .2, .07)
    gradient.add_color_stop_rgb(.05, .55, .30, .09)
    gradient.add_color_stop_rgb(.18, .88, .69, .59)
    gradient.add_color_stop_rgb(.3, .96, .85, .77)
    gradient.add_color_stop_rgb(.5, 1, 1, 1)

    context.set_source(gradient)
    context.rectangle(stick_x, stick_y_start, 30, stick_height)

    context.fill()


def draw_glowing_text(context, text, x, y):
    context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(70)

    # Set glow effect with a blurred shadow
    context.set_source_rgba(1, .9, 0.45, 0.27)
    context.move_to(x + 5, y + 5)
    context.show_text(text)

    context.set_source_rgba(1, 1, 1) # Yellow text color
    context.move_to(x, y)
    context.show_text(text)

# Background
context.set_source_rgba(0, 0, 0)
context.paint()

# Draw lollipop
base_radius = 100
draw_lollipop_head(context, WIDTH // 2, HEIGHT // 2 - 100, 200)
draw_lollipop_stick(context, WIDTH //2, HEIGHT // 2, 400)

draw_glowing_text(context, "THE", WIDTH // 2  + 45 , HEIGHT - 120 )
draw_glowing_text(context, "LOLLIPOP", WIDTH // 2 + 50 , HEIGHT - 40 )

# Write to PNG
surface.write_to_png('3D_Lollipop.png')
print("3D lollipop image created!")