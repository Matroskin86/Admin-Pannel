import reflex as rx
from app.states.coupons_state import CouponsState, Coupon


def coupon_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Active",
            rx.el.span(
                "Active",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-green-50 text-green-700 w-fit border border-green-100",
            ),
        ),
        (
            "Expired",
            rx.el.span(
                "Expired",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-red-50 text-red-700 w-fit border border-red-100",
            ),
        ),
        (
            "Exhausted",
            rx.el.span(
                "Exhausted",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-700 w-fit border border-gray-200",
            ),
        ),
        rx.el.span(status),
    )


def coupon_row(coupon: Coupon) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    coupon["code"],
                    class_name="font-mono font-bold text-teal-700 text-sm bg-teal-50 px-2 py-1 rounded border border-teal-100",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(coupon["type"], class_name="text-sm text-gray-600 font-medium"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    coupon["type"] == "Percentage",
                    f"{coupon['value']:.0f}%",
                    f"${coupon['value']:.0f}",
                ),
                class_name="text-sm text-gray-900 font-bold",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{coupon['used']} / {coupon['limit']}",
                    class_name="text-xs font-medium text-gray-600 mb-1 block",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-1.5 rounded-full bg-teal-500",
                        style={"width": f"{coupon['used'] / coupon['limit'] * 100}%"},
                    ),
                    class_name="w-24 h-1.5 bg-gray-100 rounded-full overflow-hidden",
                ),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            coupon_status_badge(coupon["status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        on_click=lambda: CouponsState.select_coupon(coupon["code"]),
        class_name=rx.cond(
            CouponsState.selected_code == coupon["code"],
            "hover:bg-teal-50/80 bg-teal-50 cursor-pointer transition-colors border-l-4 border-teal-500",
            "hover:bg-gray-50 cursor-pointer transition-colors border-l-4 border-transparent",
        ),
    )


def coupons_pagination() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            CouponsState.showing_text, class_name="text-sm text-gray-500 font-medium"
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=CouponsState.prev_page,
                disabled=CouponsState.page == 1,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.foreach(
                CouponsState.page_numbers,
                lambda p: rx.el.button(
                    p,
                    on_click=lambda: CouponsState.set_page(p),
                    class_name=rx.cond(
                        CouponsState.page == p,
                        "w-8 h-8 flex items-center justify-center rounded-lg bg-teal-600 text-white text-sm font-medium shadow-sm",
                        "w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium",
                    ),
                ),
            ),
            rx.el.button(
                "Next",
                on_click=CouponsState.next_page,
                disabled=CouponsState.page == CouponsState.total_pages,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-6 py-4 border-t border-gray-100",
    )


def coupons_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Code",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Type",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Value",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Usage",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Status",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    class_name="bg-gray-50/50",
                )
            ),
            rx.el.tbody(
                rx.foreach(CouponsState.current_page_coupons, coupon_row),
                class_name="divide-y divide-gray-100 bg-white",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        coupons_pagination(),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col justify-between h-full",
    )


