import reflex as rx
from app.states.nav_state import NavState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.orders_view import orders_view
from app.components.customers_view import customers_view
from app.components.products_view import products_view
from app.components.trials_view import trials_view
from app.components.coupons_view import coupons_view


def dashboard_placeholder() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                NavState.active_item,
                class_name="text-3xl font-bold text-gray-900 mb-2 tracking-tight",
            ),
            rx.el.p(
                f"Manage your {NavState.active_item.lower()} and view performance metrics.",
                class_name="text-gray-500 font-medium",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="h-8 w-1/3 bg-gray-200/50 rounded-lg mb-4"),
                    rx.el.div(class_name="h-64 bg-gray-100/50 rounded-xl"),
                    class_name="p-6 h-full",
                ),
                class_name="col-span-12 lg:col-span-8 bg-white rounded-2xl shadow-sm border border-gray-100 animate-pulse",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="h-8 w-1/2 bg-gray-200/50 rounded-lg mb-4"),
                    rx.el.div(class_name="h-32 bg-gray-100/50 rounded-xl mb-4"),
                    rx.el.div(class_name="h-32 bg-gray-100/50 rounded-xl"),
                    class_name="p-6 h-full",
                ),
                class_name="col-span-12 lg:col-span-4 bg-white rounded-2xl shadow-sm border border-gray-100 animate-pulse",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="h-48 bg-gray-50 rounded-xl border border-gray-200 border-dashed flex items-center justify-center text-gray-400 font-medium"
                ),
                class_name="col-span-12 p-6 bg-white rounded-2xl shadow-sm border border-gray-100",
            ),
            class_name="grid grid-cols-12 gap-6",
        ),
        class_name="p-6 sm:p-8 max-w-7xl mx-auto w-full",
    )


def content_area() -> rx.Component:
    """The main content area which changes based on selection."""
    return rx.match(
        NavState.active_item,
        ("Customers", customers_view()),
        ("Orders", orders_view()),
        ("Products", products_view()),
        ("Trials", trials_view()),
        ("Coupons", coupons_view()),
        dashboard_placeholder(),
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            content_area(),
            class_name="flex-1 ml-0 md:ml-64 min-h-screen bg-gray-50/50 flex flex-col",
        ),
        class_name="flex min-h-screen font-['Inter'] bg-gray-50 text-gray-900",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")