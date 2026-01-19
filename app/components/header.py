import reflex as rx
from app.states.nav_state import NavState


def header() -> rx.Component:
    """The top header component with search and profile."""
    return rx.el.header(
        rx.el.div(
            rx.icon(
                "search",
                class_name="text-gray-400 absolute left-4 top-1/2 -translate-y-1/2",
                size=20,
            ),
            rx.el.input(
                placeholder="Global search...",
                on_change=NavState.set_search,
                class_name="w-full pl-12 pr-4 py-2.5 bg-gray-50 border border-transparent rounded-xl focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 focus:bg-white transition-all duration-200 text-gray-900 placeholder-gray-500 font-medium",
                default_value=NavState.search_query,
            ),
            class_name="relative w-full max-w-md hidden md:block",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "bell",
                        size=20,
                        class_name="text-gray-500 hover:text-gray-700 transition-colors",
                    ),
                    rx.el.div(
                        class_name="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"
                    ),
                    class_name="p-2 relative rounded-full hover:bg-gray-100 transition-colors",
                ),
                rx.el.button(
                    rx.icon(
                        "circle_gauge",
                        size=20,
                        class_name="text-gray-500 hover:text-gray-700 transition-colors",
                    ),
                    class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                ),
                class_name="flex items-center gap-1",
            ),
            rx.el.div(class_name="h-8 w-px bg-gray-200 mx-2"),
            rx.el.button(
                rx.el.div(
                    rx.el.p(
                        "Alex Johnson",
                        class_name="text-sm font-semibold text-gray-900 leading-none",
                    ),
                    rx.el.p(
                        "Admin",
                        class_name="text-xs text-gray-500 font-medium text-right",
                    ),
                    class_name="hidden md:flex flex-col items-end gap-1",
                ),
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=Alex",
                    class_name="h-10 w-10 rounded-full bg-gray-100 border-2 border-white shadow-sm",
                ),
                class_name="flex items-center gap-3 pl-2 hover:opacity-80 transition-opacity",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="h-20 bg-white/90 backdrop-blur-md border-b border-gray-200 px-6 sm:px-8 flex items-center justify-between sticky top-0 z-10",
    )