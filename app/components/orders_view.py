import reflex as rx
from app.states.orders_state import OrdersState, Order


def order_row(order: Order) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(order["id"], class_name="font-mono text-sm font-medium"),
            class_name="px-6 py-4 whitespace-nowrap text-gray-900",
        ),
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=order["image"],
                    class_name="h-10 w-10 rounded-lg bg-gray-100 object-cover",
                ),
                rx.el.span(
                    order["product_name"], class_name="font-medium text-gray-900"
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(order["quantity"], class_name="text-gray-600 font-medium"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"${order['total']:.2f}", class_name="text-gray-900 font-semibold"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        on_click=lambda: OrdersState.select_order(order["id"]),
        class_name=rx.cond(
            OrdersState.selected_order_id == order["id"],
            "hover:bg-teal-50/80 bg-teal-50 cursor-pointer transition-colors border-l-4 border-teal-500",
            "hover:bg-gray-50 cursor-pointer transition-colors border-l-4 border-transparent",
        ),
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            OrdersState.showing_text, class_name="text-sm text-gray-500 font-medium"
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=OrdersState.prev_page,
                disabled=OrdersState.page == 1,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.foreach(
                OrdersState.page_numbers,
                lambda p: rx.el.button(
                    p,
                    on_click=lambda: OrdersState.set_page(p),
                    class_name=rx.cond(
                        OrdersState.page == p,
                        "w-8 h-8 flex items-center justify-center rounded-lg bg-teal-600 text-white text-sm font-medium shadow-sm",
                        "w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium",
                    ),
                ),
            ),
            rx.el.button(
                "Next",
                on_click=OrdersState.next_page,
                disabled=OrdersState.page == OrdersState.total_pages,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-6 py-4 border-t border-gray-100",
    )


def orders_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "ID",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Product",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Quantity",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Charged",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    class_name="bg-gray-50/50",
                )
            ),
            rx.el.tbody(
                rx.foreach(OrdersState.current_page_orders, order_row),
                class_name="divide-y divide-gray-100 bg-white",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        pagination_controls(),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col justify-between h-full",
    )


def product_details_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=OrdersState.selected_order["image"],
                class_name="w-full h-48 object-cover rounded-xl mb-6 bg-gray-50",
            ),
            rx.el.div(
                rx.el.h2(
                    OrdersState.selected_order["product_name"],
                    class_name="text-xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    OrdersState.selected_order["id"],
                    class_name="text-sm text-gray-500 font-mono mb-6",
                ),
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Unit Price",
                            class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "$",
                                class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-medium",
                            ),
                            rx.el.input(
                                name="price",
                                type="number",
                                step="0.01",
                                default_value=OrdersState.selected_order["price"],
                                key=f"price-{OrdersState.selected_order_id}",
                                class_name="w-full pl-7 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all font-medium text-gray-900",
                            ),
                            class_name="relative",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Quantity",
                            class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2",
                        ),
                        rx.el.input(
                            name="quantity",
                            type="number",
                            default_value=OrdersState.selected_order["quantity"],
                            key=f"qty-{OrdersState.selected_order_id}",
                            class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all font-medium text-gray-900",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Total Value", class_name="text-sm text-gray-500"),
                        rx.el.p(
                            f"${OrdersState.selected_order['total']:.2f}",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p("Ordered On", class_name="text-sm text-gray-500"),
                        rx.el.p(
                            OrdersState.selected_order["date"],
                            class_name="text-sm font-medium text-gray-900",
                        ),
                    ),
                    class_name="flex items-center justify-between p-4 bg-gray-50 rounded-xl mb-6",
                ),
                rx.el.button(
                    "Save Changes",
                    type="submit",
                    class_name="w-full py-2.5 bg-teal-600 hover:bg-teal-700 text-white font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98] mb-3",
                ),
                on_submit=OrdersState.update_order,
            ),
            rx.el.button(
                "Delete Product",
                on_click=OrdersState.delete_order,
                class_name="w-full py-2.5 bg-white border border-red-200 text-red-600 hover:bg-red-50 font-medium rounded-xl transition-all active:scale-[0.98]",
            ),
        ),
        class_name="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 h-full",
    )


def orders_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"Orders ({OrdersState.total_items})",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Manage and track all your customer orders here.",
                class_name="text-gray-500 font-medium text-sm",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                    size=18,
                ),
                rx.el.input(
                    placeholder="Search customer...",
                    on_change=OrdersState.set_search,
                    class_name="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none w-64 transition-all",
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("plus", size=18),
                rx.el.span("Add New User"),
                class_name="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-sm font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98]",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
    )


def orders_view() -> rx.Component:
    return rx.el.div(
        orders_header(),
        rx.el.div(
            rx.el.div(
                orders_table(), class_name="col-span-12 lg:col-span-8 flex flex-col"
            ),
            rx.el.div(
                rx.cond(
                    OrdersState.orders,
                    product_details_panel(),
                    rx.el.div(
                        "No order selected",
                        class_name="flex items-center justify-center h-full text-gray-400 bg-white rounded-2xl border border-gray-100",
                    ),
                ),
                class_name="col-span-12 lg:col-span-4 h-fit",
            ),
            class_name="grid grid-cols-12 gap-6 items-start",
        ),
        class_name="p-6 sm:p-8 max-w-7xl mx-auto w-full",
    )