import reflex as rx
from app.states.trials_state import TrialsState, Trial


def trial_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Active",
            rx.el.span(
                "Active",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 w-fit border border-blue-100",
            ),
        ),
        (
            "Expired",
            rx.el.span(
                "Expired",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-700 w-fit border border-gray-200",
            ),
        ),
        (
            "Converted",
            rx.el.span(
                "Converted",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-green-50 text-green-700 w-fit border border-green-100",
            ),
        ),
        (
            "Pending",
            rx.el.span(
                "Pending",
                class_name="px-2.5 py-1 rounded-lg text-xs font-medium bg-yellow-50 text-yellow-700 w-fit border border-yellow-100",
            ),
        ),
        rx.el.span(status),
    )


def trial_row(trial: Trial) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(trial["id"], class_name="font-mono text-gray-500 text-xs"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        trial["customer_name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=trial["image"],
                    class_name="h-8 w-8 rounded-lg bg-gray-50 object-cover border border-gray-100",
                ),
                rx.el.span(
                    trial["product_name"],
                    class_name="text-sm text-gray-900 font-medium",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                trial["end_date"], class_name="text-sm text-gray-600 font-medium"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            trial_status_badge(trial["status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        on_click=lambda: TrialsState.select_trial(trial["id"]),
        class_name=rx.cond(
            TrialsState.selected_trial_id == trial["id"],
            "hover:bg-teal-50/80 bg-teal-50 cursor-pointer transition-colors border-l-4 border-teal-500",
            "hover:bg-gray-50 cursor-pointer transition-colors border-l-4 border-transparent",
        ),
    )


def trials_pagination() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            TrialsState.showing_text, class_name="text-sm text-gray-500 font-medium"
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=TrialsState.prev_page,
                disabled=TrialsState.page == 1,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.foreach(
                TrialsState.page_numbers,
                lambda p: rx.el.button(
                    p,
                    on_click=lambda: TrialsState.set_page(p),
                    class_name=rx.cond(
                        TrialsState.page == p,
                        "w-8 h-8 flex items-center justify-center rounded-lg bg-teal-600 text-white text-sm font-medium shadow-sm",
                        "w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium",
                    ),
                ),
            ),
            rx.el.button(
                "Next",
                on_click=TrialsState.next_page,
                disabled=TrialsState.page == TrialsState.total_pages,
                class_name="px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-6 py-4 border-t border-gray-100",
    )


def trials_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "ID",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-16",
                    ),
                    rx.el.th(
                        "Customer",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Product",
                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "End Date",
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
                rx.foreach(TrialsState.current_page_trials, trial_row),
                class_name="divide-y divide-gray-100 bg-white",
            ),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        trials_pagination(),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col justify-between h-full",
    )


def trial_details_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Trial Details", class_name="text-lg font-bold text-gray-900 mb-6"
            ),
            rx.el.div(
                rx.image(
                    src=TrialsState.selected_trial["image"],
                    class_name="h-20 w-20 rounded-xl bg-gray-50 object-cover border border-gray-100 shadow-sm",
                ),
                rx.el.div(
                    rx.el.p(
                        "Trial ID", class_name="text-xs text-gray-400 font-medium mb-1"
                    ),
                    rx.el.h2(
                        TrialsState.selected_trial["id"],
                        class_name="text-base font-bold text-gray-900 mb-2 leading-tight font-mono",
                    ),
                    rx.el.p(
                        TrialsState.selected_trial["product_name"],
                        class_name="text-sm text-teal-600 font-medium bg-teal-50 px-2 py-1 rounded w-fit",
                    ),
                    class_name="flex flex-col flex-1",
                ),
                class_name="flex items-start gap-4 mb-6 pb-6 border-b border-gray-100",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Customer",
                        class_name="text-xs text-gray-500 uppercase font-bold mb-1",
                    ),
                    rx.el.p(
                        TrialsState.selected_trial["customer_name"],
                        class_name="text-sm font-medium text-gray-900",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Start Date",
                            class_name="text-xs text-gray-500 uppercase font-bold mb-1",
                        ),
                        rx.el.p(
                            TrialsState.selected_trial["start_date"],
                            class_name="text-sm font-medium text-gray-900",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "End Date",
                            class_name="text-xs text-gray-500 uppercase font-bold mb-1",
                        ),
                        rx.el.p(
                            TrialsState.selected_trial["end_date"],
                            class_name="text-sm font-medium text-gray-900",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", size=16, class_name="mr-2"),
                "Delete Trial",
                on_click=TrialsState.delete_trial,
                class_name="flex items-center justify-center w-full py-2.5 text-red-600 hover:bg-red-50 bg-white border border-red-100 rounded-xl text-sm font-medium transition-colors mb-8",
            ),
        ),
        rx.el.div(
            rx.el.h4(
                "Update Status", class_name="text-sm font-bold text-gray-900 mb-4"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Status",
                        class_name="block text-xs font-semibold text-gray-500 uppercase mb-2",
                    ),
                    rx.el.select(
                        rx.el.option("Active", value="Active"),
                        rx.el.option("Expired", value="Expired"),
                        rx.el.option("Converted", value="Converted"),
                        rx.el.option("Pending", value="Pending"),
                        name="status",
                        default_value=TrialsState.selected_trial["status"],
                        key=f"status-{TrialsState.selected_trial_id}",
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
                on_submit=TrialsState.update_trial,
            ),
            class_name="border-t border-gray-100 pt-6",
        ),
        class_name="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 h-full flex flex-col",
    )


def add_trial_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Add New Trial", class_name="text-lg font-bold text-gray-900 mb-6"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Customer Name",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="customer_name",
                        placeholder="e.g. John Doe",
                        required=True,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Product Name",
                        class_name="text-sm font-medium text-gray-700 mb-1 block",
                    ),
                    rx.el.input(
                        name="product_name",
                        placeholder="e.g. Chanel No. 5",
                        required=True,
                        class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent",
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
                        "Add Trial",
                        type="submit",
                        class_name="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700 shadow-sm",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=TrialsState.add_trial,
                reset_on_submit=True,
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-md w-full",
        ),
        open=TrialsState.is_add_modal_open,
        on_open_change=TrialsState.toggle_add_modal,
    )


def trials_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"Trials ({TrialsState.total_items})",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Manage product trials and samples.",
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
                    placeholder="Search trial...",
                    on_change=TrialsState.set_search,
                    class_name="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none w-64 transition-all",
                    default_value=TrialsState.search_query,
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("plus", size=18),
                rx.el.span("New Trial"),
                on_click=TrialsState.toggle_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-sm font-medium rounded-xl shadow-sm shadow-teal-200 transition-all active:scale-[0.98]",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
    )


def trials_view() -> rx.Component:
    return rx.el.div(
        add_trial_modal(),
        trials_header(),
        rx.el.div(
            rx.el.div(
                trials_table(), class_name="col-span-12 lg:col-span-8 flex flex-col"
            ),
            rx.el.div(
                rx.cond(
                    TrialsState.trials,
                    trial_details_panel(),
                    rx.el.div(
                        "No trial selected",
                        class_name="flex items-center justify-center h-full text-gray-400 bg-white rounded-2xl border border-gray-100 p-8",
                    ),
                ),
                class_name="col-span-12 lg:col-span-4 h-fit",
            ),
            class_name="grid grid-cols-12 gap-6 items-start",
        ),
        class_name="p-6 sm:p-8 max-w-7xl mx-auto w-full",
    )