import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
from pathlib import Path

# allow user to resize
# add menu bar
# add more pillow things


def update_image(original, blur, contrast, emboss, contour, flipx, flipy):
    global image
    image = original.filter(ImageFilter.GaussianBlur(blur))
    image = image.filter(ImageFilter.UnsharpMask(contrast))

    if emboss:
        image = image.filter(ImageFilter.EMBOSS())
    if contour:
        image = image.filter(ImageFilter.CONTOUR())
    if flipx:
        image = ImageOps.mirror(image)
    if flipy:
        image = ImageOps.flip(image)

    bio = BytesIO()
    image.save(bio, format='PNG')

    window['-IMAGE-'].update(data=bio.getvalue())


image_path = sg.popup_get_file(
    'Open', no_window=True, file_types=(('PNG Files', '.png'),))


def show_GUI_info(settings):
    sg.popup_scrolled(settings, title='Current GUI Settings')


def main_window():

    # Menu Bar
    menu_def = [
        ['Help', ['About', 'GUI Info', 'Exit',]],
    ]

    # GUI
    controls_col = sg.Column([
        [sg.Frame("Blur", layout=[
                  [sg.Slider(range=(0, 10), orientation="horizontal", key="-BLUR-")]])],
        [sg.Frame("Contrast", layout=[
                  [sg.Slider(range=(0, 10), orientation="horizontal", key="-CONTRAST-")]])],
        [sg.Checkbox("Emboss", key="-EMBOSS-"),
         sg.Checkbox("Contour", key="-CONTOUR-")],
        [sg.Checkbox("Flip X", key="-FLIPX-"),
         sg.Checkbox("Flip Y", key="-FLIPY-")],
        [sg.Button("Exit", key='-EXIT-', button_color='red'), sg.Button("Save", key="-SAVE-", button_color='green')]])

    image_col = sg.Column([[sg.Image(image_path, key='-IMAGE-')]])

    layout = [[[sg.MenubarCustom(menu_def)], controls_col, image_col]]

    original = Image.open(image_path)
    global window
    window = sg.Window("Python PNG Editor", layout, use_custom_titlebar=True)

    while True:
        event, values = window.read(timeout=50)
        if event == sg.WIN_CLOSED:
            break
        update_image(
            original,
            values['-BLUR-'],
            values['-CONTRAST-'],
            values['-EMBOSS-'],
            values['-CONTOUR-'],
            values['-FLIPX-'],
            values['-FLIPY-']
        )

        if event == 'About':
            window.disappear()
            sg.popup('Version 1.0', 'This program allows users to quickly edit PNG files',
                     'Built with Python and PySimpleGUI')
            window.reappear()

        if event == 'GUI Info':
            show_GUI_info(settings)

        if event == 'Exit':
            window.close()

        if event == '-SAVE-':
            save_path = sg.popup_get_file(
                'Save', save_as=True, no_window=True) + '.png'
            image.save(save_path, 'PNG')

        if event == '-EXIT-':
            window.close()

    window.close()


if __name__ == '__main__':
    settings_path = Path.cwd()
    settings = sg.UserSettings(path=settings_path, filename='config.ini',
                               use_config_file=True, convert_bools_and_none=True)
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    main_window()
