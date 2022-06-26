
from Views.menu import MenuViews
from Controllers.menu_control import MenuController


def main():
    MenuViews.application_title()
    MenuController().main_menu_start()


if __name__ == "__main__":
    main()
