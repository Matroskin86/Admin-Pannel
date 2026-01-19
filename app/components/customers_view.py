import reflex as rx
from app.states.customers_state import CustomersState, Customer


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Active",
            rx.el.span(
                "Active",
                class_name="px-2 py-1 rounded-md text-xs font-medium bg-green-100 text-green-700 w-fit",
            ),
        ),
        (
            "Inactive",
            rx.el.span(
                "Inactive",
                class_name="px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700 w-fit",
            ),
        ),
        (
            "Pending",
            rx.el.span(
                "Pending",
                class_name="px-2 py-1 rounded-md text-xs font-medium bg-yellow-100 text-yellow-700 w-fit",
            ),
        ),
        (
            "VIP",
            rx.el.span(
                "VIP",
                class_name="px-2 py-1 rounded-md text-xs font-medium bg-purple-100 text-purple-700 w-fit",
            ),
        ),
        rx.el.span(
            status,
            class_name="px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700 w-fit",
        ),
    )


def customer_row(customer: Customer) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=customer["avatar"],
                    class_name="h-10 w-10 rounded-full bg-gray-100 object-cover border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p(
                        customer["name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        customer["email"],
                        class_name="text-xs text-gray-500 font-medium",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                customer["phone"], class_name="text-sm text-gray-600 font-medium"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                customer["company"], class_name="text-sm text-gray-900 font-medium"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(customer["status"]), class_name="px-6 py-4 whitespace-nowrap"
        ),
        on_click=lambda: CustomersState.select_customer(customer["id"]),
        class_name=rx.cond(
            CustomersState.selected_customer_id == customer["id"],
            "hover:bg-teal-50/80 bg-teal-50 cursor-pointer transition-colors border-l-4 border-teal-500",
            "hover:bg-gray-50 cursor-pointer transition-colors border-l-4 border-transparent",
        ),
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            CustomersState.showing_text, class_name="text-sm text-gray-500 font-medium"
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=CustomersState.prev_page,
                disabled=CustomersState.page == 1,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.foreach(
                CustomersState.page_numbers,
                lambda p: rx.el.button(
                    p,
                    on_click=lambda: CustomersState.set_page(p),
                    class_name=rx.cond(
                        CustomersState.page == p,
                        "w-8 h-8 flex items-center justify-center rounded-lg bg-teal-600 text-white text-sm font-medium shadow-sm",
                        "w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium",
                    ),
                ),
            ),
            rx.el.button(
                "Next",
                on_click=CustomersState.next_page,
                disabled=CustomersState.page == CustomersState.total_pages,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-6 py-4 border-t border-gray-100",
    )


def customers_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Customer",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Phone",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Company",
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
                rx.foreach(CustomersState.current_page_customers, customer_row),
                class_name="divide-y divide-gray-100 bg-white",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        pagination_controls(),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col justify-between h-full",
    )


def customer_details_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=CustomersState.selected_customer["avatar"],
                    class_name="w-24 h-24 rounded-full bg-gray-50 border-4 border-white shadow-sm mb-4 mx-auto",
                ),
                rx.el.h2(
                    CustomersState.selected_customer["name"],
                    class_name="text-xl font-bold text-gray-900 text-center",
                ),
                rx.el.p(
                    CustomersState.selected_customer["company"],
                    class_name="text-sm text-gray-500 font-medium text-center mb-6",
                ),
                class_name="flex flex-col items-center border-b border-gray-100 pb-6 mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2",
                    ),
                    rx.el.input(
                        name="name",
                        default_value=CustomersState.selected_customer["name"],
                        key=f"name-{CustomersState.selected_customer_id}",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all font-medium text-gray-900 mb-4",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2",
                    ),
                    rx.el.input(
                        name="email",
                        default_value=CustomersState.selected_customer["email"],
                        key=f"email-{CustomersState.selected_customer_id}",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all font-medium text-gray-900 mb-4",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone Number",
                        class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2",
                    ),
                    rx.el.input(
                        name="phone",
                        default_value=CustomersState.selected_customer["phone"],
                        key=f"phone-{CustomersState.selected_customer_id}",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all font-medium text-gray-900 mb-4",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Company",
                        class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2",
                    ),
                    rx.el.input(
                        name="company",
                        default_value=CustomersState.selected_customer["company"],
                        key=f"company-{CustomersState.selected_customer_id}",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all font-medium text-gray-900 mb-6",
                    ),
                ),
                rx.el.button(
                    "Save Changes",
                    type="submit",
                    class_name="w-full py-2.5 bg-teal-600 hover:bg-teal-700 text-white font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98] mb-3",
                ),
                on_submit=CustomersState.update_customer,
            ),
            rx.el.button(
                "Delete Customer",
                on_click=CustomersState.delete_customer,
                class_name="w-full py-2.5 bg-white border border-red-200 text-red-600 hover:bg-red-50 font-medium rounded-xl transition-all active:scale-[0.98]",
            ),
        ),
        class_name="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 h-full",
    )


def add_customer_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Add New Customer", class_name="text-lg font-bold text-gray-900 mb-4"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="name",
                        placeholder="John Doe",
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="email",
                        type="email",
                        placeholder="john@example.com",
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="phone",
                        placeholder="+1 (555) 000-0000",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Company",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="company",
                        placeholder="Acme Corp",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-6",
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
                        "Add Customer",
                        type="submit",
                        class_name="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=CustomersState.add_customer,
                reset_on_submit=True,
            ),
        ),
        open=CustomersState.is_add_modal_open,
        on_open_change=CustomersState.toggle_add_modal,
    )


def customers_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"Customers ({CustomersState.total_items})",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Manage your customer base and contact information.",
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
                    on_change=CustomersState.set_search,
                    class_name="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none w-64 transition-all",
                    default_value=CustomersState.search_query,
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("plus", size=18),
                rx.el.span("Add New User"),
                on_click=CustomersState.toggle_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-sm font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98]",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
    )


def customers_view() -> rx.Component:
    return rx.el.div(
        add_customer_modal(),
        customers_header(),
        rx.el.div(
            rx.el.div(
                customers_table(), class_name="col-span-12 lg:col-span-8 flex flex-col"
            ),
            rx.el.div(
                rx.cond(
                    CustomersState.customers,
                    customer_details_panel(),
                    rx.el.div(
                        "No customer selected",
                        class_name="flex items-center justify-center h-full text-gray-400 bg-white rounded-2xl border border-gray-100",
                    ),
                ),
                class_name="col-span-12 lg:col-span-4 h-fit",
            ),
            class_name="grid grid-cols-12 gap-6 items-start",
        ),
        class_name="p-6 sm:p-8 max-w-7xl mx-auto w-full",
    )