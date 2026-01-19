import reflex as rx
from app.states.nav_state import NavState


def sidebar_item(item: dict) -> rx.Component:
    """Renders a single sidebar navigation item."""
    is_active = NavState.active_item == item["label"]
    return rx.el.button(
        rx.icon(
            item["icon"],
            class_name=rx.cond(
                is_active, "text-teal-600", "text-gray-400 group-hover:text-gray-600"
            ),
            size=20,
        ),
        rx.el.span(
            item["label"],
            class_name=rx.cond(
                is_active,
                "font-medium text-teal-900",
                "font-medium text-gray-600 group-hover:text-gray-900",
            ),
        ),
        on_click=lambda: NavState.set_active(item["label"]),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-4 py-3 bg-teal-50 border-r-4 border-teal-600 w-full transition-all duration-200 cursor-pointer relative",
            "flex items-center gap-3 px-4 py-3 hover:bg-gray-50 w-full transition-all duration-200 group cursor-pointer border-r-4 border-transparent relative",
        ),
    )


def sidebar() -> rx.Component:
    """The main sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("book-a", class_name="text-white fill-current", size=24),
                class_name="bg-gradient-to-br from-teal-500 to-teal-700 p-2 rounded-lg shadow-md",
            ),
            rx.el.span(
                "Inventory",
                class_name="text-2xl font-bold tracking-tight text-gray-900 font-['Inter']",
            ),
            class_name="flex items-center gap-3 px-6 py-8 mb-2",
        ),
        rx.el.nav(
            rx.foreach(NavState.menu_items, sidebar_item),
            class_name="flex flex-col gap-1 py-2 flex-1 w-full",
        ),
        rx.el.div(
            rx.el.div(class_name="h-px bg-gray-100 my-2 mx-4"),
            rx.el.button(
                rx.icon(
                    "settings",
                    size=20,
                    class_name="text-gray-400 group-hover:text-gray-600",
                ),
                rx.el.span(
                    "Settings",
                    class_name="font-medium text-gray-600 group-hover:text-gray-900",
                ),
                on_click=lambda: NavState.set_active("Settings"),
                class_name="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 w-full transition-all duration-200 group cursor-pointer",
            ),
            rx.el.button(
                rx.icon(
                    "log-out",
                    size=20,
                    class_name="text-red-400 group-hover:text-red-600",
                ),
                rx.el.span(
                    "Logout",
                    class_name="font-medium text-gray-600 group-hover:text-red-700",
                ),
                class_name="flex items-center gap-3 px-4 py-3 hover:bg-red-50 w-full transition-all duration-200 group cursor-pointer mb-6",
            ),
            class_name="mt-auto w-full",
        ),
        class_name="hidden md:flex flex-col w-64 h-screen bg-white border-r border-gray-200 fixed left-0 top-0 z-20 shadow-sm",
    )