def coupon_details_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Coupon Details", class_name="text-lg font-bold text-gray-900 mb-6"
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("ticket", class_name="text-teal-600", size=32),
                    class_name="h-16 w-16 rounded-2xl bg-teal-50 flex items-center justify-center mb-4",
                ),
                rx.el.h2(
                    CouponsState.selected_coupon["code"],
                    class_name="text-2xl font-bold text-gray-900 mb-1 font-mono tracking-wider",
                ),
                rx.el.p(
                    "Discount Code", class_name="text-sm text-gray-500 font-medium mb-6"
                ),
                class_name="flex flex-col items-center border-b border-gray-100 pb-6 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Discount Type",
                        class_name="text-xs text-gray-500 uppercase font-bold mb-1",
                    ),
                    rx.el.p(
                        CouponsState.selected_coupon["type"],
                        class_name="text-sm font-medium text-gray-900",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Value",
                            class_name="text-xs text-gray-500 uppercase font-bold mb-1",
                        ),
                        rx.el.p(
                            rx.cond(
                                CouponsState.selected_coupon["type"] == "Percentage",
                                f"{CouponsState.selected_coupon['value']:.0f}%",
                                f"${CouponsState.selected_coupon['value']:.0f}",
                            ),
                            class_name="text-lg font-bold text-teal-600",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Used Count",
                            class_name="text-xs text-gray-500 uppercase font-bold mb-1",
                        ),
                        rx.el.p(
                            CouponsState.selected_coupon["used"],
                            class_name="text-lg font-bold text-gray-900",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", size=16, class_name="mr-2"),
                "Delete Coupon",
                on_click=CouponsState.delete_coupon,
                class_name="flex items-center justify-center w-full py-2.5 text-red-600 hover:bg-red-50 bg-white border border-red-100 rounded-xl text-sm font-medium transition-colors mb-8",
            ),
        ),
        rx.el.div(
            rx.el.h4(
                "Update Limits", class_name="text-sm font-bold text-gray-900 mb-4"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Usage Limit",
                        class_name="block text-xs font-semibold text-gray-500 uppercase mb-2",
                    ),
                    rx.el.input(
                        name="limit",
                        type="number",
                        default_value=CouponsState.selected_coupon["limit"],
                        key=f"limit-{CouponsState.selected_code}",
                        class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm font-medium focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Expiry Date",
                        class_name="block text-xs font-semibold text-gray-500 uppercase mb-2",
                    ),
                    rx.el.input(
                        name="expiry_date",
                        type="date",
                        default_value=CouponsState.selected_coupon["expiry_date"],
                        key=f"expiry-{CouponsState.selected_code}",
                        class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm font-medium focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    rx.icon("save", size=18, class_name="mr-2"),
                    "Save Changes",
                    type="submit",
                    class_name="w-full flex items-center justify-center py-2.5 bg-white border border-teal-600 text-teal-700 hover:bg-teal-50 font-medium rounded-xl transition-all shadow-sm",
                ),
                on_submit=CouponsState.update_coupon,
            ),
            class_name="border-t border-gray-100 pt-6",
        ),
        class_name="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 h-full flex flex-col",
    )


def add_coupon_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Create New Coupon", class_name="text-lg font-bold text-gray-900 mb-6"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Coupon Code",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="code",
                        placeholder="e.g. SUMMER2024",
                        required=True,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent uppercase",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Discount Type",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.select(
                        rx.el.option("Percentage", value="Percentage"),
                        rx.el.option("Fixed Amount", value="Fixed Amount"),
                        name="type",
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Value",
                            class_name="text-sm font-medium text-gray-700 mb-1 block",
                        ),
                        rx.el.input(
                            name="value",
                            type="number",
                            placeholder="20",
                            required=True,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Usage Limit",
                            class_name="text-sm font-medium text-gray-700 mb-1 block",
                        ),
                        rx.el.input(
                            name="limit",
                            type="number",
                            placeholder="100",
                            required=True,
                            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 mr-2",
                        )
                    ),
                    rx.el.button(
                        "Create Coupon",
                        type="submit",
                        class_name="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700 shadow-sm",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=CouponsState.add_coupon,
                reset_on_submit=True,
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-md w-full",
        ),
        open=CouponsState.is_add_modal_open,
        on_open_change=CouponsState.toggle_add_modal,
    )


def coupons_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"Coupons ({CouponsState.total_items})",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Manage discount codes and promotions.",
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
                    placeholder="Search code...",
                    on_change=CouponsState.set_search,
                    class_name="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none w-64 transition-all",
                    default_value=CouponsState.search_query,
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("plus", size=18),
                rx.el.span("New Coupon"),
                on_click=CouponsState.toggle_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-sm font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98]",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
    )


def coupons_view() -> rx.Component:
    return rx.el.div(
        add_coupon_modal(),
        coupons_header(),
        rx.el.div(
            rx.el.div(
                coupons_table(), class_name="col-span-12 lg:col-span-8 flex flex-col"
            ),
            rx.el.div(
                rx.cond(
                    CouponsState.coupons,
                    coupon_details_panel(),
                    rx.el.div(
                        "No coupon selected",
                        class_name="flex items-center justify-center h-full text-gray-400 bg-white rounded-2xl border border-gray-100 p-8",
                    ),
                ),
                class_name="col-span-12 lg:col-span-4 h-fit",
            ),
            class_name="grid grid-cols-12 gap-6 items-start",
        ),
        class_name="p-6 sm:p-8 max-w-7xl mx-auto w-full",
    )